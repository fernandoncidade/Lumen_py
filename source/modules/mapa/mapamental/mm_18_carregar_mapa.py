import os
import json
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QColor, QTransform, QPen
from source.utils.LogManager import LogManager
from source.modules.mapa.mp_01_NoConceito import NoConceito
from source.modules.mapa.mp_02_LinhaConexao import LinhaConexao
logger = LogManager.get_logger()

def _carregar_mapa_de_arquivo(self, arquivo: str, silencioso: bool = False) -> bool:
    try:
        if not arquivo or not os.path.exists(arquivo):
            return False

        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        try:
            self._lumen_backup_paused = True

        except Exception:
            pass

        self.limpar_mapa(emitir_mensagem=False)

        for no_data in dados['nos']:
            no = NoConceito(no_data['x'], no_data['y'], no_data['texto'], QColor(no_data['cor']))
            no.notas = no_data.get('notas', '')
            no.info_associada = list(no_data.get('info_associada', []) or [])

            if no_data.get('arquivo_vinculado'):
                try:
                    no.set_arquivo_vinculado(no_data.get('arquivo_vinculado'))

                except Exception:
                    no.arquivo_vinculado = no_data.get('arquivo_vinculado')

            if 'hierarquia_payload' in no_data:
                no._lumen_hierarquia_payload = no_data.get('hierarquia_payload')

            if 'ideia_payload' in no_data:
                no._lumen_ideia_payload = no_data.get('ideia_payload')

            if 'hierarquia_nivel' in no_data:
                no._lumen_hierarquia_nivel = no_data.get('hierarquia_nivel')

            if 'hierarquia_tipo' in no_data:
                no._lumen_hierarquia_tipo = no_data.get('hierarquia_tipo')

            self.scene.addItem(no)
            self.nos.append(no)

            try:
                no._badge.setVisible(bool(no.notas))

            except Exception:
                pass

        for con_data in dados.get('conexoes', []):
            try:
                ini = con_data.get('inicio')
                fim = con_data.get('fim')

                if ini is None or fim is None:
                    continue

                if not (0 <= ini < len(self.nos) and 0 <= fim < len(self.nos)):
                    continue

                linha = LinhaConexao(self.nos[ini], self.nos[fim])
                estilo = con_data.get("estilo", {}) or {}

                if isinstance(estilo, dict) and estilo:
                    try:
                        cor = QColor(str(estilo.get("cor", "#b4b4b4")))
                        alpha = estilo.get("alpha")

                        if alpha is not None:
                            cor.setAlpha(max(0, min(255, int(alpha))))

                        largura = float(estilo.get("largura", 2.0))
                        largura = max(0.1, largura)

                        linha_estilo = estilo.get("linha_estilo")

                        if linha_estilo is None:
                            linha_estilo = int(Qt.SolidLine)

                        elif hasattr(linha_estilo, "value"):
                            linha_estilo = int(linha_estilo.value)

                        else:
                            linha_estilo = int(linha_estilo)

                        pen = QPen(cor, largura, Qt.PenStyle(linha_estilo))
                        pen.setCosmetic(bool(estilo.get("cosmetica", True)))
                        linha.setPen(pen)

                    except Exception:
                        pass

                self.scene.addItem(linha)

            except Exception:
                pass

        hier = dados.get('hierarquia', {}) or {}
        try:
            self._modo_navegacao_hierarquia = bool(hier.get('modo', False))
            root_idx = hier.get('root_idx')
            self._hierarquia_root = self.nos[root_idx] if isinstance(root_idx, int) and 0 <= root_idx < len(self.nos) else None

            parent_map = {}

            for filho_idx_str, pai_idx in (hier.get('parent', {}) or {}).items():
                try:
                    filho_idx = int(filho_idx_str)

                    if not (0 <= filho_idx < len(self.nos)):
                        continue

                    filho = self.nos[filho_idx]
                    pai = self.nos[pai_idx] if isinstance(pai_idx, int) and 0 <= pai_idx < len(self.nos) else None
                    parent_map[filho] = pai

                except Exception:
                    continue

            children_map = {}

            for pai_idx_str, filhos_idx in (hier.get('children', {}) or {}).items():
                try:
                    pai_idx = int(pai_idx_str)

                    if not (0 <= pai_idx < len(self.nos)):
                        continue

                    filhos = []

                    for fi in filhos_idx or []:
                        if isinstance(fi, int) and 0 <= fi < len(self.nos):
                            filhos.append(self.nos[fi])

                    children_map[self.nos[pai_idx]] = filhos

                except Exception:
                    continue

            self._hierarquia_parent = parent_map
            self._hierarquia_children = children_map
            self._nos_expandidos = set(self.nos[i] for i in (hier.get('expandidos', []) or []) if isinstance(i, int) and 0 <= i < len(self.nos))

            if not (dados.get("conexoes", []) or []):
                try:
                    existentes = set()

                    for item in self.scene.items():
                        if isinstance(item, LinhaConexao):
                            par = tuple(sorted((id(item.no_inicio), id(item.no_fim))))
                            existentes.add(par)

                    for filho, pai in parent_map.items():
                        if pai is None:
                            continue

                        par = tuple(sorted((id(filho), id(pai))))

                        if par in existentes:
                            continue

                        linha = LinhaConexao(pai, filho)

                        if hasattr(filho, "_lumen_ideia_payload"):
                            pen = QPen(QColor(34, 139, 34, 150), 1, Qt.DashLine)
                            pen.setCosmetic(True)
                            linha.setPen(pen)

                        else:
                            nivel_filho = int(getattr(filho, "_lumen_hierarquia_nivel", 1) or 1)
                            espessura = max(4 - nivel_filho, 1)
                            pen = QPen(QColor(101, 67, 33), espessura, Qt.SolidLine)
                            pen.setCosmetic(True)
                            linha.setPen(pen)

                        self.scene.addItem(linha)
                        existentes.add(par)

                except Exception:
                    pass

            if self._modo_navegacao_hierarquia:
                if self._hierarquia_root is None and self.nos:
                    self._hierarquia_root = self.nos[0]

                for no in self.nos:
                    self._hierarquia_children.setdefault(no, [])

                if hasattr(self, "_instalar_handlers_nos"):
                    self._instalar_handlers_nos()

        except Exception:
            pass

        layout = dados.get('layout', {}) or {}

        try:
            self._lumen_layout_orientation = str(layout.get('orientation', 'free') or 'free')
            self._lumen_layout_freeze_on_click = bool(layout.get('freeze_on_click', False))

        except Exception:
            pass

        config = dados.get('config', {}) or {}

        try:
            scene = getattr(self, "scene", None)

            if scene is not None:
                rect = config.get("scene_rect")

                if isinstance(rect, (list, tuple)) and len(rect) == 4:
                    scene.setSceneRect(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))

                if "grid_step" in config:
                    scene._grid_step = int(config.get("grid_step") or 40)

                if "snap_enabled" in config:
                    scene._snap_enabled = bool(config.get("snap_enabled"))

        except Exception:
            pass

        try:
            view = getattr(self, "view", None)

            if view is not None:
                tf = config.get("view_transform")

                if isinstance(tf, (list, tuple)) and len(tf) == 9:
                    view.setTransform(QTransform(*[float(v) for v in tf]))

                if "view_zoom" in config:
                    view._current_zoom = int(config.get("view_zoom") or 0)

        except Exception:
            pass

        saved_nodes = dados.get('nos', []) or []

        for i, no in enumerate(self.nos):
            try:
                if i < len(saved_nodes) and 'visivel' in saved_nodes[i]:
                    no.setVisible(bool(saved_nodes[i].get('visivel', True)))

            except Exception:
                pass

        if hasattr(self, "_atualizar_visibilidade_linhas"):
            self._atualizar_visibilidade_linhas()

        try:
            self._lumen_backup_last_hash = None

        except Exception:
            pass

        try:
            self._lumen_backup_paused = False

        except Exception:
            pass

        return True

    except Exception as e:
        logger.error(f"Erro ao carregar mapa mental: {str(e)}", exc_info=True)
        return False

def carregar_mapa(self):
    try:
        arquivo, _ = QFileDialog.getOpenFileName(
            self, 
            QCoreApplication.translate("App", "Carregar Mapa Mental"), 
            self.caminho_persistente, 
            QCoreApplication.translate("App", "JSON Files (*.json)")
        )

        if arquivo:
            _carregar_mapa_de_arquivo(self, arquivo)

    except Exception as e:
        logger.error(f"Erro ao carregar mapa mental: {str(e)}", exc_info=True)

def _carregar_backup_automatico(self) -> bool:
    try:
        base_dir = getattr(self, "caminho_persistente", None)

        if not base_dir:
            from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
            base_dir = obter_caminho_persistente()

        caminho = os.path.join(base_dir, "mapa_mental.json")
        return _carregar_mapa_de_arquivo(self, caminho, silencioso=True)

    except Exception as e:
        logger.error(f"Erro ao carregar backup automatico: {str(e)}", exc_info=True)
        return False
