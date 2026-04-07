from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _on_event_bus_tarefa(self, dados: dict):
    try:
        payload = dados or {}
        if payload.get("origin") != "tempo":
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

        date_iso = payload.get("date") or payload.get("date_iso") or None
        time_str = payload.get("time") or None
        description = payload.get("description") or payload.get("desc") or None
        file_path = payload.get("file_path") or None

        try:
            self._adicionar_tarefa_integrada_do_tempo(titulo=titulo, prioridade=prioridade, date=date_iso, time=time_str, description=description, file_path=file_path)

        except Exception:
            try:
                self._adicionar_tarefa_integrada_do_tempo(titulo=titulo, prioridade=prioridade)

            except Exception:
                pass

    except Exception as e:
        logger.debug(f"Falha ao receber tarefa do Tempo no Eisenhower: {e}", exc_info=True)
