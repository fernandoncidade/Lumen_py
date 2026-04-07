from PySide6.QtCore import QObject, Signal, Slot
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class FeynmanWorker(QObject):
    request_load = Signal(str)
    request_save = Signal(str, object)
    conceitos_loaded = Signal(object)
    save_finished = Signal(bool)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.request_load.connect(self._load)
        self.request_save.connect(self._save)

    @Slot(str)
    def _load(self, arquivo_conceitos):
        try:
            import os, json
            if arquivo_conceitos and os.path.exists(arquivo_conceitos):
                with open(arquivo_conceitos, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.conceitos_loaded.emit(dados if isinstance(dados, list) else [])

            else:
                self.conceitos_loaded.emit([])

        except Exception as e:
            logger.error(f"Erro no worker (Feynman): {str(e)}", exc_info=True)

    @Slot(str, object)
    def _save(self, arquivo_conceitos, conceitos):
        try:
            import json, os
            if not arquivo_conceitos:
                self.save_finished.emit(False)
                return

            dirp = os.path.dirname(arquivo_conceitos)
            if dirp and not os.path.exists(dirp):
                try:
                    os.makedirs(dirp, exist_ok=True)

                except Exception:
                    pass

            with open(arquivo_conceitos, 'w', encoding='utf-8') as f:
                json.dump(conceitos or [], f, ensure_ascii=False, indent=4)

            self.save_finished.emit(True)

        except Exception as e:
            logger.error(f"Erro no worker (Feynman): {str(e)}", exc_info=True)
