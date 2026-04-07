from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def atualizar_coluna_doing_timer(self):
    try:
        self.col_doing_timer_list.clear()

        if not hasattr(self, 'tarefas') or not self.tarefas:
            return

        for t in getattr(self.tarefas, 'tarefas', []):
            if getattr(t, 'status', '') == "Doing":
                prioridade_norm = Tarefa.normalizar_prioridade(getattr(t, 'prioridade', 'Importante e Urgente'))
                emoji = {
                    "Importante e Urgente": "🔴",
                    "Importante, mas Não Urgente": "🟠",
                    "Não Importante, mas Urgente": "🟡",
                    "Não Importante e Não Urgente": "🟢",
                }.get(prioridade_norm, "🔴")
                texto = f"{emoji} {t.titulo} — 🍅 {t.pomodoros_completados}"
                self.col_doing_timer_list.addItem(texto)

    except Exception as e:
        logger.error(f"Erro ao atualizar coluna de tarefas em progresso no timer: {str(e)}", exc_info=True)
