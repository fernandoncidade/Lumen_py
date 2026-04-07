from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _executar_alerta(self, titulo, texto):
    try:
        self._sound_mgr.play_looping()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.finished.connect(lambda _: self._sound_mgr.stop())
        msg.exec()

    except Exception as e:
        logger.error(f"Erro ao executar alerta com som: {e}", exc_info=True)
        QMessageBox.information(self, titulo, texto)
        try:
            self._sound_mgr.stop()

        except Exception as e:
            logger.error(f"Erro ao parar som do alerta: {e}", exc_info=True)
