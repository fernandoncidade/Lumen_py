from datetime import datetime
from uuid import uuid4
from source.utils.LogManager import LogManager
from source.modules.tempo.Tarefa import to_dict, from_dict, normalizar_prioridade


class Tarefa:
    def __init__(self, titulo, descricao="", etapas=None, prioridade="Importante e Urgente", status="Todo", id=None, file_path=None, date=None, time=None):
        self.titulo = titulo
        self.descricao = descricao
        self.etapas = etapas or []
        self.prioridade = self.normalizar_prioridade(prioridade)
        self.status = status
        self.data_criacao = datetime.now().isoformat()
        self.pomodoros_completados = 0
        self.id = id or str(uuid4())
        self.file_path = file_path or None
        self.date = date or None
        self.time = time or None
        self.logger = LogManager.get_logger()

    def to_dict(self):
        return to_dict(self)

    @staticmethod
    def from_dict(data):
        return from_dict(data)

    @staticmethod
    def normalizar_prioridade(valor):
        return normalizar_prioridade(valor)
