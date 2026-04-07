from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mover_tarefa(self, item, status_atual):
    try:
        tarefa_id = item.data(Qt.UserRole)
        alvo = None
        for tarefa in self.tarefas:
            if getattr(tarefa, 'id', None) == tarefa_id:
                alvo = tarefa
                break

        if not alvo:
            texto = (
                item.text().split('\n')[0]
                .replace('🔴 ', '')
                .replace('🟠 ', '')
                .replace('🟡 ', '')
                .replace('🟢 ', '')
            )
            for tarefa in self.tarefas:
                if tarefa.titulo == texto:
                    alvo = tarefa
                    break

        if not alvo:
            return

        if status_atual == "Todo":
            alvo.status = "Doing"

        elif status_atual == "Doing":
            alvo.status = "Done"

        else:
            alvo.status = "Todo"

        self.salvar_tarefas()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao mover tarefa: {str(e)}", exc_info=True)
