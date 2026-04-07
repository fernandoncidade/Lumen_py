from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def toggle_timer(self):
    try:
        if self.timer_ativo:
            self.timer.stop()
            self.timer_ativo = False
            self.gerenciador_botoes.set_button_text(self.btn_iniciar, QCoreApplication.translate("App", "▶️ Continuar"))

        else:
            self.timer.start(1000)
            self.timer_ativo = True
            self.gerenciador_botoes.set_button_text(self.btn_iniciar, QCoreApplication.translate("App", "⏸️ Pausar"))

    except Exception as e:
        logger.error(f"Erro ao alternar estado do timer: {str(e)}", exc_info=True)
