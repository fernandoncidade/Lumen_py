from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPainter
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class LineEditFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(self._frame_width(), self._frame_width(), self._frame_width(), self._frame_width())

    def _frame_width(self) -> int:
        try:
            from PySide6.QtWidgets import QStyle
            return int(self.style().pixelMetric(QStyle.PM_DefaultFrameWidth, None, self) or 1)

        except Exception:
            return 1

    def layout(self) -> QVBoxLayout:
        return self._layout

    def paintEvent(self, event):
        try:
            from PySide6.QtWidgets import QStyleOptionFrame, QStyle
            opt = QStyleOptionFrame()
            opt.initFrom(self)
            opt.rect = self.rect()
            opt.lineWidth = self._frame_width()
            opt.midLineWidth = 0

            painter = QPainter(self)
            self.style().drawPrimitive(QStyle.PE_FrameLineEdit, opt, painter, self)

        except Exception:
            return super().paintEvent(event)
