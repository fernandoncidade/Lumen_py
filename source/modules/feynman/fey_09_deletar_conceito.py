from PySide6.QtCore import Qt
from source.utils.MessageBox import MessageBox
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

        if MessageBox.feynman_confirm_delete_concepts(self, titulos):
            total_antes = len(getattr(self, "conceitos", []) or [])
            titulos_set = set(t.lower() for t in titulos)
            self.conceitos = [c for c in self.conceitos if c.get('titulo', '').lower() not in titulos_set]
            removidos = total_antes - len(getattr(self, "conceitos", []) or [])

            if removidos > 0:
                self.salvar_conceitos()
                self.atualizar_lista()
                self.limpar_campos()
                MessageBox.feynman_delete_success(self)

            else:
                MessageBox.feynman_delete_error(self)

    except Exception as e:
        logger.error(f"Erro ao deletar conceito: {str(e)}", exc_info=True)
        MessageBox.feynman_delete_error(self)
