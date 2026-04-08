from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_traducoes(self):
    try:
        ciclos_total = max(1, int(getattr(self, "ciclos_permitidos", 4)))

        if self.em_foco:
            if self.ciclos_completados >= ciclos_total:
                self.label_status.setText(QCoreApplication.translate("App", "✅ Meta concluída | Ciclo: {ciclo}/{total}").format(ciclo=ciclos_total, total=ciclos_total))

            else:
                ciclo_atual = (self.ciclos_completados % ciclos_total) + 1
                self.label_status.setText(QCoreApplication.translate("App", "🎯 Modo: Foco | Ciclo: {ciclo}/{total}").format(ciclo=ciclo_atual, total=ciclos_total))

        else:
            ciclo_concluido = self.ciclos_completados % ciclos_total

            if ciclo_concluido == 0 and self.ciclos_completados > 0:
                ciclo_concluido = ciclos_total

            elif ciclo_concluido == 0 and self.ciclos_completados == 0:
                ciclo_concluido = 1

            tipo_descanso = QCoreApplication.translate("App", "Longo") if self.ciclos_completados % ciclos_total == 0 else QCoreApplication.translate("App", "Curto")
            self.label_status.setText(QCoreApplication.translate("App", "☕ Modo: Descanso {tipo} | Ciclo: {ciclo}/{total}").format(tipo=tipo_descanso, ciclo=ciclo_concluido, total=ciclos_total))

        texto_iniciar = (QCoreApplication.translate("App", "⏸️ Pausar") if self.timer_ativo else QCoreApplication.translate("App", "▶️ Iniciar"))

        self.gerenciador_botoes.set_button_text(self.btn_iniciar, texto_iniciar)
        self.gerenciador_botoes.set_button_text(self.btn_resetar, QCoreApplication.translate("App", "⏱️ Resetar Relógio"))
        self.gerenciador_botoes.set_button_text(self.btn_pular, QCoreApplication.translate("App", "⏭️ Pular"))

        if hasattr(self, 'btn_resetar_ciclo'):
            self.gerenciador_botoes.set_button_text(self.btn_resetar_ciclo, QCoreApplication.translate("App", "🔄 Resetar Ciclo"))

        self.config_group.setTitle(QCoreApplication.translate("App", "⚙️ Configurações"))
        self.label_foco.setText(QCoreApplication.translate("App", "Foco (min):"))
        self.label_descanso.setText(QCoreApplication.translate("App", "Descanso (min):"))

        if hasattr(self, 'label_ciclos'):
            self.label_ciclos.setText(QCoreApplication.translate("App", "Ciclo 1/{total}:").format(total=ciclos_total))

        self._aplicar_tema_dinamico()

    except Exception as e:
        logger.error(f"Erro ao atualizar traduções do PomodoroTimer: {str(e)}", exc_info=True)
