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

        def _is_light_color(col) -> bool:
            try:
                r, g, b = col.red(), col.green(), col.blue()
                lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                return lum >= 0.85

            except Exception:
                return True

        is_light_theme = _is_light_color(window_color)

        def _apply_base_as_window(widget):
            if widget is None:
                return

            pal = widget.palette()

            try:
                from PySide6.QtWidgets import QListWidget, QLineEdit, QComboBox
                is_list = isinstance(widget, QListWidget)
                is_native_input = isinstance(widget, (QLineEdit, QComboBox))

            except Exception:
                is_list = False
                is_native_input = False

            if not is_native_input:
                pal.setColor(QPalette.Base, window_color)
                pal.setColor(QPalette.AlternateBase, window_color)

            else:
                try:
                    if is_light_theme:
                        pal.setColor(QPalette.Base, window_color)

                    else:
                        darker = window_color.darker(110)
                        pal.setColor(QPalette.Base, darker)

                except Exception:
                    pass

            if not is_list:
                pal.setColor(QPalette.Button, window_color)

            pal.setColor(QPalette.Highlight, highlight_color)
            pal.setColor(QPalette.HighlightedText, highlight_text)
            pal.setColor(QPalette.Text, text_color)
            pal.setColor(QPalette.ButtonText, button_text)
            pal.setColor(QPalette.WindowText, window_text)

            widget.setPalette(pal)

            if not is_native_input:
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
                        if is_native_input:
                            popup_pal = v.palette()

                            if is_light_theme:
                                popup_base = window_color

                            else:
                                popup_base = window_color.darker(115)

                            popup_pal.setColor(QPalette.Base, popup_base)
                            popup_pal.setColor(QPalette.AlternateBase, popup_base)
                            v.setPalette(popup_pal)

                            try:
                                v.viewport().setAutoFillBackground(True)
                                v.viewport().setPalette(popup_pal)

                            except Exception:
                                pass

                        else:
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
