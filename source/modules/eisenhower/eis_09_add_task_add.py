from PySide6.QtCore import Qt
from source.utils.EventBus import get_event_bus
from source.modules.tempo.tmp_01_Tarefa import Tarefa
from uuid import uuid4
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def add_task_add(self):
    task_text = ""
    selected_quadrant = 0
    date_iso = None
    time_str = None

    try:
        task_text = (self.task_input.text() or "").strip()
        selected_quadrant = int(self.quadrant_selector.currentIndex())

        if hasattr(self, "date_checkbox") and self.date_checkbox.isChecked():
            try:
                date_iso = self.date_input.date().toString(Qt.ISODate)

            except Exception as e:
                logger.error(f"Falha ao obter data ISO: {e}", exc_info=True)
                date_iso = None

            if hasattr(self, "time_checkbox") and hasattr(self, "time_input") and self.time_checkbox.isChecked():
                try:
                    time_str = self.time_input.time().toString("HH:mm")

                except Exception as e:
                    logger.error(f"Falha ao obter horário: {e}", exc_info=True)
                    time_str = None

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {e}", exc_info=True)

    try:
        created_data = None

        try:
            from source.modules.eisenhower import add_task as _add_task

        except Exception:
            _add_task = globals().get('add_task')

        if _add_task:
            created_data = _add_task(self)

    except Exception as e:
        logger.error(f"Erro ao chamar add_task: {e}", exc_info=True)

    try:
        if hasattr(self, "calendar_pane") and self.calendar_pane:
            self.calendar_pane.calendar_panel.update_task_list()

        try:
            if hasattr(self, "integrate_time_button") and self.integrate_time_button and self.integrate_time_button.isChecked():
                if task_text:
                    prioridades = [
                        "Importante e Urgente",
                        "Importante, mas Não Urgente",
                        "Não Importante, mas Urgente",
                        "Não Importante e Não Urgente",
                    ]
                    prioridade = prioridades[selected_quadrant] if 0 <= selected_quadrant < len(prioridades) else "Importante e Urgente"
                    payload = {
                        "integration_id": str(uuid4()),
                        "origin": "eisenhower",
                        "id": (created_data or {}).get("id"),
                        "titulo": task_text,
                        "prioridade": Tarefa.normalizar_prioridade(prioridade),
                        "date": (created_data or {}).get("date", date_iso),
                        "time": (created_data or {}).get("time", time_str),
                        "description": (created_data or {}).get("description") or None,
                        "file_path": (created_data or {}).get("file_path") or None,
                    }
                    get_event_bus().send_tarefa(payload)

        except Exception as e:
            logger.debug(f"Falha ao enviar tarefa do Eisenhower para Gestão de Tempo: {e}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao atualizar lista de tarefas no calendário: {e}", exc_info=True)
