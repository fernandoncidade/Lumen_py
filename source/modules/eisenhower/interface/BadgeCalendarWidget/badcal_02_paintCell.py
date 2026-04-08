from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCalendarWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def paintCell(self, painter, rect, date):
    try:
        QCalendarWidget.paintCell(self, painter, rect, date)

        date_iso = date.toString(Qt.ISODate)
        count = self._task_counts.get(date_iso, 0)

        if count > 0:
            self._draw_badge(painter, rect, count)

    except Exception as e:
        logger.error(f"Erro ao pintar célula do calendário: {e}", exc_info=True)
