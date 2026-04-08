from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QLabel, QAbstractItemView, QWidget, QSizePolicy, QCheckBox, QStackedWidget
from PySide6.QtCore import Qt, QDate, QCoreApplication, QSize, Signal, QTimer
from PySide6.QtGui import QTextCharFormat, QBrush, QColor, QFont
from .ui_08_LineEditFrame import LineEditFrame
from .ui_09_BadgeCalendarWidget import BadgeCalendarWidget
from .ui_13_YearCalendarWidget import YearCalendarWidget
from .ui_10_CalendarDialog import CalendarDialog
from source.modules.eisenhower.interface.CalendarDialog import install_palette_theme_sync
from source.modules.eisenhower.services import show_context_menu
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class CalendarPanel(QWidget):
    month_view_toggle_visibility_changed = Signal(bool)
    month_view_mode_changed = Signal(str)

    def __init__(self, app, parent=None):
        super().__init__(parent)

        try:
            self.app = app
            self._date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"
            self._highlighted_dates = set()
            self._calendar_view_mode = "month"
            self._calendar_content_width = 300
            self._syncing_month_calendars = False
            self._extra_month_calendars = []
            self._extra_highlighted_dates = set()
            self._syncing_year_calendars = False
            self._extra_year_calendars = []
            self._year_sync_pending = False
            self._year_calendar_pool = []
            self._year_resize_timer = QTimer(self)
            self._year_resize_timer.setSingleShot(True)
            self._year_resize_timer.timeout.connect(self._update_year_calendars_for_width)

            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(5, 1, 5, 9)
            main_layout.setSpacing(6)

            self.calendar = BadgeCalendarWidget(self)
            self.calendar.app = app
            self.calendar.owner = self
            initial_date = app.date_input.date() if hasattr(app, "date_input") else QDate.currentDate()
            self._selected_reference_date = initial_date
            self.calendar.setSelectedDate(initial_date)
            hint = self.calendar.minimumSizeHint()
            fallback = QSize(300, 260)
            cal_size = hint.expandedTo(fallback)
            self._calendar_content_width = max(1, int(cal_size.width()))
            self.calendar.setMinimumSize(cal_size)
            self.calendar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self._apply_locale_to_calendar()

            self.year_calendar = YearCalendarWidget(self)
            self.year_calendar.app = app
            self.year_calendar.owner = self
            self.year_calendar.setSelectedDate(initial_date)
            self.year_calendar.monthSelected.connect(self._on_year_month_selected)
            self.year_calendar.monthDoubleClicked.connect(self._on_year_month_double_clicked)
            self._configure_year_calendar_widget(self.year_calendar)

            self.months_container = QWidget(self)
            self.months_layout = QHBoxLayout(self.months_container)
            self.months_layout.setContentsMargins(0, 0, 0, 0)
            self.months_layout.setSpacing(6)
            self.months_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.months_layout.addWidget(self.calendar, 0, Qt.AlignLeft | Qt.AlignTop)

            self.years_container = QWidget(self)
            self.years_layout = QHBoxLayout(self.years_container)
            self.years_layout.setContentsMargins(0, 0, 0, 0)
            self.years_layout.setSpacing(6)
            self.years_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.years_layout.addWidget(self.year_calendar, 0, Qt.AlignLeft | Qt.AlignTop)

            self.calendar_stack = QStackedWidget(self)
            self.calendar_stack.addWidget(self.months_container)
            self.calendar_stack.addWidget(self.years_container)

            self.calendar_frame = LineEditFrame(self)
            self.calendar_frame.layout().addWidget(self.calendar_stack)
            main_layout.addWidget(self.calendar_frame)

            self.controls_container = QWidget(self)
            controls_layout = QHBoxLayout(self.controls_container)
            controls_layout.setContentsMargins(0, 0, 0, 0)
            controls_layout.setSpacing(6)
            self.filter_label = QLabel(get_text("Exibir por"), self)
            controls_layout.addWidget(self.filter_label)

            self.filter_combo = QComboBox(self)
            self.filter_combo.addItem(get_text("Dia"), "day")
            self.filter_combo.addItem(get_text("Semana"), "week")
            self.filter_combo.addItem(get_text("Mês"), "month")
            self.filter_combo.addItem(get_text("Ano"), "year")
            controls_layout.addWidget(self.filter_combo)
            controls_layout.addStretch()
            self.show_priority_checkbox = QCheckBox(get_text("Mostrar prioridade"), self)
            self.show_priority_checkbox.setChecked(True)
            self.show_priority_checkbox.stateChanged.connect(self.update_task_list)
            controls_layout.addWidget(self.show_priority_checkbox)
            self.controls_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            main_layout.addWidget(self.controls_container, 0, Qt.AlignLeft)

            self.tasks_label = QLabel(get_text("Lista Global de Tarefas:"), self)
            main_layout.addWidget(self.tasks_label)

            self.tasks_list = QListWidget(self)
            self.tasks_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

            try:
                self.tasks_list.setSelectionBehavior(QAbstractItemView.SelectItems)
                self.tasks_list.setSelectionRectVisible(True)

            except Exception:
                pass

            self.tasks_list.setMouseTracking(True)
            self.tasks_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            self.tasks_list.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tasks_list.customContextMenuRequested.connect(lambda pt: show_context_menu(self.app, pt, self.tasks_list))

            try:
                self.tasks_list.itemDoubleClicked.connect(lambda item: CalendarDialog._open_linked_file(self, item))

            except Exception:
                pass

            main_layout.addWidget(self.tasks_list, 1)

            self.calendar.selectionChanged.connect(self._on_primary_calendar_selection_changed)
            self.calendar.currentPageChanged.connect(self._on_primary_calendar_page_changed)
            self.filter_combo.currentIndexChanged.connect(self._on_filter_mode_changed)

            if hasattr(self.app, "gerenciador_traducao"):
                self.app.gerenciador_traducao.idioma_alterado.connect(self._on_language_changed)

            self.set_calendar_content_width(self._calendar_content_width)
            self._update_month_calendars_for_width()
            self._update_year_calendars_for_width()
            self._on_filter_mode_changed()
            self.update_task_list()

            install_palette_theme_sync(self, logger)

        except Exception as e:
            logger.error(f"Erro ao inicializar CalendarPanel: {e}", exc_info=True)

    def set_calendar_content_width(self, width: int):
        try:
            self._calendar_content_width = max(1, int(width))

            if hasattr(self, "calendar"):
                self.calendar.setFixedWidth(self._calendar_content_width)

            for extra_calendar in list(getattr(self, "_extra_month_calendars", []) or []):
                if extra_calendar is not None:
                    extra_calendar.setFixedWidth(self._calendar_content_width)

            if hasattr(self, "year_calendar"):
                self.year_calendar.setFixedWidth(self._calendar_content_width)

            for extra_year_calendar in list(getattr(self, "_extra_year_calendars", []) or []):
                if extra_year_calendar is not None:
                    extra_year_calendar.setFixedWidth(self._calendar_content_width)

            if hasattr(self, "controls_container"):
                self.controls_container.setFixedWidth(self._calendar_content_width)

            if hasattr(self, "calendar_stack"):
                self.calendar_stack.setMinimumWidth(self._calendar_content_width)

            if hasattr(self, "calendar_frame"):
                self.calendar_frame.setMinimumWidth(self._calendar_content_width)

            if self._is_month_view_active():
                self._update_month_calendars_for_width()

            if self._is_year_view_active():
                self._update_year_calendars_for_width()

            if self._is_month_view_active():
                self._sync_month_calendar_pages_from_primary()

            if self._is_year_view_active():
                self._sync_year_calendar_pages_from_primary()

            self.updateGeometry()

        except Exception as e:
            logger.error(f"Erro ao aplicar largura fixa ao calendário: {e}", exc_info=True)

    def resizeEvent(self, event):
        try:
            if self._is_month_view_active():
                self._update_month_calendars_for_width()

            if self._is_year_view_active():
                target_count = self._desired_year_calendar_count()
                self._reconcile_year_calendar_count(target_count, sync_after_change=False)
                self._apply_year_calendar_width_distribution()
                self._schedule_year_calendars_update(80)

        except Exception as e:
            logger.error(f"Erro ao atualizar quantidade de calendários no resize: {e}", exc_info=True)

        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)

        try:
            if self._is_month_view_active():
                QTimer.singleShot(0, self._update_month_calendars_for_width)

            if self._is_year_view_active():
                QTimer.singleShot(0, self._update_year_calendars_for_width)

        except Exception as e:
            logger.error(f"Erro ao atualizar calendários no show: {e}", exc_info=True)

    def _is_month_view_active(self) -> bool:
        try:
            return bool(self.isVisible() and hasattr(self, "calendar_stack") and hasattr(self, "months_container") and self.calendar_stack.currentWidget() is self.months_container)

        except Exception:
            return False

    def _is_year_view_active(self) -> bool:
        try:
            return bool(self.isVisible() and hasattr(self, "calendar_stack") and hasattr(self, "years_container") and self.calendar_stack.currentWidget() is self.years_container)

        except Exception:
            return False

    def _schedule_year_calendars_update(self, delay_ms: int = 24):
        try:
            delay = max(0, int(delay_ms))

            if hasattr(self, "_year_resize_timer") and self._year_resize_timer is not None:
                if delay == 0:
                    self._year_resize_timer.stop()
                    self._year_resize_timer.start(0)

                else:
                    self._year_resize_timer.stop()
                    self._year_resize_timer.start(delay)

            else:
                self._update_year_calendars_for_width()

        except Exception as e:
            logger.error(f"Erro ao agendar atualização dos calendários anuais: {e}", exc_info=True)

    def _available_calendar_width(self) -> int:
        try:
            margins = self.layout().contentsMargins() if self.layout() is not None else None
            available = int(self.width())

            if margins is not None:
                available -= int(margins.left()) + int(margins.right())

            return max(0, available)

        except Exception:
            return max(0, int(self.width()))

    def _available_months_inner_width(self) -> int:
        try:
            if not self.isVisible():
                return max(1, int(getattr(self, "_calendar_content_width", 1)))

            if hasattr(self, "months_layout") and hasattr(self, "months_container"):
                margins = self.months_layout.contentsMargins()
                available = int(self.months_container.width())
                available -= int(margins.left()) + int(margins.right())

                if available > 0:
                    return available

            if hasattr(self, "calendar_stack"):
                fallback = int(self.calendar_stack.width())

                if fallback > 0:
                    return fallback

            fallback = self._available_calendar_width()

            if fallback > 0:
                return fallback

            return max(1, int(getattr(self, "_calendar_content_width", 1)))

        except Exception:
            return max(1, int(getattr(self, "_calendar_content_width", 1)))

    def _available_years_inner_width(self) -> int:
        try:
            if not self.isVisible():
                return max(1, int(getattr(self, "_calendar_content_width", 1)))

            try:
                if hasattr(self, "calendar_stack") and hasattr(self, "years_container"):
                    if self.calendar_stack.currentWidget() is not self.years_container:
                        return max(1, int(getattr(self, "_calendar_content_width", 1)))

            except Exception:
                pass

            if hasattr(self, "years_layout") and hasattr(self, "years_container"):
                margins = self.years_layout.contentsMargins()
                available = int(self.years_container.width())
                available -= int(margins.left()) + int(margins.right())

                if available > 0:
                    return available

            if hasattr(self, "calendar_stack"):
                fallback = int(self.calendar_stack.width())

                if fallback > 0:
                    return fallback

            fallback = self._available_calendar_width()

            if fallback > 0:
                return fallback

            return max(1, int(getattr(self, "_calendar_content_width", 1)))

        except Exception:
            return max(1, int(getattr(self, "_calendar_content_width", 1)))

    def _desired_month_calendar_count(self) -> int:
        try:
            base_width = max(1, int(getattr(self, "_calendar_content_width", 1)))
            available = self._available_months_inner_width()
            spacing = max(0, int(self.months_layout.spacing())) if hasattr(self, "months_layout") else 0
            return max(1, int((available + spacing) // (base_width + spacing)))

        except Exception:
            return 1

    def _apply_month_calendar_width_distribution(self):
        try:
            calendars = [self.calendar] + list(getattr(self, "_extra_month_calendars", []) or [])
            calendars = [calendar_widget for calendar_widget in calendars if calendar_widget is not None]

            if not calendars:
                return

            spacing = max(0, int(self.months_layout.spacing())) if hasattr(self, "months_layout") else 0
            available = self._available_months_inner_width()
            total_spacing = spacing * max(0, len(calendars) - 1)
            distributable_width = max(0, available - total_spacing)

            if distributable_width <= 0:
                return

            base_width = distributable_width // len(calendars)
            remainder = distributable_width % len(calendars)

            for index, calendar_widget in enumerate(calendars):
                target_width = base_width + (1 if index < remainder else 0)
                calendar_widget.setFixedWidth(max(1, int(target_width)))

        except Exception as e:
            logger.error(f"Erro ao distribuir largura entre calendários mensais: {e}", exc_info=True)

    def _create_extra_month_calendar(self):
        try:
            extra_calendar = BadgeCalendarWidget(self.months_container)
            extra_calendar.app = self.app
            extra_calendar.owner = self
            hint = extra_calendar.minimumSizeHint()
            fallback = QSize(self._calendar_content_width, 260)
            extra_calendar.setMinimumSize(hint.expandedTo(fallback))
            extra_calendar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            extra_calendar.setFixedWidth(self._calendar_content_width)

            try:
                extra_calendar.setLocale(self.calendar.locale())
                extra_calendar.setFirstDayOfWeek(self.calendar.firstDayOfWeek())

            except Exception:
                pass

            extra_calendar.selectionChanged.connect(lambda cal=extra_calendar: self._on_extra_calendar_selection_changed(cal))
            extra_calendar.currentPageChanged.connect(lambda year, month, cal=extra_calendar: self._on_extra_calendar_page_changed(cal, year, month))
            self.months_layout.addWidget(extra_calendar, 0, Qt.AlignLeft | Qt.AlignTop)
            self._extra_month_calendars.append(extra_calendar)

        except Exception as e:
            logger.error(f"Erro ao criar calendário mensal extra: {e}", exc_info=True)

    def _remove_last_extra_month_calendar(self):
        try:
            if not self._extra_month_calendars:
                return

            extra_calendar = self._extra_month_calendars.pop()

            try:
                self.months_layout.removeWidget(extra_calendar)

            except Exception:
                pass

            if extra_calendar is not None:
                extra_calendar.deleteLater()

        except Exception as e:
            logger.error(f"Erro ao remover calendário mensal extra: {e}", exc_info=True)

    def _ensure_month_calendar_count(self, target_count: int):
        try:
            target_count = max(1, int(target_count))
            current_count = 1 + len(self._extra_month_calendars)

            while current_count < target_count:
                self._create_extra_month_calendar()
                current_count += 1

            while current_count > target_count:
                self._remove_last_extra_month_calendar()
                current_count -= 1

        except Exception as e:
            logger.error(f"Erro ao ajustar quantidade de calendários mensais: {e}", exc_info=True)

    def _update_month_calendars_for_width(self):
        try:
            target_count = self._desired_month_calendar_count()
            self._ensure_month_calendar_count(target_count)
            self._apply_month_calendar_width_distribution()
            self._sync_month_calendar_pages_from_primary()
            self._sync_month_calendars_visual_data()

        except Exception as e:
            logger.error(f"Erro ao atualizar calendários mensais por largura: {e}", exc_info=True)

    def _desired_year_calendar_count(self) -> int:
        try:
            base_width = max(1, int(getattr(self, "_calendar_content_width", 1)))
            available = self._available_years_inner_width()
            return max(1, int(available // base_width))

        except Exception:
            return 1

    def _apply_year_calendar_width_distribution(self):
        try:
            calendars = [self.year_calendar] + list(getattr(self, "_extra_year_calendars", []) or [])
            calendars = [calendar_widget for calendar_widget in calendars if calendar_widget is not None]

            if not calendars:
                return

            spacing = max(0, int(self.years_layout.spacing())) if hasattr(self, "years_layout") else 0
            available = self._available_years_inner_width()
            total_spacing = spacing * max(0, len(calendars) - 1)
            distributable_width = max(0, available - total_spacing)

            if distributable_width <= 0:
                return

            base_width = distributable_width // len(calendars)
            remainder = distributable_width % len(calendars)

            for index, calendar_widget in enumerate(calendars):
                target_width = base_width + (1 if index < remainder else 0)
                target_width = max(1, int(target_width))

                try:
                    current_width = int(calendar_widget.width())

                except Exception:
                    current_width = -1

                if current_width != target_width:
                    calendar_widget.setFixedWidth(target_width)

        except Exception as e:
            logger.error(f"Erro ao distribuir largura entre calendários anuais: {e}", exc_info=True)

    def _create_extra_year_calendar(self):
        try:
            extra_year_calendar = None

            while self._year_calendar_pool:
                candidate = self._year_calendar_pool.pop()

                if candidate is not None:
                    extra_year_calendar = candidate
                    break

            if extra_year_calendar is None:
                extra_year_calendar = YearCalendarWidget(self.years_container)
                extra_year_calendar.monthSelected.connect(self._on_year_month_selected)
                extra_year_calendar.monthDoubleClicked.connect(self._on_year_month_double_clicked)

            else:
                try:
                    extra_year_calendar.setParent(self.years_container)
                    extra_year_calendar.setVisible(True)

                except Exception:
                    pass

            extra_year_calendar.app = self.app
            extra_year_calendar.owner = self
            self._configure_year_calendar_widget(extra_year_calendar)
            extra_year_calendar.setFixedWidth(self._calendar_content_width)

            try:
                extra_year_calendar.setLocale(self.calendar.locale())

            except Exception:
                pass

            self.years_layout.addWidget(extra_year_calendar, 0, Qt.AlignLeft | Qt.AlignTop)
            self._extra_year_calendars.append(extra_year_calendar)

        except Exception as e:
            logger.error(f"Erro ao criar calendário anual extra: {e}", exc_info=True)

    def _configure_year_calendar_widget(self, year_calendar_widget):
        try:
            if year_calendar_widget is None:
                return

            hint = year_calendar_widget.minimumSizeHint()
            fallback = QSize(self._calendar_content_width, max(260, int(hint.height())))
            year_calendar_widget.setMinimumSize(hint.expandedTo(fallback))
            year_calendar_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        except Exception as e:
            logger.error(f"Erro ao configurar tamanho do calendário anual: {e}", exc_info=True)

    def _remove_last_extra_year_calendar(self):
        try:
            if not self._extra_year_calendars:
                return

            extra_year_calendar = self._extra_year_calendars.pop()

            try:
                self.years_layout.removeWidget(extra_year_calendar)

            except Exception:
                pass

            if extra_year_calendar is not None:
                try:
                    extra_year_calendar.setVisible(False)
                    extra_year_calendar.setParent(self)
                    self._year_calendar_pool.append(extra_year_calendar)

                except Exception:
                    extra_year_calendar.deleteLater()

        except Exception as e:
            logger.error(f"Erro ao remover calendário anual extra: {e}", exc_info=True)

    def _ensure_year_calendar_count(self, target_count: int):
        try:
            target_count = max(1, int(target_count))
            current_count = 1 + len(self._extra_year_calendars)
            changed = False

            while current_count < target_count:
                self._create_extra_year_calendar()
                current_count += 1
                changed = True

            while current_count > target_count:
                self._remove_last_extra_year_calendar()
                current_count -= 1
                changed = True

            return changed

        except Exception as e:
            logger.error(f"Erro ao ajustar quantidade de calendários anuais: {e}", exc_info=True)
            return False

    def _reconcile_year_calendar_count(self, target_count: int, sync_after_change: bool = True) -> bool:
        try:
            current_count = 1 + len(self._extra_year_calendars)
            count_changed = False

            if int(target_count) != int(current_count):
                self.years_container.setUpdatesEnabled(False)

                try:
                    count_changed = self._ensure_year_calendar_count(target_count)

                finally:
                    self.years_container.setUpdatesEnabled(True)

            if count_changed and not sync_after_change:
                self._year_sync_pending = True
                return True

            should_sync = bool(sync_after_change and (count_changed or self._year_sync_pending))

            if should_sync:
                self._sync_year_calendar_pages_from_primary()
                self._sync_year_calendars_visual_data()
                self._year_sync_pending = False

            return bool(count_changed)

        except Exception as e:
            logger.error(f"Erro ao reconciliar quantidade dos calendários anuais: {e}", exc_info=True)
            return False

    def _update_year_calendars_for_width(self):
        try:
            if not self._is_year_view_active():
                return

            target_count = self._desired_year_calendar_count()
            self._reconcile_year_calendar_count(target_count, sync_after_change=True)
            self._apply_year_calendar_width_distribution()

        except Exception as e:
            logger.error(f"Erro ao atualizar calendários anuais por largura: {e}", exc_info=True)

    def _on_primary_calendar_selection_changed(self):
        try:
            if self._syncing_month_calendars:
                return

            selected = self.calendar.selectedDate()

            if isinstance(selected, QDate) and selected.isValid():
                self._selected_reference_date = selected

            self._sync_month_calendar_pages_from_primary()
            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao processar seleção no calendário principal: {e}", exc_info=True)

    def _on_primary_calendar_page_changed(self, year: int, month: int):
        try:
            if self._syncing_month_calendars:
                return

            selected = self.calendar.selectedDate()
            day = selected.day() if selected.isValid() else 1
            max_day = QDate(year, month, 1).daysInMonth()
            target_date = QDate(year, month, min(max(day, 1), max_day))

            if selected != target_date:
                self.calendar.setSelectedDate(target_date)
                return

            self._sync_month_calendar_pages_from_primary()
            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao processar mudança de mês no calendário principal: {e}", exc_info=True)

    def _on_extra_calendar_selection_changed(self, calendar_widget):
        try:
            if self._syncing_month_calendars:
                return

            if calendar_widget is None:
                return

            selected = calendar_widget.selectedDate()

            if not isinstance(selected, QDate) or not selected.isValid():
                return

            self._selected_reference_date = selected

            try:
                self.year_calendar.setSelectedDate(selected)

            except Exception:
                pass

            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao processar seleção em calendário mensal extra: {e}", exc_info=True)

    def _on_extra_calendar_page_changed(self, calendar_widget, year: int, month: int):
        try:
            if self._syncing_month_calendars:
                return

            if calendar_widget is None:
                return

            selected = calendar_widget.selectedDate()

            if isinstance(selected, QDate) and selected.isValid():
                self._selected_reference_date = selected

                try:
                    self.year_calendar.setSelectedDate(selected)

                except Exception:
                    pass

            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao processar navegação em calendário mensal extra: {e}", exc_info=True)

    def _sync_month_calendar_pages_from_primary(self):
        try:
            if self._syncing_month_calendars:
                return

            if not self._extra_month_calendars:
                return

            base_date = self.calendar.selectedDate()

            if not isinstance(base_date, QDate) or not base_date.isValid():
                base_date = QDate.currentDate()

            base_anchor = QDate(base_date.year(), base_date.month(), 1)
            preserved_days = {}

            for extra_calendar in self._extra_month_calendars:
                try:
                    selected = extra_calendar.selectedDate()

                    if isinstance(selected, QDate) and selected.isValid():
                        preserved_days[extra_calendar] = int(selected.day())

                except Exception:
                    pass

            self._syncing_month_calendars = True

            try:
                for idx, extra_calendar in enumerate(self._extra_month_calendars, start=1):
                    month_anchor = base_anchor.addMonths(idx)
                    extra_calendar.setCurrentPage(month_anchor.year(), month_anchor.month())
                    preferred_day = int(preserved_days.get(extra_calendar, 1))
                    max_day = month_anchor.daysInMonth()
                    target_day = max(1, min(preferred_day, max_day))
                    target_date = QDate(month_anchor.year(), month_anchor.month(), target_day)

                    try:
                        current_selected = extra_calendar.selectedDate()

                    except Exception:
                        current_selected = None

                    if target_date.isValid():
                        if not (isinstance(current_selected, QDate) and current_selected.isValid() and current_selected == target_date):
                            extra_calendar.setSelectedDate(target_date)

            finally:
                self._syncing_month_calendars = False

        except Exception as e:
            logger.error(f"Erro ao sincronizar meses dos calendários extras: {e}", exc_info=True)

    def _sync_month_calendars_visual_data(self):
        try:
            if not self._extra_month_calendars:
                self._extra_highlighted_dates = set()
                return

            task_counts = dict(getattr(self.calendar, "_task_counts", {}) or {})
            week_counts = dict(getattr(self.calendar, "_week_counts", {}) or {})
            month_counts = dict(getattr(self.calendar, "_month_counts", {}) or {})
            tooltip_map = dict(getattr(self.calendar, "_tasks_by_date", {}) or {})
            tasks_by_date_data = dict(getattr(self.calendar, "_tasks_by_date_data", {}) or {})

            for extra_calendar in self._extra_month_calendars:
                extra_calendar._task_counts = dict(task_counts)
                extra_calendar._week_counts = dict(week_counts)
                extra_calendar._month_counts = dict(month_counts)
                extra_calendar.set_task_tooltip_map(tooltip_map)
                extra_calendar.set_tasks_by_date_data(tasks_by_date_data)
                extra_calendar.updateCells()

            new_dates = set(getattr(self, "_highlighted_dates", set()) or set())
            to_clear = self._extra_highlighted_dates - new_dates

            if to_clear:
                blank = QTextCharFormat()

                for ds in to_clear:
                    qd = QDate.fromString(ds, Qt.ISODate)

                    if qd.isValid():
                        for extra_calendar in self._extra_month_calendars:
                            extra_calendar.setDateTextFormat(qd, blank)

            fmt = QTextCharFormat()
            pal = self.palette()
            base = pal.highlight().color()
            color = QColor(base.red(), base.green(), base.blue(), 60)
            fmt.setBackground(QBrush(color))
            fmt.setFontWeight(QFont.Bold)

            for ds in new_dates:
                qd = QDate.fromString(ds, Qt.ISODate)

                if qd.isValid():
                    for extra_calendar in self._extra_month_calendars:
                        extra_calendar.setDateTextFormat(qd, fmt)

            self._extra_highlighted_dates = new_dates

        except Exception as e:
            logger.error(f"Erro ao sincronizar dados visuais dos calendários extras: {e}", exc_info=True)

    def _collect_tasks(self):
        try:
            return CalendarDialog._collect_tasks(self)

        except Exception as e:
            logger.error(f"Erro ao coletar tarefas: {e}", exc_info=True)

    def update_task_list(self):
        try:
            result = CalendarDialog.update_task_list(self)
            self._sync_year_calendar_counts()
            self._sync_month_calendars_visual_data()
            return result

        except Exception as e:
            logger.error(f"Erro ao atualizar lista de tarefas: {e}", exc_info=True)

    def _update_badge_counts(self):
        try:
            return CalendarDialog._update_badge_counts(self)

        except Exception as e:
            logger.error(f"Erro ao atualizar contadores de badges: {e}", exc_info=True)

    def _get_task_dates(self):
        try:
            return CalendarDialog._get_task_dates(self)

        except Exception as e:
            logger.error(f"Erro ao obter datas de tarefas: {e}", exc_info=True)

    def _apply_highlighted_dates(self):
        try:
            return CalendarDialog._apply_highlighted_dates(self)

        except Exception as e:
            logger.error(f"Erro ao aplicar datas destacadas: {e}", exc_info=True)

    def _on_language_changed(self):
        try:
            self.filter_label.setText(get_text("Exibir por"))
            self.filter_combo.setItemText(0, get_text("Dia"))
            self.filter_combo.setItemText(1, get_text("Semana"))
            self.filter_combo.setItemText(2, get_text("Mês"))
            self.filter_combo.setItemText(3, get_text("Ano"))

            try:
                self.tasks_label.setText(get_text("Lista Global de Tarefas:"))

            except Exception:
                pass

            try:
                if hasattr(self, "show_priority_checkbox"):
                    self.show_priority_checkbox.setText(get_text("Mostrar prioridade"))

            except Exception:
                pass

            self._date_format = self.app.date_input.displayFormat() if hasattr(self.app, "date_input") else self._date_format
            self._apply_locale_to_calendar()
            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao atualizar idioma do painel de calendário: {e}", exc_info=True)

    def _apply_locale_to_calendar(self):
        try:
            result = CalendarDialog._apply_locale_to_calendar(self)

            for extra_calendar in list(getattr(self, "_extra_month_calendars", []) or []):
                try:
                    extra_calendar.setLocale(self.calendar.locale())
                    extra_calendar.setFirstDayOfWeek(Qt.Sunday)

                except Exception:
                    pass

            try:
                self.year_calendar.setLocale(self.calendar.locale())

            except Exception:
                pass

            for extra_year_calendar in list(getattr(self, "_extra_year_calendars", []) or []):
                try:
                    extra_year_calendar.setLocale(self.calendar.locale())

                except Exception:
                    pass

            return result

        except Exception as e:
            logger.error(f"Erro ao aplicar locale ao calendário: {e}", exc_info=True)

    def _on_filter_mode_changed(self):
        try:
            mode = self.filter_combo.currentData()

            if mode == "month":
                self.set_calendar_view_mode("year")

            elif mode == "year":
                self.set_calendar_view_mode("year")

            else:
                self.set_calendar_view_mode("month")

            self.month_view_toggle_visibility_changed.emit(mode == "month")

            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao alternar modo de filtro do calendário: {e}", exc_info=True)

    def _on_year_month_selected(self, qdate):
        try:
            if self._syncing_year_calendars:
                return

            if isinstance(qdate, QDate) and qdate.isValid():
                sender_widget = self.sender()
                current_day = self.calendar.selectedDate().day()
                max_day = qdate.daysInMonth()
                selected = QDate(qdate.year(), qdate.month(), min(current_day, max_day))
                self._selected_reference_date = selected

                if sender_widget is self.year_calendar:
                    self.calendar.setSelectedDate(selected)
                    self.year_calendar.setSelectedDate(selected)
                    self._sync_year_calendar_pages_from_primary()

            if self.filter_combo.currentData() in {"year", "month"}:
                self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao selecionar mês no calendário anual: {e}", exc_info=True)

    def _on_year_month_double_clicked(self, qdate):
        try:
            if isinstance(qdate, QDate) and qdate.isValid():
                self._selected_reference_date = qdate

            if self.filter_combo.currentData() == "month":
                self.set_calendar_view_mode("month")

        except Exception as e:
            logger.error(f"Erro ao abrir calendário mensal por duplo clique no calendário anual: {e}", exc_info=True)

    def _sync_year_calendar_counts(self):
        try:
            month_counts = getattr(self.calendar, "_month_counts", {}) or {}
            current_counts = dict(getattr(self.year_calendar, "_month_counts", {}) or {})

            if current_counts != dict(month_counts):
                self.year_calendar.set_month_counts(month_counts)

            selected = self.calendar.selectedDate()

            try:
                current_selected = self.year_calendar.selectedDate()

            except Exception:
                current_selected = None

            if isinstance(selected, QDate) and selected.isValid():
                if not (isinstance(current_selected, QDate) and current_selected.isValid() and current_selected.year() == selected.year() and current_selected.month() == selected.month()):
                    self.year_calendar.setSelectedDate(selected)

            self._sync_year_calendar_pages_from_primary()
            self._sync_year_calendars_visual_data()

        except Exception as e:
            logger.error(f"Erro ao sincronizar contagens no calendário anual: {e}", exc_info=True)

    def _sync_year_calendar_pages_from_primary(self):
        try:
            if self._syncing_year_calendars:
                return

            if not self._extra_year_calendars:
                return

            base_date = self.year_calendar.selectedDate()

            if not isinstance(base_date, QDate) or not base_date.isValid():
                base_date = self.calendar.selectedDate()

            if not isinstance(base_date, QDate) or not base_date.isValid():
                base_date = QDate.currentDate()

            self._syncing_year_calendars = True

            try:
                for idx, extra_year_calendar in enumerate(self._extra_year_calendars, start=1):
                    target_year = int(base_date.year()) + idx
                    target_month = int(base_date.month())

                    try:
                        extra_selected = extra_year_calendar.selectedDate()

                        if isinstance(extra_selected, QDate) and extra_selected.isValid():
                            target_month = int(extra_selected.month())

                    except Exception:
                        pass

                    target_month = max(1, min(12, target_month))
                    selected_date = QDate(target_year, target_month, 1)

                    if selected_date.isValid():
                        try:
                            current_selected = extra_year_calendar.selectedDate()

                        except Exception:
                            current_selected = None

                        if not (isinstance(current_selected, QDate) and current_selected.isValid() and current_selected.year() == selected_date.year() and current_selected.month() == selected_date.month()):
                            extra_year_calendar.setSelectedDate(selected_date)

            finally:
                self._syncing_year_calendars = False

        except Exception as e:
            logger.error(f"Erro ao sincronizar anos dos calendários anuais extras: {e}", exc_info=True)

    def _sync_year_calendars_visual_data(self):
        try:
            if not self._extra_year_calendars:
                return

            month_counts = dict(getattr(self.year_calendar, "_month_counts", {}) or {})
            month_tooltips = dict(getattr(self.year_calendar, "_month_tooltips", {}) or {})

            for extra_year_calendar in self._extra_year_calendars:
                try:
                    if hasattr(extra_year_calendar, "set_month_data"):
                        extra_year_calendar.set_month_data(month_counts, month_tooltips)

                    else:
                        extra_year_calendar.set_month_counts(month_counts)
                        extra_year_calendar.set_month_tooltip_map(month_tooltips)

                except Exception:
                    pass

        except Exception as e:
            logger.error(f"Erro ao sincronizar dados visuais dos calendários anuais extras: {e}", exc_info=True)

    def get_filter_reference_date(self):
        try:
            if self.filter_combo.currentData() == "year":
                if isinstance(self._selected_reference_date, QDate) and self._selected_reference_date.isValid():
                    return self._selected_reference_date

                return self.year_calendar.selectedDate()

            if self.filter_combo.currentData() == "month" and self._calendar_view_mode == "year":
                if isinstance(self._selected_reference_date, QDate) and self._selected_reference_date.isValid():
                    return self._selected_reference_date

                return self.year_calendar.selectedDate()

        except Exception:
            pass

        try:
            if isinstance(self._selected_reference_date, QDate) and self._selected_reference_date.isValid():
                return self._selected_reference_date

        except Exception:
            pass

        return self.calendar.selectedDate()

    def set_calendar_view_mode(self, mode):
        try:
            target_mode = "year" if mode == "year" else "month"

            if target_mode == "year":
                self.year_calendar.setSelectedDate(self.calendar.selectedDate())
                self.calendar_stack.setCurrentWidget(self.years_container)
                self._update_year_calendars_for_width()

            else:
                try:
                    if hasattr(self, "_year_resize_timer") and self._year_resize_timer is not None:
                        self._year_resize_timer.stop()

                except Exception:
                    pass

                target_date = self.year_calendar.selectedDate()

                try:
                    if self.filter_combo.currentData() == "month" and isinstance(self._selected_reference_date, QDate) and self._selected_reference_date.isValid():
                        target_date = self._selected_reference_date

                except Exception:
                    pass

                self.calendar.setSelectedDate(target_date)
                self.calendar_stack.setCurrentWidget(self.months_container)
                self._update_month_calendars_for_width()

            self._calendar_view_mode = target_mode
            self.month_view_mode_changed.emit(target_mode)

        except Exception as e:
            logger.error(f"Erro ao definir modo de visualização do calendário: {e}", exc_info=True)

    def toggle_month_filter_view_mode(self):
        try:
            if self.filter_combo.currentData() != "month":
                return

            if self._calendar_view_mode == "year":
                self.set_calendar_view_mode("month")

            else:
                self.set_calendar_view_mode("year")

            self.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao alternar visualização anual/mensal no filtro Mês: {e}", exc_info=True)

    def is_month_filter_active(self):
        try:
            return self.filter_combo.currentData() == "month"

        except Exception:
            return False

    def calendar_view_mode(self):
        try:
            return self._calendar_view_mode

        except Exception:
            return "month"
