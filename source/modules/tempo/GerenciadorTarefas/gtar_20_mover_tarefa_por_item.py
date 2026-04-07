from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mover_tarefa_por_item(self, item):
    try:
        if not item:
            return

        tarefa_id = item.data(Qt.UserRole)
        titulo_item = (
            item.text().split('\n')[0]
            .replace('🔴 ', '')
            .replace('🟠 ', '')
            .replace('🟡 ', '')
            .replace('🟢 ', '')
        )

        alvo = None
        for t in self.tarefas:
            if (tarefa_id and getattr(t, 'id', None) == tarefa_id) or (t.titulo == titulo_item):
                alvo = t
                break

        if not alvo:
            return

        opcoes = [
            QCoreApplication.translate("App", "📋 A Fazer"),
            QCoreApplication.translate("App", "⚙️ Em Progresso"),
            QCoreApplication.translate("App", "✅ Concluído")
        ]

        destino_exibido, ok = QInputDialog.getItem(
            self,
            QCoreApplication.translate("App", "Mover Tarefa"),
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
        alvo.status = mapa_destino.get(destino_exibido, "Todo")

        self.salvar_tarefas()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao mover tarefa por item (menu): {str(e)}", exc_info=True)
