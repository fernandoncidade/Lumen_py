from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def limpar_mapa(self, emitir_mensagem: bool = True):
    try:
        if emitir_mensagem and not MessageBox.mapa_confirm_clear(self):
            return

        self.scene.clear()
        self.nos.clear()
        self.no_origem = None

        self._modo_navegacao_hierarquia = False
        self._hierarquia_root = None
        self._hierarquia_parent = {}
        self._hierarquia_children = {}
        self._nos_expandidos = set()

        self._lumen_reorg_layout_state = 0
        self._lumen_layout_original_positions = {}

        if emitir_mensagem:
            MessageBox.mapa_clear_success(self)

    except Exception as e:
        logger.error(f"Erro ao limpar mapa: {str(e)}", exc_info=True)
        if emitir_mensagem:
            MessageBox.mapa_clear_error(self)
