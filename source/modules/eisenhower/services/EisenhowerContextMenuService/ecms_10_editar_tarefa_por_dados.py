from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def editar_tarefa_por_dados(self, task_data: dict):
    try:
        if not isinstance(task_data, dict):
            return

        src_list, src_item = self._find_source_item_for_calendar(task_data)
        if src_item is None:
            return

        self.editar_tarefa_item(src_item, src_list)

    except Exception as e:
        logger.error(f"Erro ao editar tarefa via dados: {e}", exc_info=True)
