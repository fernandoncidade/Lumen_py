from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def _adicionar_tarefa_interna(self, titulo: str, prioridade: str, status: str = "Todo", emitir_sinal: bool = True):
    try:
        tarefa = Tarefa(titulo, prioridade=prioridade, status=status)
        self.tarefas.append(tarefa)
        self.salvar_tarefas()
        self.atualizar_listas()

        if emitir_sinal:
            try:
                self.tarefa_adicionada.emit({
                    "id": getattr(tarefa, "id", None),
                    "titulo": getattr(tarefa, "titulo", titulo),
                    "prioridade": getattr(tarefa, "prioridade", prioridade),
                    "status": getattr(tarefa, "status", status),
                })

            except Exception:
                pass

        return tarefa

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa internamente: {str(e)}", exc_info=True)
        return None
