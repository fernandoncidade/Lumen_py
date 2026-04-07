from PySide6.QtGui import QPainterPath, QRegion
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_rounded_mask(self, widget, radius: int = 8):
    try:
        if widget is None:
            return

        rect = widget.rect()
        if rect.isEmpty():
            return

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        widget.setMask(region)

    except Exception as e:
        logger.error(f"Erro ao atualizar máscara arredondada: {str(e)}", exc_info=True)
