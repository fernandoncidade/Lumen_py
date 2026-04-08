from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _quadrant_options(self):
    try:
        return [
            self.app.quadrant1_label.text(),
            self.app.quadrant2_label.text(),
            self.app.quadrant3_label.text(),
            self.app.quadrant4_label.text(),
            self.app.quadrant1_completed_label.text(),
            self.app.quadrant2_completed_label.text(),
            self.app.quadrant3_completed_label.text(),
            self.app.quadrant4_completed_label.text(),
        ]

    except Exception as e:
        logger.error(f"Erro ao obter opções de quadrante: {e}", exc_info=True)
        return [
            "Quadrant 1",
            "Quadrant 2",
            "Quadrant 3",
            "Quadrant 4",
            "Quadrant 1 Completed",
            "Quadrant 2 Completed",
            "Quadrant 3 Completed",
            "Quadrant 4 Completed",
        ]
