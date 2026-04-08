import os
import subprocess
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QCoreApplication, QDate, QLocale
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QDateEdit, QCheckBox, QFrame, QTabWidget
from .svc_11_CustomTimeEdit import CustomTimeEdit
from .svc_12_DragDropTaskList import DragDropTaskList
from .svc_13_FileDropLineEdit import FileDropLineEdit
from .svc_14_palette_theme_sync import install_palette_theme_sync
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def _compute_widget_height(app, widget, name: str | None = None) -> int:
    try:
        if hasattr(app, "widget_heights") and isinstance(app.widget_heights, dict) and name in app.widget_heights:
            v = int(app.widget_heights.get(name) or 0)
            if v > 0:
                return v

        if hasattr(app, "widget_height_override") and isinstance(app.widget_height_override, int) and app.widget_height_override > 0:
            return int(app.widget_height_override)

        fm = widget.fontMetrics()
        return max(26, int(fm.height() * 1.2))

    except Exception:
        return 28

def _apply_widget_min_height(app, widget, name: str | None = None):
    try:
        h = _compute_widget_height(app, widget, name)
        widget.setMinimumHeight(h)

    except Exception:
        pass

def init_ui(app):
    app.main_layout = QVBoxLayout()
    input_layout_row1 = QHBoxLayout()
    input_layout_row2 = QHBoxLayout()

    input_layout_row2.setAlignment(Qt.AlignLeft)

    app.task_input = FileDropLineEdit(app, app)
    app.task_input.setPlaceholderText(get_text("Adicione uma tarefa..."))

    try:
        _apply_widget_min_height(app, app.task_input, "task_input")

    except Exception:
        app.task_input.setMinimumHeight(28)

    input_layout_row1.addWidget(app.task_input)

    app.date_checkbox = QCheckBox(get_text("Vincular data"))
    app.date_checkbox.setChecked(True)
    input_layout_row2.addWidget(app.date_checkbox)

    app.date_input = QDateEdit(app)
    app.date_input.setCalendarPopup(True)
    app.date_input.setDate(QDate.currentDate())
    _apply_widget_min_height(app, app.date_input, "date_input")

    def _apply_locale_to_date_input():
        locale = QLocale.system()
        try:
            if hasattr(app, "gerenciador_traducao"):
                idioma = app.gerenciador_traducao.obter_idioma_atual()
                if idioma and idioma.startswith("pt"):
                    locale = QLocale(QLocale.Portuguese, QLocale.Brazil)

                elif idioma and idioma.startswith("en"):
                    locale = QLocale(QLocale.English, QLocale.UnitedStates)

        except Exception as e:
            logger.error(f"Erro ao aplicar locale à data: {e}", exc_info=True)
            locale = QLocale.system()

        app.date_input.setLocale(locale)

        try:
            fmt = locale.dateFormat(QLocale.ShortFormat)

        except Exception as e:
            logger.error(f"Erro ao obter formato de data: {e}", exc_info=True)
            fmt = "dd/MM/yyyy"

        try:
            import re
            fmt = re.sub(r'(?<!y)yy(?!y)', 'yyyy', fmt)

        except Exception as e:
            logger.error(f"Erro ao ajustar formato de data: {e}", exc_info=True)

        app.date_input.setDisplayFormat(fmt)

    _apply_locale_to_date_input()

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: _apply_locale_to_date_input())

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de idioma_alterado para data: {e}", exc_info=True)

    input_layout_row2.addWidget(app.date_input)

    app.time_checkbox = QCheckBox(get_text("Vincular horário"))
    app.time_checkbox.setChecked(True)
    input_layout_row2.addWidget(app.time_checkbox)

    app.time_input = CustomTimeEdit(app)
    app.time_input.setDisplayFormat("HH:mm")
    app.time_input.setEnabled(True)
    _apply_widget_min_height(app, app.time_input, "time_input")
    input_layout_row2.addWidget(app.time_input)

    def _apply_locale_to_time_input():
        try:
            app.time_input.setDisplayFormat("HH:mm")

        except Exception as e:
            logger.error(f"Erro ao aplicar locale ao horário: {e}", exc_info=True)

    _apply_locale_to_time_input()

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: _apply_locale_to_time_input())
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: app.time_checkbox.setText(get_text("Vincular horário")))

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de idioma_alterado para horário: {e}", exc_info=True)

    def _on_time_checkbox_toggled(checked: bool):
        try:
            app.time_input.setEnabled(checked and app.date_checkbox.isChecked())

        except Exception as e:
            logger.error(f"Erro ao alternar checkbox de horário: {e}", exc_info=True)

    def _on_date_checkbox_toggled(checked: bool):
        try:
            app.time_checkbox.setEnabled(checked)
            app.time_input.setEnabled(checked and app.time_checkbox.isChecked())
            if not checked:
                app.time_checkbox.setChecked(False)

        except Exception as e:
            logger.error(f"Erro ao alternar checkbox de data: {e}", exc_info=True)

    app.time_checkbox.toggled.connect(_on_time_checkbox_toggled)
    app.date_checkbox.toggled.connect(_on_date_checkbox_toggled)
    app.time_checkbox.setEnabled(app.date_checkbox.isChecked())

    app.quadrant_selector = QComboBox(app)
    app.quadrant_selector.addItems([
        get_text("🔴 Importante e Urgente"),
        get_text("🟠 Importante, mas Não Urgente"),
        get_text("🟡 Não Importante, mas Urgente"),
        get_text("🟢 Não Importante e Não Urgente")
    ])
    app.quadrant_selector_label = QLabel(get_text("Prioridade"))

    try:
        _apply_widget_min_height(app, app.quadrant_selector_label, "quadrant_selector_label")

    except Exception:
        pass

    input_layout_row2.addWidget(app.quadrant_selector_label)
    input_layout_row2.addWidget(app.quadrant_selector)

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: app.quadrant_selector_label.setText(get_text("Prioridade")))

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de idioma_alterado para rótulo Prioridade: {e}", exc_info=True)

    app.add_button = QPushButton(get_text("Adicionar Tarefa"))
    add_icon_path = get_icon_path("organizador.png")
    if add_icon_path:
        app.add_button.setIcon(QIcon(add_icon_path))

    app.add_button.clicked.connect(app.add_task)
    input_layout_row1.addWidget(app.add_button)

    app.calendar_button = QPushButton(get_text("Calendário"))
    add_icon_path = get_icon_path("calendar.png")
    if add_icon_path:
        app.calendar_button.setIcon(QIcon(add_icon_path))

    app.calendar_button.clicked.connect(app.open_calendar)
    input_layout_row1.addWidget(app.calendar_button)

    app.main_layout.addLayout(input_layout_row1)
    app.main_layout.addLayout(input_layout_row2)

    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    app.main_layout.addWidget(separator)

    app.quadrant1_label = QLabel(get_text("🔴 Importante e Urgente"))
    app.quadrant1_list = DragDropTaskList(app, is_completed_list=False)
    app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))
    app.quadrant1_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant1_completed_list = DragDropTaskList(app, is_completed_list=True)
    app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))

    app.quadrant2_label = QLabel(get_text("🟠 Importante, mas Não Urgente"))
    app.quadrant2_list = DragDropTaskList(app, is_completed_list=False)
    app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))
    app.quadrant2_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant2_completed_list = DragDropTaskList(app, is_completed_list=True)
    app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))

    app.quadrant3_label = QLabel(get_text("🟡 Não Importante, mas Urgente"))
    app.quadrant3_list = DragDropTaskList(app, is_completed_list=False)
    app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))
    app.quadrant3_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant3_completed_list = DragDropTaskList(app, is_completed_list=True)
    app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))

    app.quadrant4_label = QLabel(get_text("🟢 Não Importante e Não Urgente"))
    app.quadrant4_list = DragDropTaskList(app, is_completed_list=False)
    app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))
    app.quadrant4_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant4_completed_list = DragDropTaskList(app, is_completed_list=True)
    app.add_placeholder(app.quadrant4_completed_list, get_text("Nenhuma Tarefa Concluída"))

    class _AutoOpenTabWidget(QTabWidget):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self._owner = owner
            self.setAcceptDrops(True)

        def dragEnterEvent(self, event):
            try:
                event.acceptProposedAction()

            except Exception:
                pass

        def dragMoveEvent(self, event):
            try:
                tb = self.tabBar()
                pos = tb.mapFrom(self, event.pos())
                idx = tb.tabAt(pos)

                if idx is not None and idx >= 0 and idx != self.currentIndex():
                    self.setCurrentIndex(idx)

                event.acceptProposedAction()

            except Exception:
                try:
                    super().dragMoveEvent(event)

                except Exception:
                    pass

        def dropEvent(self, event):
            try:
                tb = self.tabBar()
                pos = tb.mapFrom(self, event.pos())
                idx = tb.tabAt(pos)

                if idx is not None and idx >= 0:
                    self.setCurrentIndex(idx)

                    try:
                        from source.modules.eisenhower.services.svc_12_DragDropTaskList import DragDropTaskList

                        source_list = event.source()
                        source_is_completed = False

                        if isinstance(source_list, DragDropTaskList):
                            source_is_completed = bool(getattr(source_list, "_is_completed_list", False))

                        targets = (
                            (self._owner.quadrant1_list, self._owner.quadrant1_completed_list),
                            (self._owner.quadrant2_list, self._owner.quadrant2_completed_list),
                            (self._owner.quadrant3_list, self._owner.quadrant3_completed_list),
                            (self._owner.quadrant4_list, self._owner.quadrant4_completed_list),
                        )
                        if 0 <= idx < len(targets):
                            target_list = targets[idx][1 if source_is_completed else 0]

                        else:
                            target_list = None

                        if isinstance(source_list, DragDropTaskList) and target_list is not None:
                            if source_list is target_list:
                                event.acceptProposedAction()
                                return

                            items = list(source_list.selectedItems() or [])

                            if not items and source_list.currentItem() is not None:
                                items = [source_list.currentItem()]

                            if not items:
                                event.ignore()
                                return

                            target_is_completed = bool(getattr(target_list, "_is_completed_list", False))
                            new_state = Qt.Checked if target_is_completed else Qt.Unchecked

                            source_list.blockSignals(True)
                            target_list.blockSignals(True)

                            try:
                                for it in items:
                                    if it and (it.flags() & Qt.ItemIsSelectable):
                                        self._owner.move_item_between_lists(it, source_list, target_list, new_state)

                            finally:
                                source_list.blockSignals(False)
                                target_list.blockSignals(False)

                            try:
                                source_list.clearSelection()

                            except Exception:
                                pass

                            try:
                                if hasattr(self._owner, "save_tasks"):
                                    self._owner.save_tasks()

                                if hasattr(self._owner, "calendar_pane") and self._owner.calendar_pane:
                                    self._owner.calendar_pane.calendar_panel.update_task_list()

                            except Exception:
                                pass

                            event.acceptProposedAction()
                            return

                    except Exception:
                        pass

                event.ignore()

            except Exception:
                try:
                    super().dropEvent(event)

                except Exception:
                    pass

    tabs = _AutoOpenTabWidget(app)
    app.quadrant_tabs = tabs

    def _make_tab(label_widget, list_widget, completed_label_widget, completed_list_widget):
        tab = QWidget()
        l = QVBoxLayout()
        l.addWidget(label_widget)
        l.addWidget(list_widget)
        l.addWidget(completed_label_widget)
        l.addWidget(completed_list_widget)
        tab.setLayout(l)
        return tab

    tabs.addTab(_make_tab(app.quadrant1_label, app.quadrant1_list, app.quadrant1_completed_label, app.quadrant1_completed_list), get_text("🔴 Importante e Urgente"))
    tabs.addTab(_make_tab(app.quadrant2_label, app.quadrant2_list, app.quadrant2_completed_label, app.quadrant2_completed_list), get_text("🟠 Importante, mas Não Urgente"))
    tabs.addTab(_make_tab(app.quadrant3_label, app.quadrant3_list, app.quadrant3_completed_label, app.quadrant3_completed_list), get_text("🟡 Não Importante, mas Urgente"))
    tabs.addTab(_make_tab(app.quadrant4_label, app.quadrant4_list, app.quadrant4_completed_label, app.quadrant4_completed_list), get_text("🟢 Não Importante e Não Urgente"))

    app.main_layout.addWidget(tabs)

    container = QWidget()
    container.setLayout(app.main_layout)

    if hasattr(app, "setCentralWidget"):
        app.setCentralWidget(container)

    else:
        app._root_widget = container

    def _open_linked_file(app, item):
        try:
            if item is None:
                return

            data = item.data(Qt.UserRole) or {}
            path = data.get("file_path")
            if not path:
                return

            if os.path.exists(path):
                try:
                    if os.name == 'nt':
                        os.startfile(path)

                    else:
                        subprocess.Popen(["xdg-open", path])

                except Exception:
                    try:
                        subprocess.Popen([path], shell=True)

                    except Exception:
                        pass

            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(app, get_text("Erro"), get_text("Arquivo não encontrado."))

        except Exception as e:
            logger.error(f"Erro ao abrir arquivo vinculado: {e}", exc_info=True)

    app.quadrant1_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant1_list, app.quadrant1_completed_list))
    app.quadrant2_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant2_list, app.quadrant2_completed_list))
    app.quadrant3_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant3_list, app.quadrant3_completed_list))
    app.quadrant4_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant4_list, app.quadrant4_completed_list))

    app.quadrant1_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant1_completed_list, app.quadrant1_list))
    app.quadrant2_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant2_completed_list, app.quadrant2_list))
    app.quadrant3_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant3_completed_list, app.quadrant3_list))
    app.quadrant4_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant4_completed_list, app.quadrant4_list))

    for lst in (
        app.quadrant1_list, app.quadrant2_list, app.quadrant3_list, app.quadrant4_list,
        app.quadrant1_completed_list, app.quadrant2_completed_list, app.quadrant3_completed_list, app.quadrant4_completed_list
    ):
        lst.setContextMenuPolicy(Qt.CustomContextMenu)
        lst.customContextMenuRequested.connect(lambda point, l=lst: app.show_context_menu(point, l))

        try:
            lst.itemDoubleClicked.connect(lambda item, l=lst: _open_linked_file(app, item))

        except Exception:
            pass

    install_palette_theme_sync(app, logger)
