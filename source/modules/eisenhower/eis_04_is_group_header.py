from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _is_group_header(self, item):
    try:
        return item.data(Qt.UserRole + 1) == "group_header"

    except Exception as e:
        logger.error(f"Erro ao verificar se o item é um cabeçalho de grupo: {e}", exc_info=True)
        return False
