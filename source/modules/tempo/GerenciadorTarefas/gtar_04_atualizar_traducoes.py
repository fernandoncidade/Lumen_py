from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_traducoes(self):
    try:
        self.input_tarefa.setPlaceholderText(QCoreApplication.translate("App", "Digite uma nova tarefa ou arraste um arquivo... (Ex: 'Estudar Resistência dos Materiais - Cap 3')"))
        self.combo_prioridade.clear()
        self.combo_prioridade.addItems([
            QCoreApplication.translate("App", "🔴 Importante e Urgente"),
            QCoreApplication.translate("App", "🟠 Importante, mas Não Urgente"),
            QCoreApplication.translate("App", "🟡 Não Importante, mas Urgente"),
            QCoreApplication.translate("App", "🟢 Não Importante e Não Urgente")
        ])
        self.combo_prioridade.setCurrentText(QCoreApplication.translate("App", "🔴 Importante e Urgente"))
        self._ajustar_largura_combo(self.combo_prioridade)

        if hasattr(self, "gerenciador_botoes") and self.gerenciador_botoes is not None:
            self.gerenciador_botoes.set_button_text(self.btn_adicionar, QCoreApplication.translate("App", "➕ Adicionar"))
            self.gerenciador_botoes.set_button_text(self.btn_remover, QCoreApplication.translate("App", "🗑️ Remover Tarefa(s)"))
            self.gerenciador_botoes.set_button_text(self.btn_mover, QCoreApplication.translate("App", "🔀 Mover Tarefa(s)"))

        else:
            self.btn_adicionar.setText(QCoreApplication.translate("App", "➕ Adicionar"))
            self.btn_remover.setText(QCoreApplication.translate("App", "🗑️ Remover Tarefa(s)"))
            self.btn_mover.setText(QCoreApplication.translate("App", "🔀 Mover Tarefa(s)"))

        if hasattr(self, 'btn_resetar_contagem'):
            if hasattr(self, "gerenciador_botoes") and self.gerenciador_botoes is not None:
                self.gerenciador_botoes.set_button_text(self.btn_resetar_contagem, QCoreApplication.translate("App", "🔄 Resetar Contagem"))

            else:
                self.btn_resetar_contagem.setText(QCoreApplication.translate("App", "🔄 Resetar Contagem"))

        self.col_todo.setTitle(QCoreApplication.translate("App", "📋 A Fazer"))
        self.col_doing.setTitle(QCoreApplication.translate("App", "⚙️ Em Progresso"))
        self.col_done.setTitle(QCoreApplication.translate("App", "✅ Concluído"))

        try:
            if hasattr(self, "status_tabs") and self.status_tabs is not None:
                self.status_tabs.setTabText(0, QCoreApplication.translate("App", "📋 A Fazer"))
                self.status_tabs.setTabText(1, QCoreApplication.translate("App", "⚙️ Em Progresso"))
                self.status_tabs.setTabText(2, QCoreApplication.translate("App", "✅ Concluído"))

        except Exception:
            pass

        try:
            if hasattr(self, 'atualizar_listas') and callable(self.atualizar_listas):
                self.atualizar_listas()

        except Exception as e:
            logger.error(f"Erro ao atualizar listas: {str(e)}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao atualizar traduções do GerenciadorTarefas: {str(e)}", exc_info=True)
