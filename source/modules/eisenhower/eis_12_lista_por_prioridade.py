from source.modules.tempo.tmp_01_Tarefa import Tarefa
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _lista_por_prioridade(self, prioridade: str):
    try:
        try:
            p = Tarefa.normalizar_prioridade(prioridade)

        except Exception as e:
            logger.error(f"Falha ao normalizar prioridade: {e}", exc_info=True)
            p = "Importante e Urgente"

        if p == "Importante e Urgente":
            return getattr(self, "quadrant1_list", None)

        if p == "Importante, mas Não Urgente":
            return getattr(self, "quadrant2_list", None)

        if p == "Não Importante, mas Urgente":
            return getattr(self, "quadrant3_list", None)

        return getattr(self, "quadrant4_list", None)

    except Exception as e:
        logger.error(f"Erro ao obter lista por prioridade: {e}", exc_info=True)
