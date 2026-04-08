from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
from source.utils.EventBus import get_event_bus
from uuid import uuid4
logger = LogManager.get_logger()

def _on_tarefa_adicionada_gestao_tempo(self, dados: dict):
    try:
        if not hasattr(self, 'btn_eisenhower_integrado') or not self.btn_eisenhower_integrado.isChecked():
            return

        titulo = (dados or {}).get("titulo")
        prioridade = (dados or {}).get("prioridade")

        if not titulo:
            return

        payload = {
            "integration_id": str(uuid4()),
            "origin": "tempo",
            "id": (dados or {}).get("id"),
            "titulo": titulo,
            "prioridade": Tarefa.normalizar_prioridade(prioridade),
            "description": (dados or {}).get("description") or (dados or {}).get("desc") or None,
            "file_path": (dados or {}).get("file_path") or None,
            "date": (dados or {}).get("date") or (dados or {}).get("date_iso") or None,
            "time": (dados or {}).get("time") or None,
        }
        get_event_bus().send_tarefa(payload)

    except Exception as e:
        logger.debug(f"Falha ao enviar tarefa para Eisenhower: {e}", exc_info=True)
