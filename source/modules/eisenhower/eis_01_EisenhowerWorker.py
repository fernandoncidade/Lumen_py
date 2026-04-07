from PySide6.QtCore import QObject, Signal, Slot
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class _EisenhowerWorker(QObject):
    request_save = Signal(str, object)
    save_finished = Signal(bool)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.request_save.connect(self._save)

    @Slot(str, object)
    def _save(self, path, tasks):
        try:
            import json, os
            if not path:
                self.save_finished.emit(False)
                return

            dirp = os.path.dirname(path)
            if dirp and not os.path.exists(dirp):
                try:
                    os.makedirs(dirp, exist_ok=True)

                except Exception:
                    pass

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(tasks or {}, f, ensure_ascii=False, indent=2)

            self.save_finished.emit(True)

        except Exception as e:
            self.error.emit(str(e))
