from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Signal
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class _KanbanListWidget(QListWidget):
    tarefas_soltadas = Signal()

    try:
        def dropEvent(self, event):
            super().dropEvent(event)
            self.tarefas_soltadas.emit()

    except Exception as e:
        logger.error(f"Erro no KanbanListWidget.dropEvent: {str(e)}", exc_info=True)
