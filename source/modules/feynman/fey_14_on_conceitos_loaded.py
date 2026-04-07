from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_conceitos_loaded(self, conceitos):
    try:
        self.conceitos = conceitos or []
        try:
            if hasattr(self, 'atualizar_lista'):
                self.atualizar_lista()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao processar conceitos carregados: {e}", exc_info=True)
