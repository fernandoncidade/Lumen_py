from PySide6.QtCore import QThread
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _stop_eisenhower_thread(self):
    try:
        if hasattr(self, '_eisenhower_thread') and isinstance(self._eisenhower_thread, QThread) and self._eisenhower_thread.isRunning():
            try:
                self._eisenhower_thread.quit()

            except Exception as e:
                logger.error(f"Erro ao solicitar parada da thread do Eisenhower: {e}", exc_info=True)

            try:
                self._eisenhower_thread.wait(3000)

            except Exception as e:
                logger.error(f"Erro ao aguardar parada da thread do Eisenhower: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao parar thread do Eisenhower: {e}", exc_info=True)

def cleanup(self):
    try:
        self._stop_eisenhower_thread()

    except Exception as e:
        logger.error(f"Erro ao limpar recursos do Eisenhower: {e}", exc_info=True)
