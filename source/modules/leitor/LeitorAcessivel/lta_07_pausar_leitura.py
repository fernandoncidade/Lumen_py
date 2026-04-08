from PySide6.QtMultimedia import QMediaPlayer
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def pausar_leitura(self):
    try:
        if self.usar_edge_tts:
            estado = self.player.playbackState()

            if estado == QMediaPlayer.PlayingState:
                self.player.pause()
                self._is_paused = True
                self._update_pause_button()
                self._pause_speech_highlight()
                self._pause_pdf_speech_highlight()

            elif estado == QMediaPlayer.PausedState:
                self.player.play()
                self._is_paused = False
                self._update_pause_button()
                self._resume_speech_highlight()
                self._resume_pdf_speech_highlight()

            else:
                pass

        else:
            MessageBox.leitor_pause_requires_edge_tts(self)

    except Exception as e:
        logger.error(f"Erro ao alternar pausa/continuação: {str(e)}", exc_info=True)
