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

        for lbl in (self.label_status, self.label_tempo):
            lbl.setPalette(app_pal)
            lbl.setAutoFillBackground(False)

        def _apply_combo_base_as_window(combo: QComboBox):
            if combo is None:
                return

            pal = combo.palette()
            pal.setColor(QPalette.Button, window_color)
            pal.setColor(QPalette.Base, window_color)
            pal.setColor(QPalette.AlternateBase, window_color)
            combo.setPalette(pal)
            combo.setAutoFillBackground(True)

            view = combo.view()
            if view is not None:
                view.setPalette(pal)
                try:
                    view.viewport().setAutoFillBackground(True)

                except Exception:
                    pass

        _apply_combo_base_as_window(getattr(self, "spin_foco", None))
        _apply_combo_base_as_window(getattr(self, "spin_descanso", None))

        self.update()

    except Exception as e:
        logger.error(f"Erro ao aplicar tema dinâmico PomodoroTimer: {str(e)}", exc_info=True)
