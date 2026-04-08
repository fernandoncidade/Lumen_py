import os
from source.utils.LogManager import LogManager
from .lta_26_pdf_view import PDFView
logger = LogManager.get_logger()


class FileDropPDFView(PDFView):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.setAcceptDrops(True)

        try:
            self.viewport().setAcceptDrops(True)

        except Exception:
            pass

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

                    if path and path.lower().endswith(".pdf") and os.path.isfile(path):
                        try:
                            if hasattr(self._app, "carregar_pdf"):
                                self._app.carregar_pdf(path, keep_pdf_tab=True)

                            self.setToolTip(path)

                        except Exception:
                            pass

                        event.acceptProposedAction()
                        return

        except Exception:
            logger.error("Erro ao processar drop no FileDropPDFView", exc_info=True)

        super().dropEvent(event)
