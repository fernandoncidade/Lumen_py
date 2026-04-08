from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _instalar_handlers_nos(self):
    try:
        for no in self.nos:
            if not hasattr(no, "_lumen_mousePressEvent_original"):
                no._lumen_mousePressEvent_original = no.mousePressEvent

            if not hasattr(no, "_lumen_mouseReleaseEvent_original"):
                no._lumen_mouseReleaseEvent_original = getattr(no, "mouseReleaseEvent", None)

            def _press_handler(event, n=no):
                try:
                    try:
                        n._lumen_press_scene_pos = event.scenePos()
                        n._lumen_pos_at_press = n.scenePos()

                    except Exception:
                        n._lumen_press_scene_pos = None
                        n._lumen_pos_at_press = None

                    return n._lumen_mousePressEvent_original(event)

                except Exception as ex:
                    logger.error(f"Erro no press handler do nó: {ex}", exc_info=True)
                    return n._lumen_mousePressEvent_original(event)

            no.mousePressEvent = _press_handler

            def _release_handler(event, n=no):
                try:
                    if n._lumen_mouseReleaseEvent_original:
                        n._lumen_mouseReleaseEvent_original(event)

                    if event.button() != Qt.LeftButton:
                        return

                    moved = False
                    try:
                        pos_at_press = getattr(n, "_lumen_pos_at_press", None)
                        if pos_at_press is not None:
                            dx = n.scenePos().x() - pos_at_press.x()
                            dy = n.scenePos().y() - pos_at_press.y()
                            if (dx * dx + dy * dy) > (4.0):
                                moved = True

                    except Exception:
                        moved = False

                    if moved:
                        try:
                            snap = getattr(self, "_lumen_layout_original_snapshot", None)
                            if snap and isinstance(snap, dict):
                                pos_map = snap.get("positions") or {}
                                pos_map[n] = n.pos()
                                snap["positions"] = pos_map

                        except Exception:
                            pass

                    if not moved:
                        if self.modo_conexao:
                            self.clicar_no_para_conectar(event, n)
                            return

                        if self._modo_navegacao_hierarquia:
                            self._clicar_no_para_expandir_hierarquia(n)

                except Exception as ex:
                    logger.error(f"Erro no release handler do nó: {ex}", exc_info=True)

            no.mouseReleaseEvent = _release_handler

    except Exception as e:
        logger.error(f"Erro ao instalar handlers nos nós: {e}", exc_info=True)
