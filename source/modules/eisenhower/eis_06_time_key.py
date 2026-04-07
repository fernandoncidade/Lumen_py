from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _time_key(self, time_str: str):
    if not time_str:
        return (999, 999)

    try:
        parts = time_str.split(":")
        return (int(parts[0]), int(parts[1]))

    except Exception as e:
        logger.error(f"Erro ao converter hora '{time_str}' para chave de tempo: {e}", exc_info=True)
        return (999, 999)
