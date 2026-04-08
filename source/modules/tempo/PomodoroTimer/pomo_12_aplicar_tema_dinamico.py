from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _aplicar_tema_dinamico(self):
    try:
        app = QCoreApplication.instance()
        if not app:
            return

        app_pal = app.palette()
        window_color = app_pal.color(QPalette.Window)

        def _is_light_color(col) -> bool:
            try:
                r, g, b = col.red(), col.green(), col.blue()
                lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                return lum >= 0.85

            except Exception:
                return True

        is_light_theme = _is_light_color(window_color)

        for lbl in (self.label_status, self.label_tempo):
            lbl.setPalette(app_pal)
            lbl.setAutoFillBackground(False)

        def _apply_combo_base_as_window(combo: QComboBox):
            if combo is None:
                return

            pal = combo.palette()

            try:
                pal.setColor(QPalette.Button, window_color)

            except Exception:
                pass

            combo.setPalette(pal)

            try:
                view = combo.view()

                if view is not None:
                    popup_pal = view.palette()

                    if is_light_theme:
                        popup_base = window_color

                    else:
                        popup_base = window_color.darker(115)

                    popup_pal.setColor(QPalette.Base, popup_base)
                    popup_pal.setColor(QPalette.AlternateBase, popup_base)
                    view.setPalette(popup_pal)

                    try:
                        view.viewport().setAutoFillBackground(True)
                        view.viewport().setPalette(popup_pal)

                    except Exception:
                        pass

            except Exception:
                pass

        _apply_combo_base_as_window(getattr(self, "spin_foco", None))
        _apply_combo_base_as_window(getattr(self, "spin_descanso", None))

        self.update()

    except Exception as e:
        logger.error(f"Erro ao aplicar tema dinâmico PomodoroTimer: {str(e)}", exc_info=True)
