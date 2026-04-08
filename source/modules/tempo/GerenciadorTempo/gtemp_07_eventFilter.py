from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def eventFilter(self, obj, event):
    try:
        tipos = (
            QEvent.ApplicationPaletteChange,
            QEvent.PaletteChange,
            QEvent.StyleChange,
            QEvent.ThemeChange,
        )
        try:
            tipos = tipos + (QEvent.ColorSchemeChange,)

        except AttributeError:
            pass

        if event.type() in tipos:
            self._aplicar_tema_dinamico_inputs()

            try:
                if hasattr(self, "_ajustar_largura_minima_coluna_esquerda"):
                    self._ajustar_largura_minima_coluna_esquerda()

            except Exception:
                pass

        if event.type() == QEvent.Resize:
            try:
                if hasattr(self, "_ajustar_largura_minima_coluna_esquerda"):
                    self._ajustar_largura_minima_coluna_esquerda()

            except Exception:
                pass

    except Exception as e:
        logger.error(f"Erro no eventFilter do GerenciadorTempo: {str(e)}", exc_info=True)

    return QWidget.eventFilter(self, obj, event)
