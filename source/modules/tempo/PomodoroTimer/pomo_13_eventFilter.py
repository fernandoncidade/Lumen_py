from PySide6.QtCore import QEvent, QObject
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def eventFilter(self, obj, event):
    try:
        tipos = (
            QEvent.ApplicationPaletteChange,
            QEvent.PaletteChange,
            QEvent.StyleChange,
        )

        try:
            tipos = tipos + (QEvent.ColorSchemeChange,)

        except AttributeError:
            pass

        if event.type() in tipos:
            self._aplicar_tema_dinamico()

    except Exception as e:
        logger.error(f"Erro no eventFilter PomodoroTimer: {str(e)}", exc_info=True)

    return QObject.eventFilter(self, obj, event)
