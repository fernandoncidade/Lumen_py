from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_tarefa_por_item(self, item):
    try:
        tarefa_id = item.data(Qt.UserRole)
        if tarefa_id:
            self.tarefas = [t for t in self.tarefas if getattr(t, 'id', None) != tarefa_id]

        else:
            titulo = (
                item.text().split('\n')[0]
                .replace('🔴 ', '')
                .replace('🟠 ', '')
                .replace('🟡 ', '')
                .replace('🟢 ', '')
            )
            self.tarefas = [t for t in self.tarefas if t.titulo != titulo]

        self.salvar_tarefas()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao remover tarefa pelo menu de contexto: {str(e)}", exc_info=True)
