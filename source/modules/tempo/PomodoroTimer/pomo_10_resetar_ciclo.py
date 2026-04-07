from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def resetar_ciclo(self):
    try:
        self.timer.stop()
        self.timer_ativo = False
        self.em_foco = True
        self.ciclos_completados = 0
        self.tempo_restante = self.tempo_foco
        self.progress.setMaximum(self.tempo_foco)
        self.progress.setValue(self.tempo_foco)
        self.atualizar_display()

        self.gerenciador_botoes.set_button_text(self.btn_iniciar, QCoreApplication.translate("App", "▶️ Iniciar"))
        self.atualizar_traducoes()

    except Exception as e:
        logger.error(f"Erro ao resetar ciclo: {str(e)}", exc_info=True)
