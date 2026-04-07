from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def cleanup(self):
    try:
        self._stop_feynman_thread()

    except Exception as e:
        logger.error(f"Erro ao executar cleanup: {e}", exc_info=True)
