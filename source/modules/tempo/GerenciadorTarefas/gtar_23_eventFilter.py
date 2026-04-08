from PySide6.QtCore import QEvent, QObject
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
            if event.type() == QEvent.Resize:
                try:
                    if hasattr(self, "_ajustar_linha_botoes") and callable(self._ajustar_linha_botoes):
                        self._ajustar_linha_botoes()

                except Exception:
                    pass

                if hasattr(obj, "_rounded_radius"):
                    self._update_rounded_mask(obj, getattr(obj, "_rounded_radius", 8))

                for g in (getattr(self, 'col_todo', None), getattr(self, 'col_doing', None), getattr(self, 'col_done', None)):
                    if g and hasattr(g, "_rounded_radius"):
                        self._update_rounded_mask(g, getattr(g, "_rounded_radius", 8))

                        try:
                            self._update_rounded_mask(g.lista, max(0, g._rounded_radius - 2))
                            vp = getattr(g.lista, "viewport", None)
                            if callable(vp):
                                self._update_rounded_mask(g.lista.viewport(), max(0, g._rounded_radius - 2))

                        except Exception:
                            pass

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro no eventFilter do GerenciadorTarefas: {str(e)}", exc_info=True)

    return QObject.eventFilter(self, obj, event)
