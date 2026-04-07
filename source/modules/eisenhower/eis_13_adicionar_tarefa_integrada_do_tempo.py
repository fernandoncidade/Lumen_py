from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _adicionar_tarefa_integrada_do_tempo(self, titulo: str, prioridade: str):
    try:
        lst = self._lista_por_prioridade(prioridade)
        if lst is None:
            return

        try:
            for i in range(lst.count()):
                it = lst.item(i)
                if not it:
                    continue

                if not (it.flags() & Qt.ItemIsSelectable):
                    continue

                data = it.data(Qt.UserRole) or {}
                base = (data.get("text") or it.text() or "").strip()
                if base == titulo:
                    return

        except Exception:
            pass

        if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
            lst.clear()

        from PySide6.QtWidgets import QListWidgetItem
        task_item = QListWidgetItem(titulo)
        task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        task_item.setCheckState(Qt.Unchecked)
        task_item.setData(Qt.UserRole, {"text": titulo, "date": None, "time": None})

        if hasattr(self, "insert_task_into_quadrant_list"):
            self.insert_task_into_quadrant_list(lst, task_item)

        else:
            lst.addItem(task_item)

        try:
            self.save_tasks()

        except Exception:
            pass

        try:
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.calendar_panel.update_task_list()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa integrada do Tempo: {e}", exc_info=True)
