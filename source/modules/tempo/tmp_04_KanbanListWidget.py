from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Signal
from source.utils.LogManager import LogManager


class _KanbanListWidget(QListWidget):
    tarefas_soltadas = Signal()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.tarefas_soltadas.emit()
