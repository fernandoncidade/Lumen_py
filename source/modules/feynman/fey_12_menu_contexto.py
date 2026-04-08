import os
from PySide6.QtWidgets import QMenu, QFileDialog
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QAction
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _obter_conceito_do_item_menu(self, item):
    try:
        if item is None:
            return None

        try:
            data = item.data(Qt.UserRole)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        titulo = item.text().split(' - ')[0].replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '')
        return next((c for c in self.conceitos if c.get('titulo') == titulo), None)

    except Exception:
        return None

def _obter_referencia_conceito(self, item):
    try:
        conceito_item = _obter_conceito_do_item_menu(self, item)

        if not isinstance(conceito_item, dict):
            return None

        titulo = (conceito_item.get('titulo') or '').strip()

        if not titulo:
            return None

        conceito_lista = next((c for c in self.conceitos if (c.get('titulo') or '').strip() == titulo), None)

        if isinstance(conceito_lista, dict):
            return conceito_lista

        return conceito_item

    except Exception:
        return None

def _texto_acao_com_caminho(label, caminho):
    try:
        caminho_limpo = (caminho or '').strip()

        if not caminho_limpo:
            return label

        return f"{label}\t{os.path.abspath(caminho_limpo)}"

    except Exception:
        return label

def mostrar_menu_contexto(self, position):
    try:
        item = self.lista_conceitos.itemAt(position)

        if not item:
            return

        conceito = _obter_conceito_do_item_menu(self, item)
        caminho_vinculado = ''

        if isinstance(conceito, dict):
            caminho_vinculado = (conceito.get('arquivo_vinculado') or '').strip()

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

        menu.addSeparator()

        acao_vincular = QAction(_texto_acao_com_caminho(QCoreApplication.translate("App", "📎 Vincular Arquivo"), caminho_vinculado), self)
        acao_vincular.triggered.connect(lambda: self.vincular_arquivo_conceito(item))
        menu.addAction(acao_vincular)

        acao_remover_vinculo = QAction(_texto_acao_com_caminho(QCoreApplication.translate("App", "🗑️ Remover Arquivo Vinculado"), caminho_vinculado), self)
        acao_remover_vinculo.setEnabled(bool(caminho_vinculado))
        acao_remover_vinculo.triggered.connect(lambda: self.remover_arquivo_vinculado(item))
        menu.addAction(acao_remover_vinculo)

        acao_abrir_arquivo = QAction(_texto_acao_com_caminho(QCoreApplication.translate("App", "📂 Abrir Arquivo Vinculado"), caminho_vinculado), self)
        acao_abrir_arquivo.setEnabled(bool(caminho_vinculado))
        acao_abrir_arquivo.triggered.connect(lambda: self.abrir_arquivo_conceito(item))
        menu.addAction(acao_abrir_arquivo)

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

def vincular_arquivo_conceito(self, item):
    try:
        conceito = _obter_referencia_conceito(self, item)

        if not conceito:
            return

        caminho_atual = (conceito.get('arquivo_vinculado') or '').strip()
        diretorio_base = ''

        if caminho_atual:
            try:
                diretorio_base = os.path.dirname(os.path.abspath(caminho_atual))

            except Exception:
                diretorio_base = ''

        caminho, _ = QFileDialog.getOpenFileName(
            self,
            QCoreApplication.translate("App", "Selecionar arquivo para vincular"),
            diretorio_base,
            QCoreApplication.translate("App", "Todos os arquivos (*)")
        )

        if not caminho:
            return

        caminho_abs = os.path.abspath(caminho)
        conceito['arquivo_vinculado'] = caminho_abs

        try:
            item.setData(Qt.UserRole, conceito)

        except Exception:
            pass

        if isinstance(getattr(self, 'conceito_atual', None), dict) and self.conceito_atual.get('titulo') == conceito.get('titulo'):
            self.conceito_atual['arquivo_vinculado'] = caminho_abs

        self.salvar_conceitos()
        self.atualizar_lista()

    except Exception as e:
        logger.error(f"Erro ao vincular arquivo ao conceito: {str(e)}", exc_info=True)

def remover_arquivo_vinculado(self, item):
    try:
        conceito = _obter_referencia_conceito(self, item)

        if not conceito:
            return

        caminho_atual = (conceito.get('arquivo_vinculado') or '').strip()

        if not caminho_atual:
            return

        conceito['arquivo_vinculado'] = None

        try:
            item.setData(Qt.UserRole, conceito)

        except Exception:
            pass

        if isinstance(getattr(self, 'conceito_atual', None), dict) and self.conceito_atual.get('titulo') == conceito.get('titulo'):
            self.conceito_atual['arquivo_vinculado'] = None

        self.salvar_conceitos()
        self.atualizar_lista()

        MessageBox.feynman_unlinked_file_removed(self)

    except Exception as e:
        logger.error(f"Erro ao remover arquivo vinculado: {str(e)}", exc_info=True)
