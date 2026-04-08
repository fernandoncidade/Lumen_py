from PySide6.QtGui import QColor, QBrush
from source.utils.LogManager import LogManager
from source.modules.mapa.mp_02_LinhaConexao import LinhaConexao
logger = LogManager.get_logger()

def clicar_no_para_conectar(self, event, no):
    try:
        if not self.modo_conexao:
            return

        if self.no_origem is None:
            self.no_origem = no
            no.setBrush(QBrush(QColor("#ffc107")))

        else:
            if self.no_origem != no:
                linha = LinhaConexao(self.no_origem, no)
                self.scene.addItem(linha)

                try:
                    if getattr(self, "_modo_navegacao_hierarquia", False):
                        parent_map = getattr(self, "_hierarquia_parent", None) or {}
                        children_map = getattr(self, "_hierarquia_children", None) or {}
                        raiz = getattr(self, "_hierarquia_root", None)

                        def _ensure_child(pai, filho):
                            parent_map[filho] = pai
                            filhos = children_map.setdefault(pai, [])

                            if filho not in filhos:
                                filhos.append(filho)

                            children_map.setdefault(filho, [])

                        def _is_ia_node(n):
                            try:
                                return hasattr(n, "_lumen_hierarquia_payload") or hasattr(n, "_lumen_ideia_payload")

                            except Exception:
                                return False

                        def _is_descendant(child, ancestor):
                            try:
                                p = parent_map.get(child)

                                while p is not None:
                                    if p is ancestor:
                                        return True

                                    p = parent_map.get(p)

                            except Exception:
                                pass

                            return False

                        def _detach_from_parent(child):
                            try:
                                old_parent = parent_map.get(child)

                                if old_parent is None:
                                    return

                                filhos_old = children_map.get(old_parent, [])

                                if child in filhos_old:
                                    try:
                                        filhos_old.remove(child)

                                    except Exception:
                                        pass

                            except Exception:
                                pass

                        a = self.no_origem
                        b = no
                        a_in = a in parent_map or a is raiz
                        b_in = b in parent_map or b is raiz

                        if a_in and not b_in:
                            _ensure_child(a, b)

                            try:
                                self._nos_expandidos.add(a)

                            except Exception:
                                pass

                        elif b_in and not a_in:
                            _ensure_child(b, a)

                            try:
                                self._nos_expandidos.add(b)

                            except Exception:
                                pass

                        elif not a_in and not b_in:
                            if raiz is None:
                                self._hierarquia_root = a
                                parent_map[a] = None
                                children_map.setdefault(a, [])
                                _ensure_child(a, b)

                            else:
                                _ensure_child(raiz, a)
                                _ensure_child(raiz, b)

                            try:
                                self._nos_expandidos.add(self._hierarquia_root)

                            except Exception:
                                pass

                        else:
                            ia = a if _is_ia_node(a) else (b if _is_ia_node(b) else None)
                            manual = b if ia is a else (a if ia is b else None)

                            if ia is not None and manual is not None:
                                if not _is_descendant(ia, manual):
                                    _detach_from_parent(manual)
                                    _ensure_child(ia, manual)

                                    try:
                                        self._nos_expandidos.add(ia)

                                    except Exception:
                                        pass

                        self._hierarquia_parent = parent_map
                        self._hierarquia_children = children_map

                        if hasattr(self, "_instalar_handlers_nos"):
                            self._instalar_handlers_nos()

                        if hasattr(self, "_aplicar_visibilidade_por_foco"):
                            alvo = self._hierarquia_root or a
                            self._aplicar_visibilidade_por_foco(alvo, abrir_foco=True)

                except Exception:
                    pass

            self.no_origem.setBrush(QBrush(self.no_origem.cor))
            self.no_origem = None

    except Exception as e:
        logger.error(f"Erro ao conectar nós: {str(e)}", exc_info=True)
