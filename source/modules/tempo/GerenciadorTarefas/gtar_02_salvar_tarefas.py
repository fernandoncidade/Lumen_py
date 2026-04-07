import json
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def salvar_tarefas(self):
    try:
        os.makedirs(os.path.dirname(self.arquivo_tarefas), exist_ok=True)
        with open(self.arquivo_tarefas, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tarefas], f, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erro ao salvar tarefas: {str(e)}", exc_info=True)
