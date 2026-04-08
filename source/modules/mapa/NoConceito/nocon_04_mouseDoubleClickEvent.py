from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDialog, QTextEdit, QDialogButtonBox, QPushButton, QMessageBox, QFileDialog
from PySide6.QtCore import QCoreApplication, QTimer, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from source.utils.LogManager import LogManager
from source.utils.GerenciadorBotoesUI import GerenciadorBotoesUI
logger = LogManager.get_logger()

def mouseDoubleClickEvent(self, event):
    try:
        try:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
                caminho = getattr(self, "arquivo_vinculado", None)
                if caminho:
                    event.accept()
                    QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))
                    return

        except Exception:
            pass

        parent = None

        try:
            scene = self.scene()
            if scene and scene.views():
                parent = scene.views()[0]

        except Exception:
            parent = None

        dialogo = QDialog(parent)
        dialogo.setWindowTitle(QCoreApplication.translate("App", "Editar Conceito"))
        dialogo.setMinimumSize(560, 460)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Texto do Conceito:"), dialogo))
        input_texto = QTextEdit(dialogo)
        input_texto.setPlainText(self.texto)
        input_texto.setMaximumHeight(60)
        layout.addWidget(input_texto)

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Informações associadas:"), dialogo))
        info_view = QTextEdit(dialogo)
        info_view.setReadOnly(False)

        try:
            info_view.setPlaceholderText(QCoreApplication.translate("App", "Edite as informações associadas. Separe itens por uma linha em branco."))

        except Exception:
            pass

        if self.info_associada:
            info_view.setPlainText("\n\n".join(self.info_associada))

        else:
            info_view.setPlainText(QCoreApplication.translate("App", "Sem informações associadas."))

        layout.addWidget(info_view)

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Notas (Método Feynman - explique com suas palavras):"), dialogo))
        input_notas = QTextEdit(dialogo)
        input_notas.setPlainText(self.notas)
        layout.addWidget(input_notas)

        layout_botoes = QHBoxLayout()
        col_esquerda = QVBoxLayout()

        ger_botoes = GerenciadorBotoesUI(dialogo)
        btn_integrar_feynman = ger_botoes.create_button_with_auto_resize(QCoreApplication.translate("App", "➕ Integrar ao Método Feynman"))
        btn_integrar_feynman.setToolTip(QCoreApplication.translate("App", "Envia as notas para o Método Feynman"))
        col_esquerda.addWidget(btn_integrar_feynman)

        caminho_vinculado = getattr(self, "arquivo_vinculado", None)
        linha_arquivo = QHBoxLayout()
        btn_arquivo = QPushButton(dialogo)
        btn_arquivo._lumen_click_handler = None
        lbl_caminho = QLabel(caminho_vinculado or "", dialogo)
        lbl_caminho.setTextInteractionFlags(Qt.TextSelectableByMouse)
        linha_arquivo.addWidget(btn_arquivo)
        linha_arquivo.addWidget(lbl_caminho)
        col_esquerda.addLayout(linha_arquivo)

        linha_remover = QHBoxLayout()
        btn_remover = QPushButton(QCoreApplication.translate("App", "🗑️ Remover Arquivo:"), dialogo)
        lbl_remover_caminho = QLabel(caminho_vinculado or "", dialogo)
        lbl_remover_caminho.setTextInteractionFlags(Qt.TextSelectableByMouse)
        linha_remover.addWidget(btn_remover)
        linha_remover.addWidget(lbl_remover_caminho)
        col_esquerda.addLayout(linha_remover)

        def _abrir_arquivo(caminho: str | None):
            if not caminho:
                return

            QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))

        def _atualizar_ui_arquivo(caminho: str | None):
            if btn_arquivo._lumen_click_handler is not None:
                try:
                    btn_arquivo.clicked.disconnect(btn_arquivo._lumen_click_handler)

                except Exception:
                    pass

                btn_arquivo._lumen_click_handler = None

            if caminho:
                btn_arquivo.setText(QCoreApplication.translate("App", "📂 Abrir Arquivo:"))
                lbl_caminho.setText(caminho)
                lbl_remover_caminho.setText(caminho)
                btn_remover.setVisible(True)
                lbl_remover_caminho.setVisible(True)

                def _handler_open(_checked=False, c=caminho):
                    _abrir_arquivo(c)

                btn_arquivo._lumen_click_handler = _handler_open
                btn_arquivo.clicked.connect(btn_arquivo._lumen_click_handler)

            else:
                btn_arquivo.setText(QCoreApplication.translate("App", "🔗 Vincular Arquivo"))
                lbl_caminho.setText("")
                lbl_remover_caminho.setText("")
                btn_remover.setVisible(False)
                lbl_remover_caminho.setVisible(False)
                btn_arquivo._lumen_click_handler = _vincular_arquivo
                btn_arquivo.clicked.connect(btn_arquivo._lumen_click_handler)

        def _remover_arquivo():
            try:
                self.arquivo_vinculado = None

                try:
                    self.setToolTip(QCoreApplication.translate("App", ""))

                except Exception:
                    pass

                _atualizar_ui_arquivo(None)

            except Exception as e:
                logger.error(f"Erro ao remover arquivo vinculado: {e}", exc_info=True)

        btn_remover.clicked.connect(_remover_arquivo)

        def _vincular_arquivo():
            try:
                caminho, _ = QFileDialog.getOpenFileName(
                    dialogo,
                    QCoreApplication.translate("App", "Vincular arquivo"),
                    "",
                    QCoreApplication.translate("App", "Todos os arquivos (*.*)")
                )
                if not caminho:
                    return

                self.arquivo_vinculado = caminho

                try:
                    self.setToolTip(QCoreApplication.translate("App", "Para abrir o arquivo vinculado, clique CTRL+duplo clique com o botão esquerdo do mouse sobre o nó."))

                except Exception:
                    pass

                _atualizar_ui_arquivo(caminho)

            except Exception as e:
                logger.error(f"Erro ao vincular arquivo: {e}", exc_info=True)

        _atualizar_ui_arquivo(caminho_vinculado)

        layout_botoes.addLayout(col_esquerda)
        layout_botoes.addStretch(1)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialogo)
        botoes.accepted.connect(dialogo.accept)
        botoes.rejected.connect(dialogo.reject)
        layout_botoes.addWidget(botoes)

        layout.addLayout(layout_botoes)

        dialogo.setLayout(layout)

        def integrar_ao_feynman():
            try:
                try:
                    if input_notas.hasFocus():
                        input_notas.clearFocus()

                    if input_texto.hasFocus():
                        input_texto.clearFocus()

                    QCoreApplication.processEvents()

                except Exception:
                    pass

                titulo = input_texto.toPlainText().strip()
                notas_texto = input_notas.toPlainText().strip()

                if not titulo:
                    QMessageBox.warning(
                        dialogo,
                        QCoreApplication.translate("App", "Atenção"),
                        QCoreApplication.translate("App", "Por favor, digite o título do conceito!")
                    )
                    return

                if not notas_texto:
                    QMessageBox.warning(
                        dialogo,
                        QCoreApplication.translate("App", "Atenção"),
                        QCoreApplication.translate("App", "Por favor, escreva suas notas antes de integrar ao Método Feynman!")
                    )
                    return

                dados = {
                    'titulo': titulo,
                    'notas': notas_texto,
                    'explicacao': notas_texto,
                    'lacunas': '',
                    'revisao': notas_texto,
                    'dominio': 0,
                }
                try:
                    self.event_bus.send_conceito(dados)

                except Exception:
                    self.event_bus.conceito_atualizado.emit(dados)

                logger.info(f"Conceito '{titulo}' integrado ao Método Feynman via botão específico")

                QCoreApplication.processEvents()
                QTimer.singleShot(50, lambda: QMessageBox.information(
                    dialogo,
                    QCoreApplication.translate("App", "✅ Integrado"),
                    QCoreApplication.translate("App", "Conceito '{titulo}' integrado ao Método Feynman com sucesso!").format(titulo=titulo)
                ))

            except Exception as e:
                logger.error(f"Erro ao integrar conceito ao Método Feynman: {str(e)}", exc_info=True)
                QMessageBox.critical(
                    dialogo,
                    QCoreApplication.translate("App", "Erro"),
                    QCoreApplication.translate("App", "Erro ao integrar ao Método Feynman: {erro}").format(erro=str(e))
                )

        btn_integrar_feynman.clicked.connect(integrar_ao_feynman)

        if dialogo.exec():
            self.texto = input_texto.toPlainText().strip()
            self.notas = input_notas.toPlainText().strip()

            try:
                raw_info = info_view.toPlainText()
                entries = [s.strip() for s in raw_info.split('\n\n') if s.strip()]
                self.info_associada = entries

            except Exception:
                pass

            self.texto_item.setPlainText(self.texto)
            rect = self.texto_item.boundingRect()
            self.texto_item.setPos(-rect.width()/2, -rect.height()/2)
            self._badge.setVisible(bool(self.notas))
            logger.debug(f"Conceito '{self.texto}' atualizado localmente (OK) - SEM integração ao Feynman")

    except Exception as e:
        logger.error(f"Erro ao editar conceito: {str(e)}", exc_info=True)
