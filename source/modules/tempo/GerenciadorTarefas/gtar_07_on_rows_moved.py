from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_rows_moved(self, lista):
    try:
        self._sincronizar_status_pos_movimento(prioridade_lista=lista)

    except Exception as e:
        logger.error(f"Erro ao tratar rowsMoved: {e}", exc_info=True)
