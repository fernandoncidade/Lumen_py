from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_traducoes(self):
    try:
        self.label_tarefas.setText(QCoreApplication.translate("App", "📊 Quadro de Tarefas"))

        if hasattr(self, 'pomodoro') and self.pomodoro:
            self.pomodoro.atualizar_traducoes()

        if hasattr(self, 'tarefas') and self.tarefas:
            self.tarefas.atualizar_traducoes()

        if hasattr(self, 'col_doing_timer_group') and self.col_doing_timer_group:
            self.col_doing_timer_group.setTitle(QCoreApplication.translate("App", "⚙️ Em Progresso"))

    except Exception as e:
        logger.error(f"Erro ao atualizar traduções do GerenciadorTempo: {str(e)}", exc_info=True)
