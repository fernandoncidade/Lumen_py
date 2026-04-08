from PySide6.QtCore import Qt
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def remover_todas_por_data(self, date_iso: str) -> int:
    try:
        if not date_iso:
            return 0

        try:
            if not MessageBox.eisen_confirm_remove_tasks_by_day(self.app):
                return 0

        except Exception:
            pass

        removed = 0
        lists = [
            getattr(self.app, "quadrant1_list", None),
            getattr(self.app, "quadrant2_list", None),
            getattr(self.app, "quadrant3_list", None),
            getattr(self.app, "quadrant4_list", None),
            getattr(self.app, "quadrant1_completed_list", None),
            getattr(self.app, "quadrant2_completed_list", None),
            getattr(self.app, "quadrant3_completed_list", None),
            getattr(self.app, "quadrant4_completed_list", None),
        ]

        for lst in lists:
            if lst is None:
                continue

            for i in range(lst.count() - 1, -1, -1):
                it = lst.item(i)

                if not it or not (it.flags() & Qt.ItemIsSelectable):
                    continue

                data = it.data(Qt.UserRole) or {}

                if (data.get("date") or "") == date_iso:
                    try:
                        lst.takeItem(i)
                        removed += 1

                    except Exception:
                        pass

        try:
            if hasattr(self.app, "cleanup_time_groups"):
                for lst in lists:
                    if lst is not None:
                        self.app.cleanup_time_groups(lst)

        except Exception:
            pass

        try:
            if hasattr(self.app, "atualizar_placeholders"):
                self.app.atualizar_placeholders()

        except Exception:
            pass

        try:
            self.app.save_tasks()

        except Exception:
            pass

        try:
            if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
                self.app.calendar_pane.calendar_panel.update_task_list()

        except Exception:
            pass

        if removed > 0:
            try:
                MessageBox.eisen_remove_tasks_success(self.app, removed)

            except Exception:
                pass

        return removed

    except Exception as e:
        logger.error(f"Erro ao remover todas as tarefas por data: {e}", exc_info=True)
        return 0
