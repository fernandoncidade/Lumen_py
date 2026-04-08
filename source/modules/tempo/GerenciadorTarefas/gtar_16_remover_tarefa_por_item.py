from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def remover_tarefa_por_item(self, item):
    try:
        if not item:
            return

        tarefa_id = item.data(Qt.UserRole)
        linha0 = (item.text().split('\n')[0] or '').strip()
        emoji_prefix = linha0[:2] if linha0 else ''
        titulo_item = (
            linha0
            .replace('🔴 ', '')
            .replace('🟠 ', '')
            .replace('🟡 ', '')
            .replace('🟢 ', '')
        )
        prioridade_map = {
            "🔴": "Importante e Urgente",
            "🟠": "Importante, mas Não Urgente",
            "🟡": "Não Importante, mas Urgente",
            "🟢": "Não Importante e Não Urgente",
        }
        prioridade_item = prioridade_map.get(emoji_prefix, None)

        try:
            resp = QMessageBox.question(
                self,
                QCoreApplication.translate("App", "Confirmar Exclusão"),
                QCoreApplication.translate("App", "Deseja remover a tarefa selecionada?\n\n{titulo}").format(titulo=titulo_item),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if resp != QMessageBox.Yes:
                return

        except Exception:
            pass

        total_antes = len(getattr(self, 'tarefas', []))
        if tarefa_id:
            self.tarefas = [t for t in self.tarefas if getattr(t, 'id', None) != tarefa_id]

        else:
            prioridade_norm = Tarefa.normalizar_prioridade(prioridade_item) if prioridade_item else None
            novas = []
            for t in self.tarefas:
                if t.titulo != titulo_item:
                    novas.append(t)
                    continue

                if prioridade_norm is None:
                    novas.append(t)
                    continue

                if Tarefa.normalizar_prioridade(getattr(t, 'prioridade', '')) != prioridade_norm:
                    novas.append(t)

            self.tarefas = novas

        self.salvar_tarefas()
        self.atualizar_listas()

        try:
            total_depois = len(getattr(self, 'tarefas', []))
            if total_depois < total_antes:
                QMessageBox.information(
                    self,
                    QCoreApplication.translate("App", "Sucesso"),
                    QCoreApplication.translate("App", "Tarefa removida com sucesso!")
                )

            else:
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("App", "Falha"),
                    QCoreApplication.translate("App", "Não foi possível remover a tarefa selecionada.")
                )

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao remover tarefa pelo menu de contexto: {str(e)}", exc_info=True)
        try:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("App", "Falha"),
                QCoreApplication.translate("App", "Ocorreu um erro ao remover a tarefa.")
            )

        except Exception:
            pass
