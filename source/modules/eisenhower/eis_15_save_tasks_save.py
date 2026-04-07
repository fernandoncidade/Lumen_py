from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def save_tasks_save(self):
    try:
        def _list_to_entries(lst):
            entries = []
            if lst is None:
                return entries

            for i in range(lst.count()):
                item = lst.item(i)
                if item.flags() & Qt.ItemIsSelectable:
                    data = item.data(Qt.UserRole) or {}
                    text = data.get("text", item.text())
                    date = data.get("date")
                    time = data.get("time")
                    entry = {"text": text, "date": date, "time": time}

                    try:
                        file_path = data.get("file_path")
                        if file_path:
                            entry["file_path"] = file_path

                    except Exception as e:
                        logger.error(f"Erro ao obter o caminho do arquivo: {e}", exc_info=True)

                    try:
                        description = data.get("description")
                        if description:
                            entry["description"] = description

                    except Exception as e:
                        logger.error(f"Erro ao obter a descrição: {e}", exc_info=True)

                    try:
                        priority = data.get("priority")
                        if priority is not None:
                            entry["priority"] = priority

                    except Exception as e:
                        logger.error(f"Erro ao obter a prioridade: {e}", exc_info=True)

                    entries.append(entry)

            return entries

        tasks = {
            "quadrant1": _list_to_entries(getattr(self, 'quadrant1_list', None) or []),
            "quadrant1_completed": _list_to_entries(getattr(self, 'quadrant1_completed_list', None) or []),
            "quadrant2": _list_to_entries(getattr(self, 'quadrant2_list', None) or []),
            "quadrant2_completed": _list_to_entries(getattr(self, 'quadrant2_completed_list', None) or []),
            "quadrant3": _list_to_entries(getattr(self, 'quadrant3_list', None) or []),
            "quadrant3_completed": _list_to_entries(getattr(self, 'quadrant3_completed_list', None) or []),
            "quadrant4": _list_to_entries(getattr(self, 'quadrant4_list', None) or []),
            "quadrant4_completed": _list_to_entries(getattr(self, 'quadrant4_completed_list', None) or []),
        }

        if hasattr(self, '_eisenhower_worker') and getattr(self, '_eisenhower_worker') is not None:
            try:
                self._eisenhower_worker.request_save.emit(self.tasks_path, tasks)

            except Exception as e:
                logger.error(f"Erro ao emitir sinal de salvar: {e}", exc_info=True)
                globals()['save_tasks'](self)

        else:
            globals()['save_tasks'](self)

    except Exception as e:
        logger.error(f"Erro ao salvar tasks via thread: {e}", exc_info=True)
