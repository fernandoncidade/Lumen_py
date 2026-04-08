from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QCalendarWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def paintCell(self, painter, rect, date):
    try:
        QCalendarWidget.paintCell(self, painter, rect, date)

        if date == QDate.currentDate() and date != self.selectedDate():
            painter.save()
            color = self.palette().highlight().color()
            color.setAlpha(210)
            pen = QPen(color, 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), 4, 4)
            painter.restore()

        date_iso = date.toString(Qt.ISODate)
        count = self._task_counts.get(date_iso, 0)

        if count > 0:
            self._draw_badge(painter, rect, count)

    except Exception as e:
        logger.error(f"Erro ao pintar célula do calendário: {e}", exc_info=True)
