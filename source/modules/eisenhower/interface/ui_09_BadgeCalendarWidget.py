from PySide6.QtWidgets import QCalendarWidget
from PySide6.QtCore import QCoreApplication
from source.modules.eisenhower.interface.BadgeCalendarWidget import set_task_counts, paintCell, _draw_badge, _date_at_pos, event as badge_event
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class BadgeCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._task_counts = {}  # {date_iso_str: count}
        self._week_counts = {}  # {(year, week_number): count}
        self._month_counts = {}  # {(year, month): count}
        self._tasks_by_date = {}  # {date_iso_str: [lines]}
        self._tasks_by_date_data = {}  # {date_iso_str: [task dicts]}

        try:
            self.setMouseTracking(True)

        except Exception:
            pass

    def set_task_tooltip_map(self, tasks_by_date: dict):
        try:
            self._tasks_by_date = tasks_by_date or {}

        except Exception as e:
            logger.error(f"Erro ao definir mapa de tooltip do calendário: {e}", exc_info=True)

    def set_tasks_by_date_data(self, tasks_by_date_data: dict):
        try:
            self._tasks_by_date_data = tasks_by_date_data or {}

        except Exception as e:
            logger.error(f"Erro ao definir mapa de dados do calendário: {e}", exc_info=True)

    def set_task_counts(self, dates_list):
        return set_task_counts(self, dates_list)

    def paintCell(self, painter, rect, date):
        return paintCell(self, painter, rect, date)

    def _draw_badge(self, painter, rect, count):
        return _draw_badge(self, painter, rect, count)

    def _date_at_pos(self, pos):
        return _date_at_pos(self, pos)

    def event(self, qt_event):
        return badge_event(self, qt_event)
