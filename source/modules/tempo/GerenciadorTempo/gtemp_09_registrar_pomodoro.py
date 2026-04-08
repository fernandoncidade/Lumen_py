from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def registrar_pomodoro(self, tipo):
    try:
        if tipo != "foco":
            return

        if not hasattr(self, 'tarefas') or not self.tarefas:
            return

        ciclos_total = max(1, int(getattr(getattr(self, 'pomodoro', None), 'ciclos_permitidos', 4)))
        fluxo_ativo = bool(
            hasattr(self.tarefas, 'chk_fluxo_tarefas_concluidas')
            and self.tarefas.chk_fluxo_tarefas_concluidas is not None
            and self.tarefas.chk_fluxo_tarefas_concluidas.isChecked()
        )

        alterou = False
        for t in getattr(self.tarefas, 'tarefas', []):
            if getattr(t, 'status', '') == "Doing":
                t.pomodoros_completados = int(getattr(t, 'pomodoros_completados', 0)) + 1

                if fluxo_ativo and int(getattr(t, 'pomodoros_completados', 0)) >= ciclos_total:
                    t.status = "Done"

                alterou = True

        if alterou:
            self.tarefas.salvar_tarefas()
            self.tarefas.atualizar_listas()
            self.atualizar_coluna_doing_timer()

    except Exception as e:
        logger.error(f"Erro ao registrar pomodoro nas tarefas em progresso: {str(e)}", exc_info=True)
