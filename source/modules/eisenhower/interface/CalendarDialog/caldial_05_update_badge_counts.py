from PySide6.QtCore import Qt, QDate
from source.modules.eisenhower.interface.CalendarDialog.caldial_03_collect_tasks import _collect_tasks
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _update_badge_counts(self):
    try:
        dates = []
        for task in _collect_tasks(self):
            ds = task.get("date")
            if ds:
                qd = QDate.fromString(ds, Qt.ISODate)
                if qd.isValid():
                    dates.append(ds)

        self.calendar.set_task_counts(dates)

    except Exception as e:
        logger.error(f"Erro ao atualizar contadores de badges: {e}", exc_info=True)
