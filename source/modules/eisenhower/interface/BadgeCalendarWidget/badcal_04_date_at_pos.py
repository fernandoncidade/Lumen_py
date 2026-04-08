from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Qt, QDate
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _date_at_pos(self, pos):
    try:
        if hasattr(self, "dateAt"):
            try:
                qd = self.dateAt(pos)
                if isinstance(qd, QDate) and qd.isValid():
                    return qd

            except Exception:
                pass

        view = self.findChild(QAbstractItemView)
        if view is not None:
            vpos = view.mapFrom(self, pos)
            idx = view.indexAt(vpos)
            if idx.isValid():
                for role in (Qt.UserRole, Qt.UserRole + 1, Qt.UserRole + 2, Qt.DisplayRole):
                    try:
                        val = idx.data(role)
                        if isinstance(val, QDate) and val.isValid():
                            return val

                    except Exception:
                        pass

                try:
                    day_val = idx.data(Qt.DisplayRole)
                    day = int(day_val)
                    if day > 0:
                        qd = QDate(self.yearShown(), self.monthShown(), day)
                        if qd.isValid():
                            return qd

                except Exception:
                    pass

    except Exception as e:
        logger.error(f"Erro ao obter data pelo mouse no calendário: {e}", exc_info=True)

    return None
