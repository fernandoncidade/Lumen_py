from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _aplicar_tema_dinamico_inputs(self):
    try:
        app = QCoreApplication.instance()
        if not app:
            return

        window_color = app.palette().color(QPalette.Window)

        try:
            if hasattr(self, 'label_tarefas') and self.label_tarefas is not None:
                pal_lbl = self.label_tarefas.palette()
                pal_lbl.setColor(QPalette.WindowText, app.palette().color(QPalette.WindowText))
                pal_lbl.setColor(QPalette.Text, app.palette().color(QPalette.Text))
                self.label_tarefas.setPalette(pal_lbl)

        except Exception as e:
            logger.debug(f"Falha ao sincronizar cor do label_tarefas: {e}", exc_info=True)

        pal = self.col_doing_timer_list.palette()
        pal.setColor(QPalette.Base, window_color)
        pal.setColor(QPalette.AlternateBase, window_color)
        self.col_doing_timer_list.setPalette(pal)
        self.col_doing_timer_list.viewport().setAutoFillBackground(True)

        self.update()

    except Exception as e:
        logger.error(f"Erro ao aplicar tema dinâmico (lista) no GerenciadorTempo: {str(e)}", exc_info=True)
