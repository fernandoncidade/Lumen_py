from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def ativar_regua_foco(self):
    try:
        if self.regua is None or not self.regua.isVisible():
            from source.modules.mod_02_regua_foco import ReguaFoco
            self.regua = ReguaFoco()

            anchor_global = self.texto_area.mapToGlobal(self.texto_area.viewport().rect().topLeft())
            tela = QApplication.screenAt(anchor_global)

            if tela is None:
                telas = QApplication.screens()
                tela = telas[0] if telas else None

            largura_inicial = min(self.texto_area.viewport().width(), 1400)
            altura_inicial = 80

            if tela:
                geo = tela.geometry()

                x = anchor_global.x()

                if x + largura_inicial > geo.right() - 10:
                    x = geo.right() - largura_inicial - 10

                if x < geo.x() + 10:
                    x = geo.x() + 10

                y = anchor_global.y() + 5

                if y < geo.y() + 10:
                    y = geo.y() + 10

                if y + altura_inicial > geo.bottom() - 10:
                    y = geo.bottom() - altura_inicial - 10

                self.regua.setGeometry(x, y, largura_inicial, altura_inicial)

            self.regua.destroyed.connect(self.regua_fechada)
            self.regua.show()

            self.gerenciador_botoes.set_button_text(self.btn_regua, QCoreApplication.translate("App", "📏 Desativar Régua de Foco"))
            self.btn_regua.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
            MessageBox.leitor_focus_ruler_activated(self)

    except Exception as e:
        logger.error(f"Erro ao ativar régua de foco: {str(e)}", exc_info=True)
