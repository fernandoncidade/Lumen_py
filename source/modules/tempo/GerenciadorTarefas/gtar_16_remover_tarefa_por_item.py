from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QCoreApplication
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

        try:
            QMessageBox.information(
                self,
                QCoreApplication.translate("App", "Sucesso"),
                QCoreApplication.translate("App", "Tarefa removida com sucesso!")
            )

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao remover tarefa pelo menu de contexto: {str(e)}", exc_info=True)
