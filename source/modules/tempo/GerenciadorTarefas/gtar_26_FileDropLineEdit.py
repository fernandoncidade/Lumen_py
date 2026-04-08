import os
from PySide6.QtWidgets import QLineEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class FileDropLineEdit(QLineEdit):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        try:
            md = event.mimeData()
            if md.hasUrls():
                event.acceptProposedAction()

            else:
                super().dragEnterEvent(event)

        except Exception:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        try:
            md = event.mimeData()
            if md.hasUrls():
                event.acceptProposedAction()

            else:
                super().dragMoveEvent(event)

        except Exception:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        try:
            md = event.mimeData()
            if md.hasUrls():
                urls = md.urls()
                if urls:
                    path = urls[0].toLocalFile()
                    if path:
                        try:
                            self.setText(os.path.basename(path))
                            setattr(self._app, "_dragged_file_path", path)
                            self.setToolTip(path)

                        except Exception:
                            pass

                event.acceptProposedAction()
                return

        except Exception:
            logger.error("Erro ao processar drop no campo de tarefa", exc_info=True)

        super().dropEvent(event)
