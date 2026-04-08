from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QBrush
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _draw_badge(self, painter, rect, count):
    try:
        painter.save()

        badge_size = 16
        padding = 2

        badge_x = rect.right() - badge_size - padding
        badge_y = rect.top() + padding
        badge_rect = QRect(badge_x, badge_y, badge_size, badge_size)

        pal = self.palette()
        badge_color = pal.highlight().color()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(badge_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(badge_rect)

        painter.setPen(pal.highlightedText().color())
        font = painter.font()
        font.setPixelSize(10)
        font.setBold(True)
        painter.setFont(font)

        count_text = str(count) if count < 100 else "99+"
        painter.drawText(badge_rect, Qt.AlignCenter, count_text)

        painter.restore()

    except Exception as e:
        logger.error(f"Erro ao desenhar badge: {e}", exc_info=True)
