from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_drop_sincronizar(self):
    try:
        sender = self.sender()
        self._sincronizar_status_pos_movimento(prioridade_lista=sender)

        if hasattr(self, "atualizar_listas") and callable(self.atualizar_listas):
            self.atualizar_listas()

        else:
            self.listas_atualizadas.emit()

    except Exception as e:
        logger.error(f"Erro ao sincronizar após drop: {e}", exc_info=True)
