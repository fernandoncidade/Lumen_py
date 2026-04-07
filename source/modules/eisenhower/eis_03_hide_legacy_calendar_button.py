from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QPushButton
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def _hide_legacy_calendar_button(self):
    try:
        for btn in self.findChildren(QPushButton):
            if btn.text().strip().lower() in {get_text("Calendário").strip().lower(), "calendário", "calendario", "calendar"}:
                btn.hide()

    except Exception as e:
        logger.error(f"Erro ao ocultar botão legado do calendário: {e}", exc_info=True)
