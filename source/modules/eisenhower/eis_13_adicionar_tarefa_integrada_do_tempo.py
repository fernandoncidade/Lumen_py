from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
from uuid import uuid4
from source.utils.TaskIdentity import tasks_match
logger = LogManager.get_logger()

def _adicionar_tarefa_integrada_do_tempo(self, titulo: str, prioridade: str, date: str = None, time: str = None, description: str = None, file_path: str = None, task_id: str = None):
    try:
        lst = self._lista_por_prioridade(prioridade)
        if lst is None:
            return

        candidata = {
            "id": task_id,
            "text": titulo,
            "date": date,
            "time": time,
            "description": description,
            "priority": prioridade,
        }

        try:
            for i in range(lst.count()):
                it = lst.item(i)

                if not it:
                    continue

                if not (it.flags() & Qt.ItemIsSelectable):
                    continue

                data = it.data(Qt.UserRole) or {}
                atual = dict(data) if isinstance(data, dict) else {"text": (it.text() or "").strip()}

                if tasks_match(atual, candidata):
                    return

        except Exception:
            pass

        if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
            lst.clear()

        from PySide6.QtWidgets import QListWidgetItem

        display_text = titulo
        date_human = None

        if date:
            try:
                from PySide6.QtCore import QDate
                qd = QDate.fromString(date, Qt.ISODate)

                if qd.isValid() and hasattr(self, "date_input"):
                    date_human = qd.toString(self.date_input.displayFormat())

                else:
                    date_human = date

            except Exception:
                date_human = date

            if time:
                display_text = f"{titulo} — {date_human} {time}"

            else:
                display_text = f"{titulo} — {date_human}"

        task_item = QListWidgetItem(display_text)
        task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        task_item.setCheckState(Qt.Unchecked)
        task_item.setData(Qt.UserRole, {
            "id": task_id or str(uuid4()),
            "text": titulo,
            "date": date,
            "time": time,
            "description": description,
            "file_path": file_path,
            "prioridade": prioridade,
            "priority": prioridade,
        })

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
