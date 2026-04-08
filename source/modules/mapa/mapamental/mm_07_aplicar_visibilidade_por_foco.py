from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _aplicar_visibilidade_por_foco(self, foco, abrir_foco: bool):
    try:
        if not self._hierarquia_root:
            return

        original_root = getattr(self, "_hierarquia_root", None)
        if abrir_foco and foco is not None:
            try:
                self._hierarquia_root = foco

            except Exception:
                pass

        vis_antes = {n for n in (getattr(self, "nos", []) or []) if getattr(n, "isVisible", lambda: True)()}
        visiveis = set()
        visiveis.add(self._hierarquia_root)

        for no_exp in self._nos_expandidos:
            if no_exp not in visiveis:
                n = no_exp
                while n is not None:
                    visiveis.add(n)
                    n = self._hierarquia_parent.get(n)

            for filho in self._hierarquia_children.get(no_exp, []):
                visiveis.add(filho)

        for no in self.nos:
            no.setVisible(no in visiveis)

        self._atualizar_visibilidade_linhas()
        orient = str(getattr(self, "_lumen_layout_orientation", "free") or "free").lower()

        if orient in ("vertical", "horizontal"):
            try:
                freeze = bool(getattr(self, "_lumen_layout_freeze_on_click", False))

                if freeze:
                    vis_depois = {n for n in (getattr(self, "nos", []) or []) if getattr(n, "isVisible", lambda: True)()}
                    novos = set(vis_depois - vis_antes)
                    removidos = set(vis_antes - vis_depois)
                    fixos = set(vis_antes & vis_depois)

                    from source.modules.mapa.MapaMental.mm_34_layout_hierarquia_navegacao import (_layout_incremental_preservando_base,)
                    _layout_incremental_preservando_base(self, novos_visiveis=novos, fixos_visiveis=fixos, removidos_visiveis=removidos)

                else:
                    from source.modules.mapa.MapaMental.mm_34_layout_hierarquia_navegacao import (_layout_hierarquia_navegacao,)
                    _layout_hierarquia_navegacao(self)

            except Exception:
                pass

        elif orient == "radial":
            try:
                import math

                nos = getattr(self, "nos", []) or []
                children_map = {n: list(self._hierarquia_children.get(n, []) or []) for n in nos}
                raiz = getattr(self, "_hierarquia_root", None)

                if raiz is None:
                    return

                fila = [raiz]
                visitados = set([raiz])

                while fila:
                    pai = fila.pop(0)
                    filhos = [f for f in children_map.get(pai, []) if getattr(f, "isVisible", lambda: True)()]
                    n = len(filhos)

                    if n == 0:
                        for f in children_map.get(pai, []):
                            if f not in visitados:
                                visitados.add(f)
                                fila.append(f)

                        continue

                    diametros = []

                    for f in filhos:
                        try:
                            rect = f.boundingRect()
                            sc = float(getattr(f, "scale", lambda: 1)()) if callable(getattr(f, "scale", None)) else getattr(f, "scale", 1)
                            w = rect.width() * sc
                            h = rect.height() * sc
                            diametros.append(max(w, h))

                        except Exception:
                            diametros.append(120.0)

                    max_d = max(diametros) if diametros else 120.0
                    pai_parent = self._hierarquia_parent.get(pai)

                    if n == 1:
                        r = max(max_d * 1.5, 200)

                        if pai_parent is None:
                            angs = [-90.0]

                        else:
                            try:
                                dx = pai.scenePos().x() - pai_parent.scenePos().x()
                                dy = pai.scenePos().y() - pai_parent.scenePos().y()
                                angs = [math.degrees(math.atan2(dy, dx))]

                            except Exception:
                                angs = [-90.0]

                    else:
                        if pai_parent is None:
                            try:
                                r_needed = max_d / math.sin(math.pi / max(2, n))

                            except Exception:
                                r_needed = max_d * n / (2 * math.pi)

                            r = max(r_needed, max_d * 1.5, 200)
                            angs = [i * (360.0 / n) for i in range(n)]

                        else:
                            try:
                                dx = pai.scenePos().x() - pai_parent.scenePos().x()
                                dy = pai.scenePos().y() - pai_parent.scenePos().y()
                                center_ang = math.degrees(math.atan2(dy, dx))

                            except Exception:
                                center_ang = -90.0

                            arc_span = min(240.0, max(60.0, 30.0 * n))
                            step_count = max(1, n - 1)
                            arc_span_rad = math.radians(arc_span)
                            delta = arc_span_rad / step_count

                            try:
                                r_needed = max_d / (2.0 * math.sin(delta / 2.0))

                            except Exception:
                                r_needed = max_d * n / (2 * math.pi)

                            r = max(r_needed, max_d * 1.2, 120)
                            start_ang = center_ang - (arc_span / 2.0)

                            if n == 1:
                                angs = [center_ang]

                            else:
                                angs = [start_ang + i * (arc_span / max(1, n - 1)) for i in range(n)]

                            def _is_descendant_of(node_check, ancestor):
                                try:
                                    p = self._hierarquia_parent.get(node_check)

                                    while p is not None:
                                        if p is ancestor:
                                            return True

                                        p = self._hierarquia_parent.get(p)

                                except Exception:
                                    pass

                                return False

                            existing_positions = []
                            for node in nos:
                                try:
                                    if node is None or node is pai:
                                        continue

                                    if not getattr(node, 'isVisible', lambda: True)():
                                        continue

                                    if _is_descendant_of(node, pai) or _is_descendant_of(pai, node):
                                        continue

                                    sc = getattr(node, 'scale', 1)

                                    try:
                                        sc = float(sc() if callable(sc) else sc)

                                    except Exception:
                                        sc = 1.0

                                    ex_d = max(node.boundingRect().width(), node.boundingRect().height()) * sc
                                    existing_positions.append((node.scenePos().x(), node.scenePos().y(), ex_d))

                                except Exception:
                                    continue

                            safe = False
                            max_iter = 12
                            it = 0

                            while not safe and it < max_iter:
                                safe = True

                                for ang in angs:
                                    ang_rad = math.radians(ang)
                                    fx_test = pai.scenePos().x() + r * math.cos(ang_rad)
                                    fy_test = pai.scenePos().y() + r * math.sin(ang_rad)

                                    for (ex_x, ex_y, ex_d) in existing_positions:
                                        dx_e = fx_test - ex_x
                                        dy_e = fy_test - ex_y
                                        dist = math.hypot(dx_e, dy_e)

                                        if dist < (max_d + ex_d) * 0.5 + 8.0:
                                            safe = False
                                            break

                                    if not safe:
                                        break

                                if not safe:
                                    r *= 1.25
                                    it += 1

                    px = pai.scenePos().x()
                    py = pai.scenePos().y()

                    for f, ang in zip(filhos, angs):
                        ang_rad = math.radians(ang)

                        try:
                            fx = px + r * math.cos(ang_rad)
                            fy = py + r * math.sin(ang_rad)
                            f.setPos(fx, fy)

                            try:
                                self._expandir_area_se_necessario(f)

                            except Exception:
                                pass

                        except Exception:
                            pass

                        if f not in visitados:
                            visitados.add(f)
                            fila.append(f)

                try:
                    self._atualizar_visibilidade_linhas()

                except Exception:
                    pass

            except Exception as e:
                logger.error(f"Erro no layout radial: {e}", exc_info=True)

        if abrir_foco and foco is not None:
            try:
                self._hierarquia_root = original_root

            except Exception:
                pass

    except Exception as e:
        logger.error(f"Erro ao aplicar visibilidade por foco: {e}", exc_info=True)
