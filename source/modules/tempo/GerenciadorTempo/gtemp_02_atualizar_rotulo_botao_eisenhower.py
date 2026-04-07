from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _atualizar_rotulo_botao_eisenhower(self) -> None:
    try:
        if not hasattr(self, 'btn_eisenhower_integrado') or not self.btn_eisenhower_integrado:
            return

        # if self.btn_eisenhower_integrado.isChecked():
        #     self.btn_eisenhower_integrado.setText(QCoreApplication.translate("App", "🗂️ Matriz Eisenhower Conectada"))

        # else:
        #     self.btn_eisenhower_integrado.setText(QCoreApplication.translate("App", "🗂️ Matriz Eisenhower Desconectada"))

    except Exception as e:
        logger.debug(f"Falha ao atualizar rótulo do botão Eisenhower: {e}", exc_info=True)
