from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

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

        tarefa = self._adicionar_tarefa_interna(titulo=titulo, prioridade=prioridade, status="Todo", emitir_sinal=True)
        if tarefa is not None:
            self.input_tarefa.clear()

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {str(e)}", exc_info=True)
