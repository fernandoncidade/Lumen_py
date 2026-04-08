from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QToolButton, QLabel, QSizePolicy, QApplication, QMenu, QMessageBox
from PySide6.QtCore import Signal, QDate, QCoreApplication, Qt, QLocale, QEvent, QObject
from PySide6.QtGui import QAction
from source.modules.eisenhower.services.svc_06_EisenhowerContextMenuService import editar_tarefa_por_dados, remover_tarefa_por_dados
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class YearCalendarWidget(QWidget):
    monthSelected = Signal(QDate)
    monthDoubleClicked = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._locale = QLocale.system()
        self._year = QDate.currentDate().year()
        self._selected_month = QDate.currentDate().month()
        self._month_counts = {}
        self._month_tooltips = {}
        self._theme_sync_filter = None
        self._styling_in_progress = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)

        self.prev_year_button = QToolButton(self)
        self.prev_year_button.setText("<")
        self.prev_year_button.clicked.connect(lambda: self.setYear(self._year - 1))
        header_layout.addWidget(self.prev_year_button)

        self.year_label = QLabel(self)
        self.year_label.setAlignment(Qt.AlignCenter)
        self.year_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        header_layout.addWidget(self.year_label, 1)

        self.next_year_button = QToolButton(self)
        self.next_year_button.setText(">")
        self.next_year_button.clicked.connect(lambda: self.setYear(self._year + 1))
        header_layout.addWidget(self.next_year_button)

        main_layout.addLayout(header_layout)

        self.month_grid = QGridLayout()
        self.month_grid.setContentsMargins(0, 0, 0, 0)
        self.month_grid.setHorizontalSpacing(6)
        self.month_grid.setVerticalSpacing(6)
        main_layout.addLayout(self.month_grid)

        self._month_buttons = []

        for month in range(1, 13):
            button = QToolButton(self)
            button.setCheckable(True)
            button.setAutoExclusive(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumHeight(56)
            button.setProperty("month", month)
            button.installEventFilter(self)
            button.clicked.connect(lambda _=False, m=month: self._on_month_clicked(m))
            self._month_buttons.append(button)

            row = (month - 1) // 4
            col = (month - 1) % 4
            self.month_grid.addWidget(button, row, col)

        self._refresh_header()
        self._refresh_month_buttons()
        self._apply_palette_style()
        self._install_theme_sync()

    def setLocale(self, locale: QLocale):
        try:
            self._locale = locale if isinstance(locale, QLocale) else QLocale.system()
            self._refresh_month_buttons()

        except Exception as e:
            logger.error(f"Erro ao definir locale no calendário anual: {e}", exc_info=True)

    def setYear(self, year: int):
        try:
            self._year = int(year)
            self._refresh_header()
            self._refresh_month_buttons()
            self.monthSelected.emit(self.selectedDate())

        except Exception as e:
            logger.error(f"Erro ao definir ano no calendário anual: {e}", exc_info=True)

    def year(self) -> int:
        return int(self._year)

    def setSelectedDate(self, qdate: QDate):
        try:
            if isinstance(qdate, QDate) and qdate.isValid():
                self._year = qdate.year()
                self._selected_month = qdate.month()
                self._refresh_header()
                self._refresh_month_buttons()

        except Exception as e:
            logger.error(f"Erro ao definir data selecionada no calendário anual: {e}", exc_info=True)

    def selectedDate(self) -> QDate:
        return QDate(self._year, self._selected_month, 1)

    def set_month_counts(self, month_counts: dict):
        try:
            self._month_counts = dict(month_counts or {})
            self._refresh_month_buttons()

        except Exception as e:
            logger.error(f"Erro ao definir contagens mensais no calendário anual: {e}", exc_info=True)

    def set_month_tooltip_map(self, month_tooltips: dict):
        try:
            self._month_tooltips = dict(month_tooltips or {})
            self._refresh_month_buttons()

        except Exception as e:
            logger.error(f"Erro ao definir tooltips mensais no calendário anual: {e}", exc_info=True)

    def eventFilter(self, watched, event):
        try:
            if watched in self._month_buttons and event.type() == QEvent.ContextMenu:
                month = int(watched.property("month") or 0)

                if 1 <= month <= 12:
                    self._show_month_context_menu(month, watched, event)
                    return True

            if watched in self._month_buttons and event.type() == QEvent.MouseButtonDblClick:
                month = int(watched.property("month") or 0)

                if 1 <= month <= 12:
                    self._on_month_clicked(month)
                    self.monthDoubleClicked.emit(self.selectedDate())
                    return True

        except Exception as e:
            logger.error(f"Erro no eventFilter do calendário anual: {e}", exc_info=True)

        return super().eventFilter(watched, event)

    def changeEvent(self, event):
        try:
            tipos = {
                QEvent.PaletteChange,
                QEvent.ApplicationPaletteChange,
                QEvent.ThemeChange,
                QEvent.StyleChange,
            }

            try:
                tipos.add(QEvent.ColorSchemeChange)

            except AttributeError:
                pass

            if event.type() in tipos:
                self._apply_palette_style()

        except Exception as e:
            logger.error(f"Erro ao processar changeEvent no calendário anual: {e}", exc_info=True)

        super().changeEvent(event)

    def _month_tasks(self, month: int) -> list:
        tasks = []

        try:
            owner = getattr(self, "owner", None)

            if owner is None or not hasattr(owner, "_collect_tasks"):
                return tasks

            year = int(self._year)

            for task in owner._collect_tasks() or []:
                ds = (task or {}).get("date")
                if not ds:
                    continue

                qd = QDate.fromString(ds, Qt.ISODate)

                if not qd.isValid():
                    continue

                if qd.year() == year and qd.month() == int(month):
                    tasks.append(task)

            tasks.sort(key=lambda t: ((t.get("date") or ""), (t.get("time") or ""), (t.get("text") or "").lower()))

        except Exception as e:
            logger.error(f"Erro ao coletar tarefas do mês no calendário anual: {e}", exc_info=True)

        return tasks

    def _format_task_label(self, task: dict, show_priority: bool) -> str:
        try:
            text = (task.get("text") or "").strip() or (get_text("(Sem título)") or "(Sem título)")
            date_str = task.get("date") or ""
            time_str = task.get("time") or ""
            emoji = ""

            if show_priority:
                try:
                    prio_label = prioridade_para_texto(task.get("priority"), getattr(self, "owner", None))

                    if prio_label:
                        cand = str(prio_label).strip()[:1]

                        if cand in {"🔴", "🟠", "🟡", "🟢"}:
                            emoji = cand

                except Exception:
                    emoji = ""

            if date_str:
                qd = QDate.fromString(date_str, Qt.ISODate)

                if qd.isValid():
                    date_fmt = "dd/MM/yyyy"

                    try:
                        owner = getattr(self, "owner", None)
                        date_fmt = getattr(owner, "_date_format", date_fmt) or date_fmt

                    except Exception:
                        pass

                    date_str = qd.toString(date_fmt)

            label = text

            if time_str:
                label = f"{date_str} {time_str} — {label}".strip()

            elif date_str:
                label = f"{date_str} — {label}".strip()

            if emoji:
                label = f"{emoji} {label}"

            return label

        except Exception:
            return (task.get("text") or "").strip() or (get_text("(Sem título)") or "(Sem título)")

    def _remove_all_tasks_for_month(self, month: int) -> int:
        try:
            app = getattr(self, "app", None)

            if app is None:
                return 0

            resp = QMessageBox.question(
                app,
                get_text("Remover Tarefas") or "Remover Tarefas",
                get_text("Deseja remover todas as tarefas do mês selecionado?") or "Deseja remover todas as tarefas do mês selecionado?",
                QMessageBox.Yes | QMessageBox.No,
            )

            if resp != QMessageBox.Yes:
                return 0

            removed = 0

            lists = [
                getattr(app, "quadrant1_list", None),
                getattr(app, "quadrant2_list", None),
                getattr(app, "quadrant3_list", None),
                getattr(app, "quadrant4_list", None),
                getattr(app, "quadrant1_completed_list", None),
                getattr(app, "quadrant2_completed_list", None),
                getattr(app, "quadrant3_completed_list", None),
                getattr(app, "quadrant4_completed_list", None),
            ]

            for lst in lists:
                if lst is None:
                    continue

                for i in range(lst.count() - 1, -1, -1):
                    it = lst.item(i)

                    if not it or not (it.flags() & Qt.ItemIsSelectable):
                        continue

                    data = it.data(Qt.UserRole) or {}
                    ds = (data.get("date") or "").strip()

                    if not ds:
                        continue

                    qd = QDate.fromString(ds, Qt.ISODate)

                    if not qd.isValid():
                        continue

                    if qd.year() == int(self._year) and qd.month() == int(month):
                        try:
                            lst.takeItem(i)
                            removed += 1

                        except Exception:
                            pass

            try:
                if hasattr(app, "cleanup_time_groups"):
                    for lst in lists:
                        if lst is not None:
                            app.cleanup_time_groups(lst)

            except Exception:
                pass

            try:
                if hasattr(app, "atualizar_placeholders"):
                    app.atualizar_placeholders()

            except Exception:
                pass

            try:
                app.save_tasks()

            except Exception:
                pass

            try:
                cp = getattr(app, "calendar_pane", None)

                if cp is not None and getattr(cp, "calendar_panel", None) is not None:
                    cp.calendar_panel.update_task_list()

            except Exception:
                pass

            return int(removed)

        except Exception as e:
            logger.error(f"Erro ao remover tarefas do mês no calendário anual: {e}", exc_info=True)
            return 0

    def _show_month_context_menu(self, month: int, watched, event):
        try:
            tasks = self._month_tasks(month)
            show_priority = True

            try:
                owner = getattr(self, "owner", None)

                if owner is not None and hasattr(owner, "show_priority_checkbox"):
                    show_priority = bool(owner.show_priority_checkbox.isChecked())

            except Exception:
                show_priority = True

            menu = QMenu(self)
            edit_menu = menu.addMenu(get_text("✏️ Editar Tarefa") or "✏️ Editar Tarefa")
            remove_menu = menu.addMenu(get_text("🗑️ Remover Tarefa") or "🗑️ Remover Tarefa")

            if tasks:
                app = getattr(self, "app", None)

                for task in tasks:
                    label = self._format_task_label(task, show_priority=show_priority)

                    act_edit = QAction(label, self)
                    act_edit.triggered.connect(lambda _=False, t=task: editar_tarefa_por_dados(app, t))
                    edit_menu.addAction(act_edit)

                    act_remove = QAction(label, self)
                    act_remove.triggered.connect(lambda _=False, t=task: remover_tarefa_por_dados(app, t, True))
                    remove_menu.addAction(act_remove)

                remove_menu.addSeparator()
                act_remove_all = QAction(get_text("Remover Todas") or "Remover Todas", self)
                act_remove_all.triggered.connect(lambda _=False, m=month: self._remove_all_tasks_for_month(m))
                remove_menu.addAction(act_remove_all)

            else:
                act_empty_edit = QAction(get_text("Nenhuma tarefa neste período."), self)
                act_empty_edit.setEnabled(False)
                edit_menu.addAction(act_empty_edit)

                act_empty_remove = QAction(get_text("Nenhuma tarefa neste período."), self)
                act_empty_remove.setEnabled(False)
                remove_menu.addAction(act_empty_remove)

            try:
                global_pos = event.globalPos()

            except Exception:
                pos = event.pos() if hasattr(event, "pos") else watched.rect().center()
                global_pos = watched.mapToGlobal(pos)

            menu.exec(global_pos)

        except Exception as e:
            logger.error(f"Erro ao exibir menu de contexto do mês no calendário anual: {e}", exc_info=True)

    def _on_month_clicked(self, month: int):
        try:
            self._selected_month = int(month)
            self._refresh_month_buttons()
            self.monthSelected.emit(self.selectedDate())

        except Exception as e:
            logger.error(f"Erro ao selecionar mês no calendário anual: {e}", exc_info=True)

    def _refresh_header(self):
        self.year_label.setText(str(self._year))

    def _refresh_month_buttons(self):
        for idx, button in enumerate(self._month_buttons, start=1):
            month_name = self._locale.standaloneMonthName(idx, QLocale.ShortFormat) or self._locale.monthName(idx, QLocale.ShortFormat)

            if not month_name:
                month_name = QDate(self._year, idx, 1).toString("MMM")

            count = int(self._month_counts.get((self._year, idx), 0) or 0)
            label = month_name.capitalize()

            if count > 0:
                label = f"{label}\n{count}"

            button.setText(label)
            button.setChecked(idx == self._selected_month)
            button.setProperty("hasTasks", count > 0)
            lines = self._month_tooltips.get((self._year, idx), []) or []

            if lines:
                button.setToolTip("\n".join(lines))

            else:
                button.setToolTip("")

            button.style().unpolish(button)
            button.style().polish(button)

    def _apply_palette_style(self):
        try:
            if self._styling_in_progress:
                return

            self._styling_in_progress = True
            pal = self.palette()
            base_color = pal.base().color()
            is_light_base = base_color.lightness() >= 128
            border_color = base_color.darker(135) if is_light_base else base_color.lighter(150)
            border = border_color.name()
            base_bg = base_color.name()
            text = pal.text().color().name()
            highlight = pal.highlight().color().name()
            highlight_text = pal.highlightedText().color().name()

            self.setStyleSheet(
                f"""
                QToolButton {{
                    border: 1px solid {border};
                    border-radius: 8px;
                    padding: 6px;
                    background: {base_bg};
                    color: {text};
                    font-weight: 600;
                }}
                QToolButton:hover {{
                    background: {base_bg};
                    border: 1px solid {highlight};
                }}
                QToolButton[hasTasks="true"] {{
                    border: 1px solid {highlight};
                }}
                QToolButton:checked {{
                    background: {highlight};
                    color: {highlight_text};
                }}
                """
            )

            for button in self._month_buttons:
                button.style().unpolish(button)
                button.style().polish(button)
                button.update()

        except Exception as e:
            logger.error(f"Erro ao aplicar estilo no calendário anual: {e}", exc_info=True)

        finally:
            self._styling_in_progress = False

    def _install_theme_sync(self):
        try:
            class _ThemeSyncFilter(QObject):
                def __init__(self, owner):
                    super().__init__(owner)
                    self.owner = owner

                def eventFilter(self, obj, event):
                    try:
                        qt_app = QApplication.instance()

                        if qt_app is None or obj is not qt_app:
                            return super().eventFilter(obj, event)

                        tipos = (
                            QEvent.ApplicationPaletteChange,
                            QEvent.ThemeChange,
                        )

                        try:
                            tipos = tipos + (QEvent.ColorSchemeChange,)

                        except AttributeError:
                            pass

                        if event.type() in tipos:
                            self.owner._apply_palette_style()

                    except Exception:
                        pass

                    return super().eventFilter(obj, event)

            qt_app = QApplication.instance()

            if qt_app is not None:
                self._theme_sync_filter = _ThemeSyncFilter(self)
                qt_app.installEventFilter(self._theme_sync_filter)

        except Exception as e:
            logger.error(f"Erro ao instalar sincronização de tema no calendário anual: {e}", exc_info=True)
