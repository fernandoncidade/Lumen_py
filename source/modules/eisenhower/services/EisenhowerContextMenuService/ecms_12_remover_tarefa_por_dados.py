from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_tarefa_por_dados(self, task_data: dict, confirm: bool = True) -> bool:
    try:
        if not isinstance(task_data, dict):
            return False

        src_list, src_item = self._find_source_item_for_calendar(task_data)
        if src_item is None or src_list is None:
            return False

        return self.remover_tarefa_item(src_item, src_list, confirm)

    except Exception as e:
        logger.error(f"Erro ao remover tarefa via dados: {e}", exc_info=True)
        return False
