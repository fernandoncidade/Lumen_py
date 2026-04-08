from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def pular_ciclo(self):
    try:
        ciclos_total = max(1, int(getattr(self, "ciclos_permitidos", 4)))
        if self.em_foco and self.ciclos_completados >= ciclos_total:
            return

        self.timer.stop()
        self.tempo_restante = 0
        self.finalizar_ciclo()

    except Exception as e:
        logger.error(f"Erro ao pular ciclo: {str(e)}", exc_info=True)
