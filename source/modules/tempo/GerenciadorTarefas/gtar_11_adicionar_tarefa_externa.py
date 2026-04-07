from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def adicionar_tarefa_externa(self, titulo: str, prioridade: str = "Importante e Urgente") -> None:
    try:
        titulo = (titulo or "").strip()
        if not titulo:
            return

        prioridade_norm = Tarefa.normalizar_prioridade(prioridade)

        for t in getattr(self, 'tarefas', []):
            if getattr(t, 'titulo', None) == titulo and Tarefa.normalizar_prioridade(getattr(t, 'prioridade', '')) == prioridade_norm:
                return

        self._adicionar_tarefa_interna(titulo=titulo, prioridade=prioridade_norm, status="Todo", emitir_sinal=False)

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa externa: {str(e)}", exc_info=True)
