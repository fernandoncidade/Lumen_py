from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mover_tarefas_marcadas(self):
    try:
        selecionados = []
        for lista in (self.col_todo.lista, self.col_doing.lista, self.col_done.lista):
            try:
                for it in lista.selectedItems() or []:
                    tid = it.data(Qt.UserRole)
                    titulo = (
                        it.text().split('\n')[0]
                        .replace('🔴 ', '')
                        .replace('🟠 ', '')
                        .replace('🟡 ', '')
                        .replace('🟢 ', '')
                    )
                    selecionados.append((tid, titulo))

            except Exception:
                pass

            for i in range(lista.count()):
                it = lista.item(i)
                if it.checkState() == Qt.Checked:
                    tid = it.data(Qt.UserRole)
                    titulo = (
                        it.text().split('\n')[0]
                        .replace('🔴 ', '')
                        .replace('🟠 ', '')
                        .replace('🟡 ', '')
                        .replace('🟢 ', '')
                    )
                    selecionados.append((tid, titulo))

        if not selecionados:
            return

        opcoes = [
            QCoreApplication.translate("App", "📋 A Fazer"),
            QCoreApplication.translate("App", "⚙️ Em Progresso"),
            QCoreApplication.translate("App", "✅ Concluído")
        ]
        destino_exibido, ok = QInputDialog.getItem(
            self,
            QCoreApplication.translate("App", "Mover Tarefas"),
            QCoreApplication.translate("App", "Selecione a coluna de destino:"),
            opcoes,
            0,
            False
        )
        if not ok or not destino_exibido:
            return

        mapa_destino = {
            QCoreApplication.translate("App", "📋 A Fazer"): "Todo",
            QCoreApplication.translate("App", "⚙️ Em Progresso"): "Doing",
            QCoreApplication.translate("App", "✅ Concluído"): "Done"
        }
        status_destino = mapa_destino.get(destino_exibido, "Todo")

        ids_set = {tid for tid, _ in selecionados if tid}
        titulos_set = {titulo for tid, titulo in selecionados if not tid}

        for tarefa in self.tarefas:
            if getattr(tarefa, 'id', None) in ids_set or tarefa.titulo in titulos_set:
                tarefa.status = status_destino

        self.salvar_tarefas()
        self.atualizar_listas()
    
    except Exception as e:
        logger.error(f"Erro ao mover tarefas marcadas: {str(e)}", exc_info=True)
