from source.utils.LogManager import LogManager
import re
logger = LogManager.get_logger()

def _normalize_voice(self, voz):
    try:
        if not voz:
            return voz

        if re.match(r'^[a-z]{2}-[A-Z]{2}-', voz):
            return voz

        m = re.search(r'\(\s*(?P<locale>[a-z]{2}-[A-Z]{2})\s*,\s*(?P<token>[A-Za-z0-9_ -]+)\s*\)', voz)
        if m:
            token = m.group('token').strip().replace(' ', '')
            return f"{m.group('locale')}-{token}"

        m2 = re.search(r'([a-z]{2}-[A-Z]{2}-[A-Za-z0-9_]+)', voz)
        if m2:
            return m2.group(1)

        m3 = re.search(r'([a-z]{2}-[A-Z]{2})\s*,\s*([A-Za-z0-9_ -]+)', voz)
        if m3:
            token = m3.group(2).strip().replace(' ', '')
            return f"{m3.group(1)}-{token}"

        logger.debug(f"Voice id '{voz}' parece inválido; normalizando com 'pt-BR-' prefix.")
        return f"pt-BR-{voz}"

    except Exception as e:
        logger.error(f"Erro ao normalizar voz: {e}", exc_info=True)

    return voz
