from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QSplitter
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
            self.main_splitter = QSplitter(Qt.Horizontal, self)
            self.main_splitter.setChildrenCollapsible(False)
            self.main_splitter.addWidget(self.calendar_pane)
            self.main_splitter.addWidget(self._root_widget)
            self.main_splitter.setCollapsible(0, False)
            self.main_splitter.setCollapsible(1, False)
            self.main_splitter.setStretchFactor(0, 0)
            self.main_splitter.setStretchFactor(1, 1)

            self._root_widget.setMinimumWidth(420)
            self.calendar_pane.setMinimumWidth(self.calendar_pane.effective_min_width())
            self.main_splitter.setSizes([self.calendar_pane.effective_min_width(), 1000])
            self.calendar_pane._update_splitter_interaction()

            outer_layout.addWidget(self.main_splitter)

            self._hide_legacy_calendar_button()

    except Exception as e:
        logger.error(f"Erro ao inicializar UI (embedded): {e}", exc_info=True)
