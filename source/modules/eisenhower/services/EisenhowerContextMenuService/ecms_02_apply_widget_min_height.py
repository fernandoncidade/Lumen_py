from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _apply_widget_min_height(self, widget, name: str | None = None):
    try:
        h = self._compute_widget_height(widget, name)
        widget.setMinimumHeight(h)

    except Exception as e:
        logger.error(f"Falha ao aplicar altura mínima no widget {name}: {e}", exc_info=True)
