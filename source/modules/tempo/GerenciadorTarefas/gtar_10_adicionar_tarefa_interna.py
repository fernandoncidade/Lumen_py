from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def _adicionar_tarefa_interna(self, titulo: str, prioridade: str, status: str = "Todo", emitir_sinal: bool = True, description: str = None, file_path: str = None, date: str = None, time: str = None):
    try:
        tarefa = Tarefa(titulo, descricao=(description or ""), prioridade=prioridade, status=status, file_path=(file_path or None), date=(date or None), time=(time or None))
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
                    "description": getattr(tarefa, "descricao", None) or None,
                    "file_path": getattr(tarefa, "file_path", None),
                    "date": getattr(tarefa, "date", None),
                    "time": getattr(tarefa, "time", None),
                })

            except Exception:
                pass

        return tarefa

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa internamente: {str(e)}", exc_info=True)
        return None
