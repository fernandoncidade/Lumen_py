from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_display(self):
    try:
        minutos = self.tempo_restante // 60
        segundos = self.tempo_restante % 60
        self.label_tempo.setText(f"{minutos:02d}:{segundos:02d}")

    except Exception as e:
        logger.error(f"Erro ao atualizar display do timer: {str(e)}", exc_info=True)
