from source.utils.LogManager import LogManager
from source.modules.mapa.mp_04_ProcessadorIA import ProcessadorIA
logger = LogManager.get_logger()

def restaurar_com_ia(self):
    try:
        if not self.nos:
            logger.warning("Nenhum conceito para reorganizar")
            return

        try:
            self._lumen_layout_freeze_on_click = True

        except Exception:
            pass

        raiz_no = getattr(self, "_hierarquia_root", None) or (self.nos[0] if self.nos else None)

        try:
            try:
                self._lumen_layout_orientation = "radial"

            except Exception:
                pass

            if hasattr(self, "_habilitar_navegacao_hierarquia"):
                try:
                    self._habilitar_navegacao_hierarquia(raiz_no)

                except Exception:
                    for no in self.nos:
                        try:
                            no.setVisible(no is raiz_no)

                        except Exception:
                            pass

                    self._nos_expandidos = set()
                    self._hierarquia_root = raiz_no

                    try:
                        self._instalar_handlers_nos()

                    except Exception:
                        pass

            else:
                for no in self.nos:
                    try:
                        no.setVisible(no is raiz_no)

                    except Exception:
                        pass

                self._nos_expandidos = set()
                self._hierarquia_root = raiz_no

                try:
                    self._instalar_handlers_nos()

                except Exception:
                    pass

            logger.info("Mapa restaurado para estado inicial: apenas nó pai visível")

            try:
                nos = (getattr(self, "nos", []) or [])

                self._lumen_layout_original_snapshot = {
                    "positions": {no: no.pos() for no in nos},
                    "visible": {no: getattr(no, "isVisible", lambda: True)() for no in nos},
                    "modo_hierarquia": bool(getattr(self, "_modo_navegacao_hierarquia", False)),
                    "hierarquia_root": getattr(self, "_hierarquia_root", None),
                    "hierarquia_parent": dict(getattr(self, "_hierarquia_parent", {}) or {}),
                    "hierarquia_children": dict(getattr(self, "_hierarquia_children", {}) or {}),
                    "nos_expandidos": set(getattr(self, "_nos_expandidos", set()) or set()),
                    "freeze_on_click": bool(getattr(self, "_lumen_layout_freeze_on_click", False)),
                    "orientation": str(getattr(self, "_lumen_layout_orientation", "free") or "free"),
                }

                try:
                    self._lumen_layout_original_positions = {}

                except Exception:
                    pass

                try:
                    self._lumen_reorg_layout_state = 1

                except Exception:
                    pass

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao restaurar estado inicial: {str(e)}", exc_info=True)

    except Exception as e:
        logger.error(f"Erro ao reorganizar com IA: {str(e)}", exc_info=True)
