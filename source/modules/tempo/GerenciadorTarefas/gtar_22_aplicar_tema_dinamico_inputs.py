from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _aplicar_tema_dinamico_inputs(self):
    try:
        app = QCoreApplication.instance()
        if not app:
            return

        app_pal = app.palette()
        window_color = app_pal.color(QPalette.Window)
        highlight_color = app_pal.color(QPalette.Highlight)
        highlight_text = app_pal.color(QPalette.HighlightedText)
        text_color = app_pal.color(QPalette.Text)
        button_text = app_pal.color(QPalette.ButtonText)
        window_text = app_pal.color(QPalette.WindowText)

        def _apply_base_as_window(widget):
            if widget is None:
                return

            pal = widget.palette()
            pal.setColor(QPalette.Base, window_color)
            pal.setColor(QPalette.AlternateBase, window_color)
            try:
                from PySide6.QtWidgets import QListWidget
                is_list = isinstance(widget, QListWidget)

            except Exception:
                is_list = False

            if not is_list:
                pal.setColor(QPalette.Button, window_color)

            pal.setColor(QPalette.Highlight, highlight_color)
            pal.setColor(QPalette.HighlightedText, highlight_text)
            pal.setColor(QPalette.Text, text_color)
            pal.setColor(QPalette.ButtonText, button_text)
            pal.setColor(QPalette.WindowText, window_text)

            widget.setPalette(pal)

            vp = getattr(widget, "viewport", None)
            if callable(vp):
                try:
                    widget.viewport().setAutoFillBackground(True)
                    widget.viewport().setPalette(pal)

                except Exception:
                    pass

            else:
                widget.setAutoFillBackground(True)

            try:
                view = getattr(widget, "view", None)
                if callable(view):
                    v = view()
                    if v is not None:
                        v.setPalette(pal)
                        try:
                            v.viewport().setAutoFillBackground(True)

                        except Exception:
                            pass

            except Exception:
                pass

        _apply_base_as_window(getattr(self, "input_tarefa", None))
        _apply_base_as_window(getattr(self, "combo_prioridade", None))

        try:
            _apply_base_as_window(self.col_todo.lista)
            _apply_base_as_window(self.col_doing.lista)
            _apply_base_as_window(self.col_done.lista)

        except Exception:
            pass

        self.update()

    except Exception as e:
        logger.error(f"Erro ao aplicar tema dinâmico (inputs) no GerenciadorTarefas: {str(e)}", exc_info=True)
