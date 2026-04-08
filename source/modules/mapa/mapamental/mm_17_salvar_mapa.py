from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QCoreApplication
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def salvar_mapa(self):
    try:
        arquivo, _ = QFileDialog.getSaveFileName(
            self, 
            QCoreApplication.translate("App", "Salvar Mapa Mental"), 
            os.path.join(self.caminho_persistente, "mapa_mental.json"), 
            QCoreApplication.translate("App", "JSON Files (*.json)")
        )

        if arquivo:
            self._salvar_mapa_em_arquivo(arquivo)

    except Exception as e:
        logger.error(f"Erro ao salvar mapa mental: {str(e)}", exc_info=True)
