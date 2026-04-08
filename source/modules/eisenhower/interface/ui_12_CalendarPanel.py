from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QLabel, QAbstractItemView, QWidget, QSizePolicy, QCheckBox
from PySide6.QtCore import Qt, QDate, QCoreApplication, QSize
from .ui_08_LineEditFrame import LineEditFrame
from .ui_09_BadgeCalendarWidget import BadgeCalendarWidget
from .ui_10_CalendarDialog import CalendarDialog
from source.modules.eisenhower.interface.CalendarDialog import install_palette_theme_sync
from source.modules.eisenhower.services import show_context_menu
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class CalendarPanel(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        try:
            self.app = app
            self._date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"
            self._highlighted_dates = set()

            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(5, 1, 5, 9)
            main_layout.setSpacing(6)

            self.calendar = BadgeCalendarWidget(self)
            self.calendar.app = app
            self.calendar.owner = self
            initial_date = app.date_input.date() if hasattr(app, "date_input") else QDate.currentDate()
            self.calendar.setSelectedDate(initial_date)
            hint = self.calendar.minimumSizeHint()
            fallback = QSize(300, 260)
            self.calendar.setMinimumSize(hint.expandedTo(fallback))
            self.calendar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self._apply_locale_to_calendar()

            self.calendar_frame = LineEditFrame(self)
            self.calendar_frame.layout().addWidget(self.calendar)
            main_layout.addWidget(self.calendar_frame)

            controls_layout = QHBoxLayout()
            self.filter_label = QLabel(get_text("Exibir por"), self)
            controls_layout.addWidget(self.filter_label)

            self.filter_combo = QComboBox(self)
            self.filter_combo.addItem(get_text("Dia"), "day")
            self.filter_combo.addItem(get_text("Semana"), "week")
            self.filter_combo.addItem(get_text("Mês"), "month")
            controls_layout.addWidget(self.filter_combo)
            controls_layout.addStretch()
            self.show_priority_checkbox = QCheckBox(get_text("Mostrar prioridade"), self)
            self.show_priority_checkbox.setChecked(True)
            self.show_priority_checkbox.stateChanged.connect(self.update_task_list)
            controls_layout.addWidget(self.show_priority_checkbox)
            main_layout.addLayout(controls_layout)

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

            self.calendar.selectionChanged.connect(self.update_task_list)
            self.filter_combo.currentIndexChanged.connect(self.update_task_list)

            if hasattr(self.app, "gerenciador_traducao"):
                self.app.gerenciador_traducao.idioma_alterado.connect(self._on_language_changed)

            self.update_task_list()

            install_palette_theme_sync(self, logger)

        except Exception as e:
            logger.error(f"Erro ao inicializar CalendarPanel: {e}", exc_info=True)

    def _collect_tasks(self):
        try:
            return CalendarDialog._collect_tasks(self)

        except Exception as e:
            logger.error(f"Erro ao coletar tarefas: {e}", exc_info=True)

    def update_task_list(self):
        try:
            return CalendarDialog.update_task_list(self)

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
            return CalendarDialog._apply_locale_to_calendar(self)

        except Exception as e:
            logger.error(f"Erro ao aplicar locale ao calendário: {e}", exc_info=True)
