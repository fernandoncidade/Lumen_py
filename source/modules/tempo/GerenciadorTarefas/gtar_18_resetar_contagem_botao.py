from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def resetar_contagem_botao(self):
    try:
        escopos = [
            QCoreApplication.translate("App", "🔹 Uma tarefa específica"),
            QCoreApplication.translate("App", "📂 Todas as tarefas de uma coluna"),
            QCoreApplication.translate("App", "🌐 Todas as tarefas (global)")
        ]

        escopo, ok = QInputDialog.getItem(
            self,
            QCoreApplication.translate("App", "🔄 Resetar Contagem"),
            QCoreApplication.translate("App", "O que deseja restaurar?"),
            escopos,
            0,
            False
        )

        if not ok or not escopo:
            return

        opcoes_colunas = [
            QCoreApplication.translate("App", "📋 A Fazer"),
            QCoreApplication.translate("App", "⚙️ Em Progresso"),
            QCoreApplication.translate("App", "✅ Concluído")
        ]

        mapa_status = {
            QCoreApplication.translate("App", "📋 A Fazer"): "Todo",
            QCoreApplication.translate("App", "⚙️ Em Progresso"): "Doing",
            QCoreApplication.translate("App", "✅ Concluído"): "Done"
        }

        if escopo == escopos[0]:
            coluna_exibida, ok = QInputDialog.getItem(
                self,
                QCoreApplication.translate("App", "🔄 Resetar Contagem"),
                QCoreApplication.translate("App", "Selecione a coluna:"),
                opcoes_colunas,
                0,
                False
            )

            if not ok or not coluna_exibida:
                return

            status_coluna = mapa_status.get(coluna_exibida, "Todo")
            tarefas_coluna = [t for t in self.tarefas if getattr(t, 'status', '') == status_coluna]

            if not tarefas_coluna:
                MessageBox.tempo_no_tasks_in_column(self)
                return

            titulos = [t.titulo for t in tarefas_coluna]
            titulo_escolhido, ok = QInputDialog.getItem(
                self,
                QCoreApplication.translate("App", "🔄 Resetar Contagem"),
                QCoreApplication.translate("App", "Selecione a tarefa:"),
                titulos,
                0,
                False
            )

            if not ok or not titulo_escolhido:
                return

            for t in tarefas_coluna:
                if t.titulo == titulo_escolhido:
                    t.pomodoros_completados = 0
                    break

        elif escopo == escopos[1]:
            coluna_exibida, ok = QInputDialog.getItem(
                self,
                QCoreApplication.translate("App", "🔄 Resetar Contagem"),
                QCoreApplication.translate("App", "Selecione a coluna:"),
                opcoes_colunas,
                0,
                False
            )

            if not ok or not coluna_exibida:
                return

            status_coluna = mapa_status.get(coluna_exibida, "Todo")
            tarefas_coluna = [t for t in self.tarefas if getattr(t, 'status', '') == status_coluna]

            if not tarefas_coluna:
                MessageBox.tempo_no_tasks_in_column(self)
                return

            for t in tarefas_coluna:
                t.pomodoros_completados = 0

        else:
            if not self.tarefas:
                MessageBox.tempo_no_tasks_anywhere(self)
                return

            for t in self.tarefas:
                t.pomodoros_completados = 0

        self.salvar_tarefas()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao resetar contagem: {str(e)}", exc_info=True)
