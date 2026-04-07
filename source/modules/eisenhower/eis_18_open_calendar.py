from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def open_calendar(self):
    try:
        if hasattr(self, "calendar_pane") and self.calendar_pane:
            self.calendar_pane.toggle_panel(open_if_hidden=True)

    except Exception as e:
        logger.error(f"Erro ao abrir calendário: {e}", exc_info=True)
