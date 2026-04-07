from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_event_bus_tarefa(self, dados: dict):
    try:
        payload = dados or {}
        if payload.get("origin") != "eisenhower":
            return

        integration_id = payload.get("integration_id")
        if integration_id and integration_id in self._integracao_ids_recebidos:
            return

        if integration_id:
            self._integracao_ids_recebidos.add(integration_id)

        titulo = (payload.get("titulo") or "").strip()
        prioridade = payload.get("prioridade") or "Importante e Urgente"

        if not titulo:
            return

        if hasattr(self, 'tarefas') and self.tarefas:
            self.tarefas.adicionar_tarefa_externa(titulo=titulo, prioridade=prioridade)

    except Exception as e:
        logger.debug(f"Falha ao receber tarefa do Eisenhower: {e}", exc_info=True)
