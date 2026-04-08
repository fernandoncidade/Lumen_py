from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def resetar_timer(self):
    try:
        ciclos_total = max(1, int(getattr(self, "ciclos_permitidos", 4)))
        self.timer.stop()
        self.timer_ativo = False
        self.tempo_restante = self.tempo_foco if self.em_foco else (self.tempo_descanso_longo if (self.ciclos_completados % ciclos_total == 0) else self.tempo_descanso_curto)
        self.progress.setMaximum(self.tempo_restante)
        self.progress.setValue(self.tempo_restante)
        self.atualizar_display()
        self.gerenciador_botoes.set_button_text(self.btn_iniciar, QCoreApplication.translate("App", "▶️ Iniciar"))

    except Exception as e:
        logger.error(f"Erro ao resetar timer: {str(e)}", exc_info=True)
