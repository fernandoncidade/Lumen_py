from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter


class SmoothGraphicsView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self._current_zoom = 0

    def wheelEvent(self, event):
        from source.modules.mapa.MapaMental.mm_03_wheelEvent import wheelEvent as _impl
        return _impl(self, event)

    def animate_focus_on(self, item):
        from source.modules.mapa.MapaMental.mm_04_animate_focus_on import animate_focus_on as _impl
        return _impl(self, item)
