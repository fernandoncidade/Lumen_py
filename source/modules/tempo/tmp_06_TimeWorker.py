from PySide6.QtCore import QObject, Signal, Slot
from source.utils.LogManager import LogManager


class _TimeWorker(QObject):
    pomodoro_completed = Signal(str)

    def __init__(self):
        super().__init__()
        self.logger = LogManager.get_logger()
        self._running = True

    @Slot(str)
    def on_pomodoro(self, tipo: str):
        try:
            self.logger.debug(f"Worker de tempo recebeu evento de pomodoro: {tipo}")
            self.pomodoro_completed.emit(tipo)

        except Exception as e:
            try:
                self.logger.error(f"Erro no TimeWorker.on_pomodoro: {e}", exc_info=True)

            except Exception:
                pass

    @Slot()
    def stop(self):
        try:
            self._running = False

        except Exception:
            pass
