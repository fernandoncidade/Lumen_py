from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _time_group_label(self, time_str: str) -> str:
    try:
        hh = int((time_str or "0:0").split(":")[0])

    except Exception as e:
        logger.error(f"Erro ao analisar hora para rótulo de grupo: {e}", exc_info=True)
        hh = 0

    return f"{hh:02d}:00–{hh:02d}:59"
