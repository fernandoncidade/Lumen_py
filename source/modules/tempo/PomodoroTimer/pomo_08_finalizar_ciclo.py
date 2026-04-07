from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def finalizar_ciclo(self):
    try:
        if self.em_foco:
            self.ciclos_completados += 1
            self.ciclo_completado.emit("foco")

            self._executar_alerta(
                QCoreApplication.translate("App", "🎉 Ciclo Completo!"),
                QCoreApplication.translate("App",
                    "Parabéns! Você completou um ciclo de foco.\n"
                    "Ciclos hoje: {ciclos}\n\n"
                    "Hora de descansar! 😊"
                ).format(ciclos=self.ciclos_completados)
            )

            if self.ciclos_completados % 4 == 0:
                self.tempo_restante = self.tempo_descanso_longo
                tipo_descanso = QCoreApplication.translate("App", "Longo")

            else:
                self.tempo_restante = self.tempo_descanso_curto
                tipo_descanso = QCoreApplication.translate("App", "Curto")

            self.em_foco = False
            ciclo_concluido = self.ciclos_completados % 4
            if ciclo_concluido == 0:
                ciclo_concluido = 4

            self.label_status.setText(QCoreApplication.translate("App", "☕ Modo: Descanso {tipo} | Ciclo: {ciclo}/4").format(tipo=tipo_descanso, ciclo=ciclo_concluido))
            self.progress.setMaximum(self.tempo_restante)
            self.progress.setValue(self.tempo_restante)

        else:
            self.ciclo_completado.emit("descanso")

            self._executar_alerta(
                QCoreApplication.translate("App", "✅ Descanso Completo"),
                QCoreApplication.translate("App",
                    "Descanso finalizado!\n"
                    "Vamos para o próximo ciclo de foco! 💪"
                )
            )

            self.em_foco = True
            self.tempo_restante = self.tempo_foco
            ciclo_atual = (self.ciclos_completados % 4) + 1
            self.label_status.setText(QCoreApplication.translate("App", "🎯 Modo: Foco | Ciclo: {ciclo}/4").format(ciclo=ciclo_atual))
            self.progress.setMaximum(self.tempo_foco)
            self.progress.setValue(self.tempo_foco)

        self.atualizar_display()
        self.timer_ativo = False
        self.gerenciador_botoes.set_button_text(self.btn_iniciar, QCoreApplication.translate("App", "▶️ Iniciar"))

    except Exception as e:
        logger.error(f"Erro ao finalizar ciclo: {str(e)}", exc_info=True)
