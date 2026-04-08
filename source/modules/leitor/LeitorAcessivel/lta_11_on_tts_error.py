from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_tts_error(self, err):
    logger.error(f"Erro no Edge TTS: {err}", exc_info=True)
    MessageBox.leitor_tts_error(self, err)
    self.leitura_finalizada()
