import json
import os
import hashlib
from PySide6.QtCore import QTimer
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.modules.mapa.mp_02_LinhaConexao import LinhaConexao
logger = LogManager.get_logger()

def _serializar_mapa(self) -> dict:
    nos = getattr(self, "nos", []) or []
    idx_by_no = {no: i for i, no in enumerate(nos)}

    def _safe_payload(valor):
        if valor is None:
            return None

        if isinstance(valor, (str, int, float, bool)):
            return valor

        if isinstance(valor, (list, tuple)):
            return [v for v in valor]

        if isinstance(valor, dict):
            return dict(valor)

        return None

    dados_nos = []
    for no in nos:
        try:
            info_associada = getattr(no, "info_associada", []) or []
            info_associada = list(info_associada)

        except Exception:
            info_associada = []

        no_data = {
            "texto": getattr(no, "texto", ""),
            "x": no.scenePos().x(),
            "y": no.scenePos().y(),
            "cor": getattr(getattr(no, "cor", None), "name", lambda: "#0078d4")(),
            "notas": getattr(no, "notas", ""),
            "info_associada": info_associada,
            "arquivo_vinculado": getattr(no, "arquivo_vinculado", None),
            "visivel": getattr(no, "isVisible", lambda: True)(),
        }

        payload_h = _safe_payload(getattr(no, "_lumen_hierarquia_payload", None))
        if payload_h is not None:
            no_data["hierarquia_payload"] = payload_h

        payload_i = _safe_payload(getattr(no, "_lumen_ideia_payload", None))
        if payload_i is not None:
            no_data["ideia_payload"] = payload_i

        nivel_h = getattr(no, "_lumen_hierarquia_nivel", None)
        if nivel_h is not None:
            no_data["hierarquia_nivel"] = nivel_h

        tipo_h = getattr(no, "_lumen_hierarquia_tipo", None)
        if tipo_h is not None:
            no_data["hierarquia_tipo"] = tipo_h

        dados_nos.append(no_data)

    conexoes = []
    for item in getattr(self, "scene", None).items() if getattr(self, "scene", None) is not None else []:
        if isinstance(item, LinhaConexao):
            try:
                inicio = idx_by_no.get(item.no_inicio, None)
                fim = idx_by_no.get(item.no_fim, None)
                if inicio is None or fim is None:
                    continue

                conexoes.append({"inicio": inicio, "fim": fim})

            except Exception:
                continue

    hierarquia_parent = getattr(self, "_hierarquia_parent", {}) or {}
    hierarquia_children = getattr(self, "_hierarquia_children", {}) or {}
    nos_expandidos = getattr(self, "_nos_expandidos", set()) or set()
    raiz_no = getattr(self, "_hierarquia_root", None)

    parent_idx = {}
    for filho, pai in hierarquia_parent.items():
        if filho not in idx_by_no:
            continue

        parent_idx[str(idx_by_no[filho])] = idx_by_no[pai] if pai in idx_by_no else None

    children_idx = {}
    for pai, filhos in hierarquia_children.items():
        if pai not in idx_by_no:
            continue

        filhos_idx = []
        for filho in filhos or []:
            if filho in idx_by_no:
                filhos_idx.append(idx_by_no[filho])

        children_idx[str(idx_by_no[pai])] = filhos_idx

    expandidos_idx = [idx_by_no[n] for n in nos_expandidos if n in idx_by_no]
    raiz_idx = idx_by_no.get(raiz_no, None)

    config = {}
    try:
        scene = getattr(self, "scene", None)
        if scene is not None:
            config["scene_rect"] = [
                float(scene.sceneRect().x()),
                float(scene.sceneRect().y()),
                float(scene.sceneRect().width()),
                float(scene.sceneRect().height()),
            ]

            config["grid_step"] = int(getattr(scene, "_grid_step", 40) or 40)
            config["snap_enabled"] = bool(getattr(scene, "_snap_enabled", True))

    except Exception:
        pass

    try:
        view = getattr(self, "view", None)
        if view is not None:
            t = view.transform()
            config["view_transform"] = [
                float(t.m11()), float(t.m12()), float(t.m13()),
                float(t.m21()), float(t.m22()), float(t.m23()),
                float(t.m31()), float(t.m32()), float(t.m33()),
            ]
            config["view_zoom"] = int(getattr(view, "_current_zoom", 0) or 0)

    except Exception:
        pass

    dados = {
        "versao": 3,
        "nos": dados_nos,
        "conexoes": conexoes,
        "hierarquia": {
            "modo": bool(getattr(self, "_modo_navegacao_hierarquia", False)),
            "root_idx": raiz_idx,
            "parent": parent_idx,
            "children": children_idx,
            "expandidos": expandidos_idx,
        },
        "layout": {
            "orientation": str(getattr(self, "_lumen_layout_orientation", "free") or "free"),
            "freeze_on_click": bool(getattr(self, "_lumen_layout_freeze_on_click", False)),
            "reorg_state": int(getattr(self, "_lumen_reorg_layout_state", 0) or 0),
        },
        "config": config,
    }

    return dados

def _salvar_mapa_em_arquivo(self, caminho: str) -> bool:
    try:
        dados = _serializar_mapa(self)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        logger.error(f"Erro ao salvar mapa mental: {e}", exc_info=True)
        return False

def _salvar_backup_automatico(self):
    try:
        if getattr(self, "_lumen_backup_paused", False):
            return

        dados = _serializar_mapa(self)
        hash_atual = hashlib.sha256(json.dumps(dados, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        if hash_atual == getattr(self, "_lumen_backup_last_hash", None):
            return

        base_dir = getattr(self, "caminho_persistente", None) or obter_caminho_persistente()
        caminho = os.path.join(base_dir, "mapa_mental.json")
        if _salvar_mapa_em_arquivo(self, caminho):
            self._lumen_backup_last_hash = hash_atual

    except Exception as e:
        logger.error(f"Erro ao salvar backup do mapa mental: {e}", exc_info=True)

def _configurar_backup_automatico(self, intervalo_ms: int = 8000):
    try:
        timer = getattr(self, "_lumen_backup_timer", None)
        if isinstance(timer, QTimer):
            return

        timer = QTimer(self)
        timer.setInterval(int(intervalo_ms))
        timer.timeout.connect(lambda: _salvar_backup_automatico(self))
        timer.start()
        self._lumen_backup_timer = timer

    except Exception as e:
        logger.error(f"Erro ao configurar backup automatico: {e}", exc_info=True)
