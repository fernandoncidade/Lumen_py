from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def atualizar_listas(self):
    try:
        self.col_todo.lista.clear()
        self.col_doing.lista.clear()
        self.col_done.lista.clear()

        for tarefa in self.tarefas:
            prioridade_norm = Tarefa.normalizar_prioridade(getattr(tarefa, 'prioridade', 'Importante e Urgente'))
            emoji = {
                "Importante e Urgente": "🔴",
                "Importante, mas Não Urgente": "🟠",
                "Não Importante, mas Urgente": "🟡",
                "Não Importante e Não Urgente": "🟢",
            }.get(prioridade_norm, "🔴")
            pomodoros_texto = QCoreApplication.translate("App", "🍅 {n} pomodoros").format(n=tarefa.pomodoros_completados)
            texto = f"{emoji} {tarefa.titulo}\n{pomodoros_texto}"

            item = QListWidgetItem(texto)

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsDragEnabled
                | Qt.ItemIsDropEnabled
            )
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, getattr(tarefa, 'id', None))

            if tarefa.status == "Todo":
                self.col_todo.lista.addItem(item)

            elif tarefa.status == "Doing":
                self.col_doing.lista.addItem(item)

            else:
                self.col_done.lista.addItem(item)

        self.listas_atualizadas.emit()

    except Exception as e:
        logger.error(f"Erro ao atualizar listas de tarefas: {str(e)}", exc_info=True)
