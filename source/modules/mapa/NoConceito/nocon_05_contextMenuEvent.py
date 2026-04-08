from PySide6.QtWidgets import QMenu
from PySide6.QtCore import QCoreApplication, QTimer
from source.modules.mapa.mp_02_LinhaConexao import LinhaConexao
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def _ptr(obj):
    try:
        from shiboken6 import getCppPointer, isValid

        if obj is None or not isValid(obj):
            return None

        return int(getCppPointer(obj)[0])

    except Exception:
        return id(obj) if obj is not None else None

def _obter_owner_mapa(no):
    try:
        scene = no.scene()

        if scene is None:
            return None

        for view in scene.views():
            pai = view.parent()

            while pai is not None:
                if hasattr(pai, "nos") and hasattr(pai, "scene"):
                    return pai

                pai = pai.parent()

    except Exception:
        pass

    return None

def _excluir_nos(scene, owner, nos_alvo, parent_for_msg):
    try:
        nos_alvo = [n for n in (nos_alvo or []) if n is not None]

        if not nos_alvo:
            return

        nos_ptrs = {_ptr(n) for n in nos_alvo if _ptr(n) is not None}

        if not nos_ptrs:
            return

        try:
            no_origem = getattr(owner, "no_origem", None) if owner is not None else None

            if _ptr(no_origem) in nos_ptrs:
                owner.no_origem = None

        except Exception:
            pass

        linhas_para_remover = []

        try:
            for item in list(scene.items()):
                if isinstance(item, LinhaConexao):
                    ini = getattr(item, "no_inicio", None)
                    fim = getattr(item, "no_fim", None)

                    if _ptr(ini) in nos_ptrs or _ptr(fim) in nos_ptrs:
                        linhas_para_remover.append(item)

        except Exception:
            linhas_para_remover = []

        for linha in linhas_para_remover:
            try:
                inicio = getattr(linha, "no_inicio", None)
                fim = getattr(linha, "no_fim", None)

                if inicio is not None and hasattr(inicio, "conexoes") and linha in (inicio.conexoes or []):
                    inicio.conexoes.remove(linha)

                if fim is not None and hasattr(fim, "conexoes") and linha in (fim.conexoes or []):
                    fim.conexoes.remove(linha)

                scene.removeItem(linha)

            except Exception:
                pass

        nos_scene = []

        try:
            for item in list(scene.items()):
                if hasattr(item, "conexoes") and hasattr(item, "texto") and _ptr(item) in nos_ptrs:
                    nos_scene.append(item)

        except Exception:
            nos_scene = list(nos_alvo)

        for no in nos_scene:
            try:
                if owner is not None:
                    owner.nos = [n for n in (getattr(owner, "nos", []) or []) if _ptr(n) not in nos_ptrs]

            except Exception:
                pass

            try:
                no.setSelected(False)
                no.setVisible(False)
                scene.removeItem(no)

            except Exception:
                pass

        try:
            if owner is not None:
                owner.nos = [n for n in (getattr(owner, "nos", []) or []) if getattr(n, "scene", lambda: None)() is scene]

        except Exception:
            pass

        if owner is not None:
            try:
                parent_map = dict(getattr(owner, "_hierarquia_parent", {}) or {})
                children_map = dict(getattr(owner, "_hierarquia_children", {}) or {})
                expandidos = set(getattr(owner, "_nos_expandidos", set()) or set())

                for pai, filhos in list(children_map.items()):
                    children_map[pai] = [f for f in (filhos or []) if _ptr(f) not in nos_ptrs]

                for no_key in list(parent_map.keys()):
                    if _ptr(no_key) not in nos_ptrs:
                        continue

                    pai = parent_map.pop(no_key, None)

                    if pai in children_map:
                        children_map[pai] = [f for f in (children_map.get(pai, []) or []) if _ptr(f) not in nos_ptrs]

                    children_map.pop(no_key, None)
                    expandidos = {n for n in expandidos if _ptr(n) not in nos_ptrs}

                root = getattr(owner, "_hierarquia_root", None)

                if _ptr(root) in nos_ptrs:
                    owner._hierarquia_root = owner.nos[0] if getattr(owner, "nos", []) else None

                owner._hierarquia_parent = parent_map
                owner._hierarquia_children = children_map
                owner._nos_expandidos = expandidos

                if hasattr(owner, "_atualizar_visibilidade_linhas"):
                    owner._atualizar_visibilidade_linhas()

            except Exception:
                logger.debug("Falha ao ajustar estrutura de hierarquia após exclusão de nós", exc_info=True)

        try:
            scene.clearSelection()
            scene.invalidate()
            scene.update()

        except Exception:
            pass

        try:
            if owner is not None:
                view = getattr(owner, "view", None)

                if view is not None and hasattr(view, "viewport"):
                    view.viewport().update()

        except Exception:
            pass

        MessageBox.mapa_delete_nodes_success(parent_for_msg)

    except Exception as e:
        logger.error(f"Erro ao excluir nó(s) do mapa mental: {e}", exc_info=True)
        MessageBox.mapa_delete_nodes_error(parent_for_msg)

def contextMenuEvent(self, event):
    try:
        scene = self.scene()

        if scene is None:
            return

        if not self.isSelected():
            try:
                scene.clearSelection()

            except Exception:
                pass

            self.setSelected(True)

        selecionados = [item for item in scene.selectedItems() if hasattr(item, "conexoes") and hasattr(item, "texto")]
        nos_alvo = selecionados if len(selecionados) > 1 else [self]

        if self not in nos_alvo:
            nos_alvo.append(self)

        vistos = set()
        nos_alvo = [n for n in nos_alvo if not (id(n) in vistos or vistos.add(id(n)))]
        nomes = [getattr(no, "texto", "") for no in nos_alvo]

        menu = QMenu()
        ac_excluir = menu.addAction(QCoreApplication.translate("App", "Excluir Nó(s) e Conexão(ões) 🪢"))
        escolhido = menu.exec(event.screenPos())

        if escolhido is not ac_excluir:
            return

        if not MessageBox.mapa_confirm_delete_nodes(self, nomes):
            return

        owner = _obter_owner_mapa(self)
        QTimer.singleShot(0, lambda sc=scene, ow=owner, ns=list(nos_alvo), p=self: _excluir_nos(sc, ow, ns, p))

    except Exception as e:
        logger.error(f"Erro ao excluir nó(s) do mapa mental: {e}", exc_info=True)
        MessageBox.mapa_delete_nodes_error(self)
