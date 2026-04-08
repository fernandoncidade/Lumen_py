from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _target_list_for_quadrant(self, quadrant_index: int, keep_completed: bool | None = False):
    try:
        pending = [self.app.quadrant1_list, self.app.quadrant2_list, self.app.quadrant3_list, self.app.quadrant4_list]
        done = [self.app.quadrant1_completed_list, self.app.quadrant2_completed_list, self.app.quadrant3_completed_list, self.app.quadrant4_completed_list]

        if 0 <= quadrant_index < 4:
            if keep_completed is None:
                return pending[quadrant_index]

            return done[quadrant_index] if keep_completed else pending[quadrant_index]

        if 4 <= quadrant_index < 8:
            return done[quadrant_index - 4]

        return None

    except Exception as e:
        logger.error(f"Erro ao obter lista alvo para quadrante {quadrant_index}: {e}", exc_info=True)
        return None
