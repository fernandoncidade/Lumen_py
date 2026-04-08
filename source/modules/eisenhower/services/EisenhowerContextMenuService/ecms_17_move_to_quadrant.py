from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _move_to_quadrant(self, item, source_list):
    try:
        opts = self._quadrant_options()
        chosen, ok = QInputDialog.getItem(
            self.app,
            self.get_text("Mover tarefa"),
            self.get_text("Selecione o quadrante:"),
            opts,
            0,
            False
        )
        if not ok or not chosen:
            return

        try:
            idx = opts.index(chosen)

        except ValueError:
            return

        keep_completed = self._is_completed_list(source_list)
        target = self._target_list_for_quadrant(idx, keep_completed=keep_completed)
        if target is None or target is source_list:
            return

        new_state = Qt.Checked if keep_completed else Qt.Unchecked

        source_list.blockSignals(True)
        target.blockSignals(True)

        try:
            self.app.move_item_between_lists(item, source_list, target, new_state)

        finally:
            source_list.blockSignals(False)
            target.blockSignals(False)

        self.app.save_tasks()
        if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
            self.app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao mover tarefa de quadrante via menu: {e}", exc_info=True)
