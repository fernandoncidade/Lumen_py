from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _ajustar_largura_minima_coluna_esquerda(self):
    try:
        left_widget = getattr(self, "left_widget", None)

        if left_widget is None:
            return

        min_tarefas = 0
        if hasattr(self, "tarefas") and self.tarefas is not None:
            try:
                min_tarefas = max(self.tarefas.minimumWidth(), self.tarefas.minimumSizeHint().width())

            except Exception:
                min_tarefas = 0

        left_widget.setMinimumWidth(max(540, min_tarefas))
        left_widget.updateGeometry()

    except Exception as e:
        logger.error(f"Erro ao ajustar largura mínima da coluna esquerda: {str(e)}", exc_info=True)
