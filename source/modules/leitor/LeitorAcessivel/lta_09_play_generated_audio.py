from PySide6.QtCore import QUrl
from source.utils.LogManager import LogManager
import os
logger = LogManager.get_logger()

def _play_generated_audio(self, path):
    try:
        try:
            if getattr(self, "_stopping_tts", False):
                try:
                    if path and os.path.exists(path):
                        os.remove(path)

                except Exception:
                    logger.debug(f"Chunk gerado após STOP não pôde ser removido: {path}", exc_info=True)

                return

        except Exception:
            pass

        try:
            if getattr(self, "_changing_voice", False):
                try:
                    if path and os.path.exists(path):
                        os.remove(path)

                except Exception:
                    logger.debug(f"Ignorando chunk gerado durante troca de voz (não pôde remover): {path}", exc_info=True)

                return

        except Exception:
            pass

        if not hasattr(self, "_generated_queue") or self._generated_queue is None:
            self._generated_queue = []

        if not hasattr(self, "_generated_files") or self._generated_files is None:
            self._generated_files = []

        if path not in self._generated_files:
            self._generated_files.append(path)

        self._generated_queue.append(path)

        playing_state = None

        try:
            if hasattr(self, "player") and self.player is not None:
                playing_state = self.player.playbackState()

        except Exception:
            playing_state = None

        from PySide6.QtMultimedia import QMediaPlayer

        if playing_state == QMediaPlayer.PlayingState:
            return

        if playing_state == QMediaPlayer.PausedState or getattr(self, "_is_paused", False):
            return

        try:
            next_path = self._generated_queue.pop(0)
            self._current_generated = next_path

            try:
                from PySide6.QtMultimedia import QAudioOutput, QMediaDevices

                try:
                    dev = QMediaDevices.defaultAudioOutput()
                    new_output = QAudioOutput(dev, self)

                except Exception:
                    new_output = QAudioOutput(self)

                try:
                    vol = getattr(self, 'slider_volume', None)
                    if vol is not None:
                        new_output.setVolume(vol.value() / 100.0)

                except Exception:
                    pass

                self.audio_output = new_output
                self.player.setAudioOutput(self.audio_output)

            except Exception:
                pass

            self.player.setSource(QUrl.fromLocalFile(next_path))
            self.player.play()

        except Exception as e:
            logger.error(f"Erro ao iniciar reprodução do chunk: {e}", exc_info=True)

            try:
                self.leitura_finalizada()

            except Exception as e:
                logger.error(f"Erro ao finalizar leitura após falha na reprodução do chunk: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao adicionar áudio gerado à fila: {str(e)}", exc_info=True)

        try:
            self.leitura_finalizada()

        except Exception as e:
            logger.error(f"Erro ao finalizar leitura após falha na reprodução do chunk: {e}", exc_info=True)
