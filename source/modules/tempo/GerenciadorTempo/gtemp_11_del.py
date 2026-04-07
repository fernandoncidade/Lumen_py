from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def __del__(self):
    try:
        self.cleanup()

    except Exception as e:
        logger.error(f"Erro no __del__: {e}", exc_info=True)
