from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen


class MapaScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_step = 40
        self._grid_pen_light = QPen(QColor(255, 255, 255, 18), 1)
        self._grid_pen_dark = QPen(QColor(0, 0, 0, 22), 1)
        self._snap_enabled = True

    def drawBackground(self, painter: QPainter, rect: QRectF):
        from source.modules.mapa.MapaMental.mm_01_drawBackground import drawBackground as _impl
        return _impl(self, painter, rect)

    def snap(self, pos: QPointF) -> QPointF:
        from source.modules.mapa.MapaMental.mm_02_snap import snap as _impl
        return _impl(self, pos)
