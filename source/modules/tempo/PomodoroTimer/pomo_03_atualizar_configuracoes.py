from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_configuracoes(self):
    try:
        novo_foco = int(self.spin_foco.currentText()) * 60
        novo_descanso_curto = int(self.spin_descanso.currentText()) * 60

        if self.em_foco:
            total_antigo = self.tempo_foco

        else:
            total_antigo = self.tempo_descanso_longo if (self.ciclos_completados % 4 == 0) else self.tempo_descanso_curto

        decorrido = max(0, total_antigo - self.tempo_restante)

        self.tempo_foco = novo_foco
        self.tempo_descanso_curto = novo_descanso_curto

        if self.em_foco:
            total_novo = self.tempo_foco

        else:
            total_novo = self.tempo_descanso_longo if (self.ciclos_completados % 4 == 0) else self.tempo_descanso_curto

        self.tempo_restante = max(total_novo - decorrido, 0)

        self.progress.setMaximum(total_novo)
        self.progress.setValue(self.tempo_restante)
        self.atualizar_display()
        self.atualizar_traducoes()

    except Exception as e:
        logger.error(f"Erro ao atualizar configurações do timer: {str(e)}", exc_info=True)
