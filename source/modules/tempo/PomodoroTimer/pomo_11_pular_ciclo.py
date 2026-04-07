from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def pular_ciclo(self):
    try:
        self.timer.stop()
        self.tempo_restante = 0
        self.finalizar_ciclo()

    except Exception as e:
        logger.error(f"Erro ao pular ciclo: {str(e)}", exc_info=True)
