from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from .services import init_ui
from .interface import Calendar
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def initUI(self):
    init_ui(self)
    try:
        if hasattr(self, "_root_widget"):
            outer_layout = QHBoxLayout(self)
            outer_layout.setContentsMargins(0, 0, 0, 0)
            outer_layout.setSpacing(0)

            self.calendar_pane = Calendar(self)
            outer_layout.addWidget(self.calendar_pane, 0, Qt.AlignLeft)
            outer_layout.addWidget(self._root_widget, 1)

            self._hide_legacy_calendar_button()

    except Exception as e:
        logger.error(f"Erro ao inicializar UI (embedded): {e}", exc_info=True)
