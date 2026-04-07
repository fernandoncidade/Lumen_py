from PySide6.QtCore import QCoreApplication
from source.utils.EventBus import get_event_bus
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def _setup_integracao_gestao_tempo(self):
    try:
        try:
            if hasattr(self, "integrate_time_button") and self.integrate_time_button:
                self.integrate_time_button.setToolTip(
                    get_text("Quando ativado, tarefas adicionadas na Matriz também são enviadas para o quadro 📋 A Fazer (Gestão de Tempo).")
                )

        except Exception:
            pass

        self._event_bus = get_event_bus()
        try:
            self._event_bus.tarefa_integracao.connect(self._on_event_bus_tarefa)

        except Exception:
            pass

        try:
            self._event_bus.drain_pending_tarefas()

        except Exception:
            pass

    except Exception as e:
        logger.debug(f"Falha ao configurar integração Gestão de Tempo: {e}", exc_info=True)
