from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from source.utils.LogManager import LogManager
from source.utils.EventBus import get_event_bus
from source.modules.mapa.NoConceito import itemChange, mousePressEvent, mouseReleaseEvent, mouseDoubleClickEvent


class NoConceito(QGraphicsEllipseItem):
    def __init__(self, x, y, texto, cor=QColor("#0078d4")):
        super().__init__(-60, -40, 120, 80)
        self.logger = LogManager.get_logger()
        try:
            self.setPos(x, y)
            self.setBrush(QBrush(QColor(cor.red(), cor.green(), cor.blue(), 185)))
            self.setPen(QPen(QColor(255, 255, 255, 28), 2))
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(18)
            shadow.setOffset(0, 3)
            shadow.setColor(QColor(0, 0, 0, 140))
            self.setGraphicsEffect(shadow)

            self.texto_item = QGraphicsTextItem(texto, self)
            self.texto_item.setDefaultTextColor(QColor(245, 245, 245))
            fonte = QFont("Segoe UI", 11, QFont.Bold)
            self.texto_item.setFont(fonte)
            rect = self.texto_item.boundingRect()
            self.texto_item.setPos(-rect.width()/2, -rect.height()/2)

            self._badge = QGraphicsEllipseItem(-4, -34, 8, 8, self)
            self._badge.setBrush(QBrush(QColor("#ffb900")))
            self._badge.setPen(QPen(Qt.NoPen))
            self._badge.setVisible(False)

            self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
            self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
            self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)

            self.conexoes = []
            self.texto = texto
            self.cor = cor
            self.notas = ""
            self.info_associada: list[str] = []

            self.event_bus = get_event_bus()

        except Exception as e:
            self.logger.error(f"Erro ao inicializar NoConceito: {str(e)}", exc_info=True)

    def itemChange(self, change, value):
        return itemChange(self, change, value)

    def mousePressEvent(self, event):
        return mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        return mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        return mouseDoubleClickEvent(self, event)
