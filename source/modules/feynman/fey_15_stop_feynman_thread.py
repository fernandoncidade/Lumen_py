from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _stop_feynman_thread(self):
    try:
        if hasattr(self, '_feynman_thread') and self._feynman_thread.isRunning():
            self._feynman_thread.quit()
            self._feynman_thread.wait(3000)

    except Exception as e:
        logger.error(f"Erro ao parar thread do Método Feynman: {e}", exc_info=True)
