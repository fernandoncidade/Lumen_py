from typing import Dict
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _log_estrutura_completa(self, no: Dict, nivel: int = 0):
    try:
        indent = "  " * nivel
        titulo = no.get('titulo', self._tr('Sem título'))[:50]
        num_conceitos = len(no.get('conceitos', []))
        num_ideias = len(no.get('ideias_principais', []))
        num_filhos = len(no.get('filhos', []))

        simbolo = {0: "🌳", 1: "🌿", 2: "🌱", 3: "🍃", 4: "🌾"}.get(nivel, "•")

        logger.debug(
            f"{indent}{simbolo} [{nivel}] {titulo} "
            f"({num_conceitos} conceitos, {num_ideias} ideias, {num_filhos} filhos)"
        )

        for filho in no.get('filhos', []):
            self._log_estrutura_completa(filho, nivel + 1)

    except Exception as e:
        logger.error(f"Erro ao logar estrutura: {e}")
