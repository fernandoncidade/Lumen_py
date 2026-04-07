from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _ha_tarefas_marcadas(self):
    try:
        for lst in (self.col_todo.lista, self.col_doing.lista, self.col_done.lista):
            for i in range(lst.count()):
                if lst.item(i).checkState() == Qt.Checked:
                    return True

        return False

    except Exception as e:
        logger.error(f"Erro ao verificar se há tarefas marcadas: {str(e)}", exc_info=True)
        return False
