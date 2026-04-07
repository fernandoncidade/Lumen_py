from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_drop_sincronizar(self):
    try:
        sender = self.sender()
        self._sincronizar_status_pos_movimento(prioridade_lista=sender)
        self.listas_atualizadas.emit()

    except Exception as e:
        logger.error(f"Erro ao sincronizar após drop: {e}", exc_info=True)
