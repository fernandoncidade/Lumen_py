from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_traducoes(self):
    try:
        if self.em_foco:
            ciclo_atual = (self.ciclos_completados % 4) + 1
            self.label_status.setText(QCoreApplication.translate("App", "🎯 Modo: Foco | Ciclo: {ciclo}/4").format(ciclo=ciclo_atual))

        else:
            ciclo_concluido = self.ciclos_completados % 4
            if ciclo_concluido == 0 and self.ciclos_completados > 0:
                ciclo_concluido = 4

            elif ciclo_concluido == 0 and self.ciclos_completados == 0:
                ciclo_concluido = 1

            tipo_descanso = QCoreApplication.translate("App", "Longo") if self.ciclos_completados % 4 == 0 else QCoreApplication.translate("App", "Curto")
            self.label_status.setText(QCoreApplication.translate("App", "☕ Modo: Descanso {tipo} | Ciclo: {ciclo}/4").format(tipo=tipo_descanso, ciclo=ciclo_concluido))

        texto_iniciar = (QCoreApplication.translate("App", "⏸️ Pausar") if self.timer_ativo else QCoreApplication.translate("App", "▶️ Iniciar"))

        self.gerenciador_botoes.set_button_text(self.btn_iniciar, texto_iniciar)
        self.gerenciador_botoes.set_button_text(self.btn_resetar, QCoreApplication.translate("App", "⏱️ Resetar Relógio"))
        self.gerenciador_botoes.set_button_text(self.btn_pular, QCoreApplication.translate("App", "⏭️ Pular"))

        if hasattr(self, 'btn_resetar_ciclo'):
            self.gerenciador_botoes.set_button_text(self.btn_resetar_ciclo, QCoreApplication.translate("App", "🔄 Resetar Ciclo"))

        self.config_group.setTitle(QCoreApplication.translate("App", "⚙️ Configurações"))
        self.label_foco.setText(QCoreApplication.translate("App", "Foco (min):"))
        self.label_descanso.setText(QCoreApplication.translate("App", "Descanso (min):"))

        self._aplicar_tema_dinamico()

    except Exception as e:
        logger.error(f"Erro ao atualizar traduções do PomodoroTimer: {str(e)}", exc_info=True)
