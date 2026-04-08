from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_tudo(self, app=None):
    app = self._resolve_app(app)
    self._clear_all_lists(app)
    self._add_placeholders_after_clear(app)

    try:
        app.task_input.clear()

    except Exception:
        pass

    try:
        app.save_tasks()

        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao limpar tudo: {e}", exc_info=True)

    QMessageBox.information(app, self.get_text("Limpar"), self.get_text("Todos os dados foram removidos.") or "Todos os dados foram removidos.")
