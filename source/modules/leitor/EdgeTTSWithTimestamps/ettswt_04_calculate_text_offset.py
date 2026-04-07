from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _calculate_text_offset(self, word: str, segment: str, last_offset: int) -> int:
    try:
        idx = segment.lower().find(word.lower(), last_offset)
        if idx >= 0:
            return idx

        idx = segment.lower().find(word.lower())
        if idx >= 0:
            return idx

    except Exception as e:
        logger.error(f"Erro ao calcular o deslocamento do texto: {e}", exc_info=True)
        pass

    return last_offset
