from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _compute_widget_height(self, widget, name: str | None = None) -> int:
    try:
        if hasattr(self.app, "widget_heights") and isinstance(self.app.widget_heights, dict) and name in self.app.widget_heights:
            v = int(self.app.widget_heights.get(name) or 0)
            if v > 0:
                return v

        if hasattr(self.app, "widget_height_override") and isinstance(self.app.widget_height_override, int) and self.app.widget_height_override > 0:
            return int(self.app.widget_height_override)

        fm = widget.fontMetrics()
        return max(26, int(fm.height() * 1.2))

    except Exception as e:
        logger.error(f"Falha ao calcular altura do widget {name}: {e}", exc_info=True)
        return 28
