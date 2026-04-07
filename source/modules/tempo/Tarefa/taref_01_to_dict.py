from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def to_dict(self):
    try:
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'etapas': self.etapas,
            'prioridade': self.prioridade,
            'status': self.status,
            'data_criacao': self.data_criacao,
            'pomodoros': self.pomodoros_completados
        }

    except Exception as e:
        logger.error(f"Erro ao converter tarefa para dicionário: {str(e)}", exc_info=True)
        return {}
