from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _clicar_no_para_expandir_hierarquia(self, no):
    try:
        if no in self._nos_expandidos:
            self._nos_expandidos.discard(no)

            def remover_descendentes(n):
                for filho in self._hierarquia_children.get(n, []):
                    self._nos_expandidos.discard(filho)
                    remover_descendentes(filho)

            remover_descendentes(no)

        else:
            self._nos_expandidos.add(no)

        try:
            old_pos = no.pos()

        except Exception:
            old_pos = None

        try:
            if int(getattr(self, "_lumen_reorg_layout_state", 0) or 0) == 1:
                self._lumen_reorg_layout_state = 0
                self._lumen_layout_original_snapshot = None

        except Exception:
            pass

        self._aplicar_visibilidade_por_foco(no, abrir_foco=True)

        try:
            if old_pos is not None:
                no.setPos(old_pos)

                try:
                    snap = getattr(self, "_lumen_layout_original_snapshot", None)
                    if snap and isinstance(snap, dict):
                        pos_map = snap.get("positions") or {}
                        pos_map[no] = no.pos()
                        snap["positions"] = pos_map

                except Exception:
                    pass

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao expandir/recolher hierarquia: {e}", exc_info=True)
