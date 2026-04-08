import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text: str) -> str:
    return QCoreApplication.translate("App", text)

def adicionar_tarefa(self):
    try:
        titulo = self.input_tarefa.text().strip()

        try:
            logger.info(f"GerenciadorTarefas.adicionar_tarefa chamado; texto='{titulo}'")

        except Exception:
            pass

        if not titulo:
            return

        idx = self.combo_prioridade.currentIndex()
        prioridades = [
            "Importante e Urgente",
            "Importante, mas Não Urgente",
            "Não Importante, mas Urgente",
            "Não Importante e Não Urgente",
        ]
        prioridade = prioridades[idx] if 0 <= idx < len(prioridades) else "Importante e Urgente"

        file_path = None
        dragged_path = getattr(self, "_dragged_file_path", None)

        if dragged_path:
            try:
                nome = os.path.basename(dragged_path)
                resp = QMessageBox.question(
                    self,
                    get_text("Vincular arquivo"),
                    get_text("Deseja vincular o arquivo a esta tarefa?\n\n{nome}").format(nome=nome),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes,
                )
                if resp == QMessageBox.Yes:
                    file_path = dragged_path

            except Exception as e:
                logger.error(f"Erro ao confirmar vínculo de arquivo: {str(e)}", exc_info=True)

        tarefa = self._adicionar_tarefa_interna(titulo=titulo, prioridade=prioridade, status="Todo", emitir_sinal=True, file_path=file_path)

        if tarefa is not None:
            self.input_tarefa.clear()

            try:
                if hasattr(self, "_dragged_file_path"):
                    self._dragged_file_path = None

                if hasattr(self, "input_tarefa") and self.input_tarefa is not None:
                    self.input_tarefa.setToolTip("")

            except Exception:
                pass

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {str(e)}", exc_info=True)
