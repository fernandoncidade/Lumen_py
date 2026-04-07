from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remove_task_remove(self, item, list_widget, confirm: bool = True):
    try:
        try:
            from source.modules.eisenhower import remove_task as _remove_task

        except Exception:
            _remove_task = globals().get('remove_task')

        if _remove_task:
            removed = _remove_task(self, item, list_widget, confirm)

        else:
            removed = False

    except Exception as e:
        logger.error(f"Erro ao chamar utilitário remove_task: {e}", exc_info=True)
        removed = False

    try:
        self.cleanup_time_groups(list_widget)
        if hasattr(self, "calendar_pane") and self.calendar_pane:
            self.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao remover tarefa: {e}", exc_info=True)

    return removed
