from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _sincronizar_status_pos_movimento(self, prioridade_lista=None):
    try:
        if not hasattr(self, 'tarefas'):
            return

        mapping = {}

        try:
            mapping[self.col_todo.lista] = "Todo"
            mapping[self.col_doing.lista] = "Doing"
            mapping[self.col_done.lista] = "Done"

        except Exception:
            return

        alterou = False

        items = list(mapping.items())
        if prioridade_lista in mapping:
            items = [it for it in items if it[0] is not prioridade_lista] + [(prioridade_lista, mapping[prioridade_lista])]

        for lst, status in items:
            for i in range(lst.count()):
                it = lst.item(i)
                if not it:
                    continue

                tid = it.data(Qt.UserRole)
                titulo = (
                    it.text().split('\n')[0]
                    .replace('🔴 ', '')
                    .replace('🟠 ', '')
                    .replace('🟡 ', '')
                    .replace('🟢 ', '')
                )

                for t in self.tarefas:
                    if (tid and getattr(t, 'id', None) == tid) or (not tid and t.titulo == titulo):
                        if getattr(t, 'status', None) != status:
                            t.status = status
                            alterou = True

                        break

        if alterou:
            self.salvar_tarefas()

    except Exception as e:
        logger.error(f"Erro ao sincronizar status após movimento: {str(e)}", exc_info=True)
