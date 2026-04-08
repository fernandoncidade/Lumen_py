from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication, Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def deletar_conceito(self):
    try:
        items = self.lista_conceitos.selectedItems()
        if not items:
            return

        titulos = []
        for it in items:
            try:
                payload = it.data(Qt.UserRole)

                if isinstance(payload, dict):
                    t = payload.get('titulo')

                else:
                    t = None

            except Exception:
                t = None

            if not t:
                t = it.text().split(' - ')[0].replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '').strip()

            if t:
                titulos.append(t)

        titulos = list(dict.fromkeys(titulos))
        if not titulos:
            return

        msg = QMessageBox(self)
        msg.setWindowTitle(QCoreApplication.translate("App", "Confirmar Exclusão"))

        if len(titulos) == 1:
            texto = QCoreApplication.translate("App", "Deseja realmente deletar o conceito '{titulo}'?").format(titulo=titulos[0])

        else:
            texto = QCoreApplication.translate("App", "Deseja realmente deletar os {n} conceitos selecionados?").format(n=len(titulos))

        msg.setText(texto)
        btn_yes = msg.addButton(QCoreApplication.translate("App", "Yes"), QMessageBox.YesRole)
        btn_no = msg.addButton(QCoreApplication.translate("App", "No"), QMessageBox.NoRole)
        msg.exec()

        if msg.clickedButton() == btn_yes:
            titulos_set = set(t.lower() for t in titulos)
            self.conceitos = [c for c in self.conceitos if c.get('titulo', '').lower() not in titulos_set]
            self.salvar_conceitos()
            self.atualizar_lista()
            self.limpar_campos()

    except Exception as e:
        logger.error(f"Erro ao deletar conceito: {str(e)}", exc_info=True)
