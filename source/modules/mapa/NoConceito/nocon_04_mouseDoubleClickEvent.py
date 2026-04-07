from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDialog, QTextEdit, QDialogButtonBox, QPushButton, QMessageBox
from PySide6.QtCore import QCoreApplication, QTimer
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mouseDoubleClickEvent(self, event):
    try:
        dialogo = QDialog()
        dialogo.setWindowTitle(QCoreApplication.translate("App", "Editar Conceito"))
        dialogo.setMinimumSize(560, 460)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Texto do Conceito:")))
        input_texto = QTextEdit()
        input_texto.setPlainText(self.texto)
        input_texto.setMaximumHeight(60)
        layout.addWidget(input_texto)

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Informações associadas:")))
        info_view = QTextEdit()
        info_view.setReadOnly(True)

        if self.info_associada:
            info_view.setPlainText("\n\n".join(self.info_associada))

        else:
            info_view.setPlainText(QCoreApplication.translate("App", "Sem informações associadas."))

        layout.addWidget(info_view)

        layout.addWidget(QLabel(QCoreApplication.translate("App", "Notas (Método Feynman - explique com suas palavras):")))
        input_notas = QTextEdit()
        input_notas.setPlainText(self.notas)
        layout.addWidget(input_notas)

        layout_botoes = QHBoxLayout()

        btn_integrar_feynman = QPushButton(QCoreApplication.translate("App", "➕ Integrar ao Método Feynman"))
        btn_integrar_feynman.setToolTip(QCoreApplication.translate("App", "Envia as notas para o Método Feynman"))
        layout_botoes.addWidget(btn_integrar_feynman)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
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

                dados = {'titulo': titulo, 'notas': notas_texto}
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
            self.texto_item.setPlainText(self.texto)
            rect = self.texto_item.boundingRect()
            self.texto_item.setPos(-rect.width()/2, -rect.height()/2)
            self._badge.setVisible(bool(self.notas))
            logger.debug(f"Conceito '{self.texto}' atualizado localmente (OK) - SEM integração ao Feynman")

    except Exception as e:
        logger.error(f"Erro ao editar conceito: {str(e)}", exc_info=True)