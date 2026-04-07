from PySide6.QtCore import QTimer
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_textos_atualizar(self):
    def _apply_updates():
        try:
            try:
                from source.modules.eisenhower import atualizar_textos as _atualizar_textos

            except Exception:
                _atualizar_textos = globals().get('atualizar_textos')

            if _atualizar_textos:
                _atualizar_textos(self)

            else:
                logger.debug('atualizar_textos não disponível no momento')

            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.on_language_changed()

        except Exception as e:
            logger.error(f"Erro ao atualizar textos: {e}", exc_info=True)

    try:
        QTimer.singleShot(0, _apply_updates)

    except Exception as e:
        logger.error(f"Erro ao agendar atualização de textos: {e}", exc_info=True)
        _apply_updates()
