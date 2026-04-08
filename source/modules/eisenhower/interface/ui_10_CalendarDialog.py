from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QComboBox, QListWidget, QLabel, QAbstractItemView, QSizePolicy, QCheckBox
from PySide6.QtCore import Qt, QDate, QCoreApplication, QSize
from .ui_08_LineEditFrame import LineEditFrame
from .ui_09_BadgeCalendarWidget import BadgeCalendarWidget
from source.modules.eisenhower.services import show_context_menu
from source.modules.eisenhower.interface.CalendarDialog import (
    closeEvent as _caldial_closeEvent,
    _open_linked_file as _caldial_open_linked_file,
    _collect_tasks as _caldial_collect_tasks,
    update_task_list as _caldial_update_task_list,
    _update_badge_counts as _caldial_update_badge_counts,
    _on_language_changed as _caldial_on_language_changed,
    _apply_locale_to_calendar as _caldial_apply_locale_to_calendar,
    _get_task_dates as _caldial_get_task_dates,
    _apply_highlighted_dates as _caldial_apply_highlighted_dates,
    install_palette_theme_sync
)
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class CalendarDialog(QDialog):
    def __init__(self, app):
        super().__init__(app)
        try:
            self.app = app
            self.setModal(True)
            self.setWindowTitle(get_text("Calendário de Tarefas"))
            self._date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"
            self._highlighted_dates = set()

            main_layout = QVBoxLayout(self)

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
                self.tasks_list.itemDoubleClicked.connect(self._open_linked_file)

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
            logger.error(f"Erro ao inicializar CalendarDialog: {e}", exc_info=True)

    def closeEvent(self, event):
        return _caldial_closeEvent(self, event)

    def _open_linked_file(self, item):
        return _caldial_open_linked_file(self, item)

    def _collect_tasks(self):
        return _caldial_collect_tasks(self)

    def update_task_list(self):
        return _caldial_update_task_list(self)

    def _update_badge_counts(self):
        return _caldial_update_badge_counts(self)

    def _on_language_changed(self):
        return _caldial_on_language_changed(self)

    def _apply_locale_to_calendar(self):
        return _caldial_apply_locale_to_calendar(self)

    def _get_task_dates(self):
        return _caldial_get_task_dates(self)

    def _apply_highlighted_dates(self):
        return _caldial_apply_highlighted_dates(self)
