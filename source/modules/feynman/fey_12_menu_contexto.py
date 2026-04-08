from PySide6.QtWidgets import QMenu
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QAction
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, position):
    try:
        item = self.lista_conceitos.itemAt(position)
        if not item:
            return

        menu = QMenu(self)

        menu_dominio = menu.addMenu(QCoreApplication.translate("App", "🎯 Redefinir Nível de Domínio"))

        acao_iniciante = QAction(QCoreApplication.translate("App", "🔴 Iniciante"), self)
        acao_iniciante.triggered.connect(lambda: self.redefinir_dominio(item, 0))
        menu_dominio.addAction(acao_iniciante)

        acao_intermediario = QAction(QCoreApplication.translate("App", "🟡 Intermediário"), self)
        acao_intermediario.triggered.connect(lambda: self.redefinir_dominio(item, 1))
        menu_dominio.addAction(acao_intermediario)

        acao_avancado = QAction(QCoreApplication.translate("App", "🟢 Avançado"), self)
        acao_avancado.triggered.connect(lambda: self.redefinir_dominio(item, 2))
        menu_dominio.addAction(acao_avancado)

        menu.exec(self.lista_conceitos.mapToGlobal(position))

    except Exception as e:
        logger.error(f"Erro ao mostrar menu de contexto: {str(e)}", exc_info=True)

def redefinir_dominio(self, item, novo_nivel):
    try:
        conceito = None
        titulo = None

        try:
            data = item.data(Qt.UserRole)

            if isinstance(data, dict):
                titulo = data.get('titulo')

                for i, c in enumerate(self.conceitos):
                    if c.get('titulo') == titulo:
                        self.conceitos[i]['dominio'] = novo_nivel
                        conceito = self.conceitos[i]
                        break

                if conceito is None:
                    data['dominio'] = novo_nivel
                    conceito = data

        except Exception:
            conceito = None

        if conceito is None:
            titulo = item.text().split(' - ')[0].replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '')
            conceito = next((c for c in self.conceitos if c.get('titulo') == titulo), None)

        if conceito:
            try:
                conceito['dominio'] = novo_nivel

            except Exception:
                pass

            self.salvar_conceitos()
            self.atualizar_lista()

            if self.conceito_atual and self.conceito_atual.get('titulo') == (titulo or conceito.get('titulo')):
                self.conceito_atual = conceito
                try:
                    self.combo_dominio.setCurrentIndex(novo_nivel)

                except Exception:
                    pass

            nivel_texto = [
                QCoreApplication.translate("App", "Iniciante"),
                QCoreApplication.translate("App", "Intermediário"),
                QCoreApplication.translate("App", "Avançado")
            ][novo_nivel]

            logger.info(f"Nível de domínio do conceito '{titulo or conceito.get('titulo')}' alterado para: {nivel_texto}")

    except Exception as e:
        logger.error(f"Erro ao redefinir domínio do conceito: {str(e)}", exc_info=True)
