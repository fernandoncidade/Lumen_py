from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_timer(self):
    try:
        self.tempo_restante -= 1
        self.progress.setValue(self.tempo_restante)
        self.atualizar_display()

        if self.tempo_restante <= 0:
            self.timer.stop()
            self.finalizar_ciclo()

    except Exception as e:
        logger.error(f"Erro ao atualizar timer: {str(e)}", exc_info=True)
