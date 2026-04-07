from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_tarefas_marcadas(self):
    try:
        ids_para_remover = set()
        titulos_para_remover = set()

        for lista in (self.col_todo.lista, self.col_doing.lista, self.col_done.lista):
            for i in range(lista.count()):
                it = lista.item(i)
                if it.checkState() == Qt.Checked:
                    tid = it.data(Qt.UserRole)
                    if tid:
                        ids_para_remover.add(tid)

                    else:
                        titulo = (
                            it.text().split('\n')[0]
                            .replace('🔴 ', '')
                            .replace('🟠 ', '')
                            .replace('🟡 ', '')
                            .replace('🟢 ', '')
                        )
                        titulos_para_remover.add(titulo)

        if not ids_para_remover and not titulos_para_remover:
            return

        novas = []
        for t in self.tarefas:
            if getattr(t, 'id', None) in ids_para_remover:
                continue

            if t.titulo in titulos_para_remover:
                continue

            novas.append(t)

        self.tarefas = novas
        self.salvar_tarefas()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao remover tarefas marcadas: {str(e)}", exc_info=True)
