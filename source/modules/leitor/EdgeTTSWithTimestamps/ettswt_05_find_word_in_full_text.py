from source.utils.LogManager import LogManager
import re
logger = LogManager.get_logger()

def _find_word_in_full_text(self, word: str, full_text: str, start: int) -> tuple[int, int, int]:
    try:
        if start is None or start < 0:
            start = 0

        w = (word or "").strip()
        if not w:
            return -1, start, 0

        def _norm(s: str) -> str:
            return (
                (s or "")
                .replace("’", "'")
                .replace("‘", "'")
                .replace("`", "'")
                .replace("´", "'")
            )

        full_norm = _norm(full_text)
        w_norm = _norm(w)
        full_lower = full_norm.lower()
        w_lower = w_norm.lower()

        candidates: list[tuple[str, int]] = [(w_lower, len(w_lower))]
        try:
            stripped = re.sub(r"^\W+|\W+$", "", w_lower, flags=re.UNICODE)
            if stripped and stripped != w_lower:
                candidates.insert(0, (stripped, len(stripped)))

        except Exception as e:
            logger.error(f"Erro ao encontrar palavra no texto completo: {e}", exc_info=True)

        for cand, clen in candidates:
            pos = full_lower.find(cand, start)
            if pos >= 0:
                return pos, pos + clen, clen

        for cand, clen in candidates:
            pos = full_lower.find(cand)
            if pos >= 0:
                return pos, pos + clen, clen

    except Exception as e:
        logger.error(f"Erro ao encontrar palavra no texto completo: {e}", exc_info=True)

    return -1, start, 0
