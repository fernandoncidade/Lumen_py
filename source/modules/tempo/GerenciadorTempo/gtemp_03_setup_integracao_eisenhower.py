from source.utils.LogManager import LogManager
from source.utils.EventBus import get_event_bus
logger = LogManager.get_logger()

def _setup_integracao_eisenhower(self):
    try:
        self._event_bus = get_event_bus()
        try:
            self._event_bus.tarefa_integracao.connect(self._on_event_bus_tarefa)

        except Exception as e:
            logger.debug(f"Falha ao conectar tarefa_integracao: {e}", exc_info=True)

        try:
            self._event_bus.drain_pending_tarefas()

        except Exception:
            pass

    except Exception as e:
        logger.debug(f"Falha ao configurar integração com Eisenhower: {e}", exc_info=True)
