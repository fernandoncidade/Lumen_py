import json
import os
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def carregar_tarefas(self):
    tarefas = []
    try:
        if os.path.exists(self.arquivo_tarefas):
            with open(self.arquivo_tarefas, "r", encoding="utf-8") as f:
                data = json.load(f)

            bruto = data.get("tarefas") if isinstance(data, dict) else data
            if isinstance(bruto, list):
                for item in bruto:
                    t = Tarefa.from_dict(item)
                    if t:
                        tarefas.append(t)

        return tarefas

    except Exception as e:
        logger.error(f"Erro ao carregar tarefas: {str(e)}", exc_info=True)
        return []
