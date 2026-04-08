import json
import os
from pathlib import Path
from typing import Optional, List
from PySide6.QtWidgets import QTabWidget, QMessageBox, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
logger = LogManager.get_logger()

def _make_placeholder(text: str) -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    lay.addWidget(lbl)
    lay.addStretch(1)
    return w

def setup_ui(self) -> None:
    self.tabs = QTabWidget()
    self.tabs.setMovable(True)
    self.setCentralWidget(self.tabs)

    self._lazy_tabs = {}
    self._default_tab_order = ["leitor", "gerenciador", "mapa", "feynman", "eisenhower"]

    def _tab_title(key: str) -> str:
        titles = {
            "leitor": QCoreApplication.translate("App", "📖 Leitor Acessível"),
            "gerenciador": QCoreApplication.translate("App", "⏱️ Gestão de Tempo"),
            "mapa": QCoreApplication.translate("App", "🧠 Mapas Mentais"),
            "feynman": QCoreApplication.translate("App", "🎓 Método Feynman"),
            "eisenhower": QCoreApplication.translate("App", "🗂️ Matriz Eisenhower"),
        }
        return titles.get(key, "")

    def _get_tabs_persist_file() -> Optional[str]:
        base = obter_caminho_persistente()

        if not base:
            return None

        return str(Path(base) / "ordem_abas.json")

    def _load_tab_order() -> List[str]:
        pf = _get_tabs_persist_file()

        if not pf or not os.path.exists(pf):
            return list(self._default_tab_order)

        try:
            with open(pf, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = data.get("order")

            if not isinstance(data, list):
                return list(self._default_tab_order)

            known = [k for k in data if k in self._default_tab_order]
            missing = [k for k in self._default_tab_order if k not in known]
            return known + missing

        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"Erro ao carregar ordem das abas: {e}", exc_info=True)
            return list(self._default_tab_order)

    def _save_tab_order() -> None:
        pf = _get_tabs_persist_file()

        if not pf:
            return

        try:
            order = []

            for i in range(self.tabs.count()):
                key = self.tabs.tabBar().tabData(i)

                if key:
                    order.append(key)

            with open(pf, "w", encoding="utf-8") as f:
                json.dump({"order": order}, f, ensure_ascii=False, indent=2)

        except OSError as e:
            logger.error(f"Erro ao salvar ordem das abas: {e}", exc_info=True)

    def _apply_tab_titles() -> None:
        for i in range(self.tabs.count()):
            key = self.tabs.tabBar().tabData(i)
            self.tabs.setTabText(i, _tab_title(key))

    def _get_tab_index_by_key(key: str) -> Optional[int]:
        for i in range(self.tabs.count()):
            if self.tabs.tabBar().tabData(i) == key:
                return i

        return None

    def _switch_to_tab_key(key: str) -> None:
        idx = _get_tab_index_by_key(key)

        if idx is not None:
            self.tabs.setCurrentIndex(idx)

    def _rebuild_tabs(order: List[str]) -> None:
        widgets_by_key = {}

        for i in range(self.tabs.count()):
            key = self.tabs.tabBar().tabData(i)

            if key:
                widgets_by_key[key] = self.tabs.widget(i)

        for i in reversed(range(self.tabs.count())):
            self.tabs.removeTab(i)

        for key in order:
            widget = widgets_by_key.get(key)

            if widget is None:
                widget = _make_placeholder(QCoreApplication.translate("App", "Carregando módulo..."))

            idx = self.tabs.addTab(widget, "")
            self.tabs.tabBar().setTabData(idx, key)

        _apply_tab_titles()

    def _reset_tab_order() -> None:
        _rebuild_tabs(list(self._default_tab_order))
        _save_tab_order()

    self._apply_tab_titles = _apply_tab_titles
    self._get_tab_index_by_key = _get_tab_index_by_key
    self._switch_to_tab_key = _switch_to_tab_key
    self.resetar_ordem_abas = _reset_tab_order

    def _register_lazy_tab(key: str, attr_name: str, factory):
        placeholder = _make_placeholder(QCoreApplication.translate("App", "Carregando módulo..."))
        idx = self.tabs.addTab(placeholder, "")
        self.tabs.tabBar().setTabData(idx, key)
        self._lazy_tabs[key] = {
            "attr": attr_name,
            "factory": factory,
            "loaded": False,
        }

    def _ensure_tab_loaded(index: int):
        try:
            key = self.tabs.tabBar().tabData(index)
            info = self._lazy_tabs.get(key)

            if not info or info["loaded"]:
                return

            real_widget = info["factory"]()
            info["loaded"] = True
            setattr(self, info["attr"], real_widget)

            self.tabs.removeTab(index)
            self.tabs.insertTab(index, real_widget, "")
            self.tabs.tabBar().setTabData(index, key)
            self.tabs.setCurrentIndex(index)

            try:
                if hasattr(self, "_registrar_contadores_modulo"):
                    self._registrar_contadores_modulo(key, real_widget)

            except Exception:
                pass

            try:
                _apply_tab_titles()

            except Exception:
                pass

        except Exception as e:
            logger.critical(f"Erro crítico ao lazy-load da aba {index}: {e}", exc_info=True)
            titulo = QCoreApplication.translate("App", "Erro ao Carregar Módulo")
            msg_topo = QCoreApplication.translate("App", "Ocorreu um erro ao carregar o módulo:")
            msg_rodape = QCoreApplication.translate("App", "Verifique se todas as dependências estão instaladas.")
            QMessageBox.critical(self, titulo, f"{msg_topo}\n\n{str(e)}\n\n{msg_rodape}")
            raise

    def _factory_leitor():
        from source.modules.mod_01_leitor_acessivel import LeitorAcessivel
        w = LeitorAcessivel()

        try:
            w.btn_regua.toggled.connect(self.sincronizar_regua_menu)

        except Exception:
            pass

        return w

    def _factory_tempo():
        from source.modules.mod_03_gerenciador_tempo import GerenciadorTempo
        return GerenciadorTempo()

    def _factory_mapa():
        from source.modules.mod_04_mapa_mental import MapaMental
        return MapaMental()

    def _factory_feynman():
        from source.modules.mod_05_metodo_feynman import MetodoFeynman
        return MetodoFeynman()

    def _factory_eisenhower():
        from source.modules.mod_06_eisenhower import MatrizEisenhower
        return MatrizEisenhower(gerenciador_traducao=self.tradutor, embedded=True)

    tab_specs = {
        "leitor": ("leitor", _factory_leitor),
        "gerenciador": ("gerenciador", _factory_tempo),
        "mapa": ("mapa", _factory_mapa),
        "feynman": ("feynman", _factory_feynman),
        "eisenhower": ("eisenhower", _factory_eisenhower),
    }

    for key in _load_tab_order():
        spec = tab_specs.get(key)
        if not spec:
            continue

        attr_name, factory = spec
        _register_lazy_tab(key, attr_name, factory)

    _apply_tab_titles()

    self.tabs.currentChanged.connect(_ensure_tab_loaded)
    self.tabs.tabBar().tabMoved.connect(lambda _from, _to: _save_tab_order())

    _ensure_tab_loaded(self.tabs.currentIndex())
