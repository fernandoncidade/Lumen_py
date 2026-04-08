from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def selecionar_conceito(self, item):
    try:
        try:
            conceito = item.data(getattr(__import__('PySide6.QtCore', fromlist=['Qt']).Qt, 'UserRole'))

        except Exception:
            conceito = None

        if conceito is None:
            titulo = item.text().split(' - ')[0].replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '')
            conceito = next((c for c in self.conceitos if c.get('titulo') == titulo), None)

        if conceito:
            self.conceito_atual = conceito
            self.input_titulo.setPlainText(conceito.get('titulo', ''))
            self.texto_explicacao.setPlainText(conceito.get('explicacao', ''))
            self.texto_lacunas.setPlainText(conceito.get('lacunas', ''))
            self.texto_revisao.setPlainText(conceito.get('revisao', ''))

            try:
                self.combo_dominio.setCurrentIndex(int(conceito.get('dominio', 0) or 0))

            except Exception:
                pass

    except Exception as e:
        logger.error(f"Erro ao selecionar conceito: {str(e)}", exc_info=True)
