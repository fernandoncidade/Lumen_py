from PySide6.QtWidgets import QMenu
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, pos, lista):
    try:
        item = lista.itemAt(pos)
        if not item:
            return

        menu = QMenu(lista)

        ac_mover_unico = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa"), self)
        ac_mover_unico.triggered.connect(lambda: self.mover_tarefa_por_item(item))
        menu.addAction(ac_mover_unico)

        if self._ha_tarefas_marcadas():
            ac_mover_marcadas = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa(s) Marcadas"), self)
            ac_mover_marcadas.triggered.connect(self.mover_tarefas_marcadas)
            menu.addAction(ac_mover_marcadas)

        ac_remover = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa"), self)
        ac_remover.triggered.connect(lambda: self.remover_tarefa_por_item(item))
        menu.addAction(ac_remover)

        if self._ha_tarefas_marcadas():
            ac_remover_marcadas = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa(s) Marcadas"), self)
            ac_remover_marcadas.triggered.connect(self.remover_tarefas_marcadas)
            menu.addAction(ac_remover_marcadas)

        menu.exec(lista.mapToGlobal(pos))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {str(e)}", exc_info=True)
