import os
from PySide6.QtWidgets import QTextEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class FileDropEdit(QTextEdit):
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

                    if path and path.lower().endswith(".pdf"):
                        try:
                            if hasattr(self._app, "carregar_pdf"):
                                self._app.carregar_pdf(path)

                            self.setToolTip(path)

                        except Exception:
                            pass

                        event.acceptProposedAction()
                        return

        except Exception:
            logger.error("Erro ao processar drop no FileDropEdit", exc_info=True)

        super().dropEvent(event)
