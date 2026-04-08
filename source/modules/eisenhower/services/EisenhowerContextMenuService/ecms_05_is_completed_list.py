from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _is_completed_list(self, lst) -> bool:
    try:
        return lst in (
            self.app.quadrant1_completed_list,
            self.app.quadrant2_completed_list,
            self.app.quadrant3_completed_list,
            self.app.quadrant4_completed_list,
        )

    except Exception as e:
        logger.error(f"Falha ao verificar se a lista é de concluídos: {e}", exc_info=True)
        return False
