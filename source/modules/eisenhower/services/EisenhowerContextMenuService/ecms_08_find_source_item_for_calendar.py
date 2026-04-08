from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _find_source_item_for_calendar(self, task_dict):
    try:
        if not isinstance(task_dict, dict):
            return None, None

        cat = task_dict.get("category")
        if not cat:
            return None, None

        completed = bool(task_dict.get("completed"))
        labels = [
            getattr(self.app, "quadrant1_label", None).text() if getattr(self.app, "quadrant1_label", None) is not None else None,
            getattr(self.app, "quadrant2_label", None).text() if getattr(self.app, "quadrant2_label", None) is not None else None,
            getattr(self.app, "quadrant3_label", None).text() if getattr(self.app, "quadrant3_label", None) is not None else None,
            getattr(self.app, "quadrant4_label", None).text() if getattr(self.app, "quadrant4_label", None) is not None else None,
        ]
        pending = [getattr(self.app, "quadrant1_list", None), getattr(self.app, "quadrant2_list", None), getattr(self.app, "quadrant3_list", None), getattr(self.app, "quadrant4_list", None)]
        done = [getattr(self.app, "quadrant1_completed_list", None), getattr(self.app, "quadrant2_completed_list", None), getattr(self.app, "quadrant3_completed_list", None), getattr(self.app, "quadrant4_completed_list", None)]

        for idx, label in enumerate(labels):
            try:
                if not label:
                    continue

                if not str(cat).startswith(label):
                    continue

                src_list = done[idx] if completed else pending[idx]
                if src_list is None:
                    continue

                for i in range(src_list.count()):
                    it = src_list.item(i)
                    if not it:
                        continue

                    if not (it.flags() & Qt.ItemIsSelectable):
                        continue

                    d = it.data(Qt.UserRole) or {}
                    if (str(d.get("text") or "").strip() == str(task_dict.get("text") or "").strip()) and (d.get("date") or "") == (task_dict.get("date") or "") and (d.get("time") or "") == (task_dict.get("time") or ""):
                        return src_list, it

            except Exception as e:
                logger.error(f"Erro ao encontrar item fonte para calendário: {e}", exc_info=True)
                continue

    except Exception as e:
        logger.error(f"Erro ao encontrar item fonte para calendário: {e}", exc_info=True)

    return None, None
