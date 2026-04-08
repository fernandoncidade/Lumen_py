from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_tarefa_item(self, item, list_widget=None, confirm: bool = True) -> bool:
    try:
        if item is None:
            return False

        lst = list_widget or item.listWidget()
        if lst is None:
            return False

        data = item.data(Qt.UserRole) or {}
        if isinstance(data, dict) and data.get("category"):
            src_list, src_item = self._find_source_item_for_calendar(data)
            if src_list is not None and src_item is not None:
                removed = self.app.remove_task(src_item, src_list, confirm)
            else:
                removed = self.app.remove_task(item, lst, confirm)

        else:
            removed = self.app.remove_task(item, lst, confirm)

        if removed:
            try:
                self.app.save_tasks()

            except Exception:
                pass

            try:
                if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
                    self.app.calendar_pane.calendar_panel.update_task_list()

            except Exception:
                pass

        return bool(removed)

    except Exception as e:
        logger.error(f"Erro ao remover tarefa via menu: {e}", exc_info=True)
        return False
