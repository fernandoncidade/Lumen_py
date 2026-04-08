from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_abas(self):
    try:
        if hasattr(self, "input_titulo"):
            try:
                self.input_titulo.clear()

            except Exception:
                pass

        if hasattr(self, "texto_explicacao"):
            try:
                self.texto_explicacao.clear()

            except Exception:
                pass

        if hasattr(self, "texto_lacunas"):
            try:
                self.texto_lacunas.clear()

            except Exception:
                pass

        if hasattr(self, "texto_revisao"):
            try:
                self.texto_revisao.clear()

            except Exception:
                pass

        try:
            if hasattr(self, "input_titulo"):
                self.input_titulo.setFocus()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao limpar abas do MetodoFeynman: {e}", exc_info=True)

def adicionar_botao_limpar(self):
    try:
        label = QCoreApplication.translate("App", "🧽 Limpar")
        btn = None

        try:
            if hasattr(self, 'gerenciador_botoes') and self.gerenciador_botoes is not None:
                btn = self.gerenciador_botoes.create_button()

                try:
                    self.gerenciador_botoes.set_button_text(btn, label)

                except Exception:
                    btn.setText(label)

        except Exception:
            btn = None

        if btn is None:
            btn = QPushButton(label, self)

            try:
                fm = btn.fontMetrics()
                min_w = 3 * fm.horizontalAdvance('m')
                btn.setMinimumWidth(min_w)

            except Exception:
                pass

        btn.clicked.connect(lambda: limpar_abas(self))

        try:
            btn.setParent(self)

        except Exception:
            pass

        self.btn_limpar = btn

    except Exception as e:
        logger.error(f"Erro ao adicionar botão Limpar: {e}", exc_info=True)
