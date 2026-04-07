from datetime import datetime
from uuid import uuid4
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

@staticmethod
def from_dict(data):
    try:
        from source.modules.tempo.tmp_01_Tarefa import Tarefa
        prioridade = Tarefa.normalizar_prioridade(data.get('prioridade', 'Importante e Urgente'))
        tarefa = Tarefa(
            data['titulo'],
            data.get('descricao', ''),
            data.get('etapas', []),
            prioridade,
            data.get('status', 'Todo'),
            id=data.get('id', str(uuid4()))
        )
        tarefa.data_criacao = data.get('data_criacao', datetime.now().isoformat())
        tarefa.pomodoros_completados = data.get('pomodoros', 0)
        return tarefa

    except Exception as e:
        logger.error(f"Erro ao criar tarefa a partir de dicionário: {str(e)}", exc_info=True)
        return None
