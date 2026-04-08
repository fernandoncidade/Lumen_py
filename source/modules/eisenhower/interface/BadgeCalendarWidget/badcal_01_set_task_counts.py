from PySide6.QtCore import Qt, QDate
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def set_task_counts(self, dates_list):
    try:
        from collections import Counter

        dates_list = dates_list or []
        self._task_counts = Counter(dates_list)

        week_counter = Counter()
        for date_str in dates_list:
            qd = QDate.fromString(date_str, Qt.ISODate)
            if qd.isValid():
                week_num = qd.weekNumber()[0]
                year = qd.year()
                week_counter[(year, week_num)] += 1

        self._week_counts = dict(week_counter)

        month_counter = Counter()
        for date_str in dates_list:
            qd = QDate.fromString(date_str, Qt.ISODate)
            if qd.isValid():
                month_counter[(qd.year(), qd.month())] += 1

        self._month_counts = dict(month_counter)
        self.updateCells()

    except Exception as e:
        logger.error(f"Erro ao definir contadores de tarefas: {e}", exc_info=True)
