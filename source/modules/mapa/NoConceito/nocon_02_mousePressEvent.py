from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mousePressEvent(self, event):
    try:
        self.setPen(QPen(QColor(255, 255, 255, 80), 3))
        QGraphicsEllipseItem.mousePressEvent(self, event)

    except Exception as e:
        logger.error(f"Erro no mousePressEvent: {str(e)}", exc_info=True)
