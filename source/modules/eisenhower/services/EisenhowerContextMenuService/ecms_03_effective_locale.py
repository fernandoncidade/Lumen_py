from PySide6.QtCore import QLocale
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _effective_locale(self) -> QLocale:
    try:
        if hasattr(self.app, "date_input") and self.app.date_input is not None:
            return self.app.date_input.locale()

    except Exception as e:
        logger.error(f"Falha ao obter locale efetivo do date_input: {e}", exc_info=True)

    try:
        if hasattr(self.app, "gerenciador_traducao"):
            idioma = self.app.gerenciador_traducao.obter_idioma_atual()
            if idioma and idioma.startswith("pt"):
                return QLocale(QLocale.Portuguese, QLocale.Brazil)

            if idioma and idioma.startswith("en"):
                return QLocale(QLocale.English, QLocale.UnitedStates)

    except Exception as e:
        logger.error(f"Falha ao obter locale efetivo do gerenciador de tradução: {e}", exc_info=True)

    return QLocale.system()
