from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def load_tasks_load(self):
    try:
        try:
            from source.modules.eisenhower import load_tasks as _load_tasks

        except Exception:
            _load_tasks = globals().get('load_tasks')

        if _load_tasks:
            _load_tasks(self)

        else:
            logger.debug('load_tasks não disponível no momento para chamada')

    except Exception as e:
        logger.error(f"Erro ao chamar load_tasks: {e}", exc_info=True)

    try:
        if hasattr(self, "calendar_pane") and self.calendar_pane:
            self.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao carregar tarefas: {e}", exc_info=True)
