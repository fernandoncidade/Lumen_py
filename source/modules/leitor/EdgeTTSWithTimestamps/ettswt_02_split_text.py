from source.utils.LogManager import LogManager
import re
logger = LogManager.get_logger()

def _split_text(self, text: str, max_chars: int = 3500) -> list:
    try:
        sentences = re.split(r'(?<=[\.\?\!\n])\s+', text)
        chunks = []
        cur = ""
        for s in sentences:
            s = s.strip()
            if not s:
                continue

            if len(cur) + len(s) + 1 <= max_chars:
                cur = (cur + " " + s).strip() if cur else s

            else:
                if cur:
                    chunks.append(cur)

                cur = s

        if cur:
            chunks.append(cur)

        return chunks

    except Exception as e:
        logger.error(f"Erro ao dividir o texto em partes: {e}", exc_info=True)
