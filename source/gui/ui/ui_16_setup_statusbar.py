from functools import partial
from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_statusbar(self):
    try:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_module_label = QLabel("")
        self.status_bar.addWidget(self.status_module_label, 1)
        self.status_selection_label = QLabel("")
        self.status_bar.addPermanentWidget(self.status_selection_label)
        self._status_selection_counts = {}
        self._status_connected_modules = set()

        def _plural(pt_singular: str, pt_plural: str, total: int) -> str:
            return pt_singular if int(total) == 1 else pt_plural

        def _active_tab_key():
            try:
                idx = self.tabs.currentIndex()

                if idx < 0:
                    return None

                return self.tabs.tabBar().tabData(idx)

            except Exception:
                return None

        def _is_qt_alive(obj) -> bool:
            if obj is None:
                return False

            try:
                from shiboken6 import isValid
                return bool(isValid(obj))

            except Exception:
                return True

        def _render_status():
            try:
                idx = self.tabs.currentIndex() if hasattr(self, "tabs") else -1

                if idx < 0:
                    self.status_module_label.setText(QCoreApplication.translate("App", "Pronto"))
                    self.status_selection_label.setText("")
                    return

                tab_name = self.tabs.tabText(idx)
                self.status_module_label.setText(QCoreApplication.translate("App", "Módulo ativo: {tab_name}").format(tab_name=tab_name))

                current_key = _active_tab_key()
                info = self._status_selection_counts.get(current_key)

                if not info:
                    self.status_selection_label.setText("")
                    return

                tipo = info.get("tipo")
                count = int(info.get("count", 0) or 0)

                if count <= 0:
                    self.status_selection_label.setText("")
                    return

                if tipo == "tarefas":
                    nome = _plural(QCoreApplication.translate("App", "tarefa"), QCoreApplication.translate("App", "tarefas"), count)

                elif tipo == "conceitos":
                    nome = _plural(QCoreApplication.translate("App", "conceito"), QCoreApplication.translate("App", "conceitos"), count)

                elif tipo == "nos":
                    nome = _plural(QCoreApplication.translate("App", "nó"), QCoreApplication.translate("App", "nós"), count)

                else:
                    nome = _plural(QCoreApplication.translate("App", "item"), QCoreApplication.translate("App", "itens"), count)

                self.status_selection_label.setText(QCoreApplication.translate("App", "Selecionados: {count} {nome}").format(count=count, nome=nome))

            except Exception as e:
                logger.error(f"Erro ao renderizar status da barra: {e}", exc_info=True)

        def _set_selection_count(module_key: str, tipo: str, count: int):
            try:
                self._status_selection_counts[module_key] = {"tipo": tipo, "count": max(0, int(count or 0))}
                _render_status()

            except Exception as e:
                logger.error(f"Erro ao definir contagem de seleção: {e}", exc_info=True)

        def _count_selected_tempo(tempo_widget):
            try:
                tarefas = getattr(tempo_widget, "tarefas", None)

                if tarefas is None:
                    _set_selection_count("gerenciador", "tarefas", 0)
                    return

                listas = []

                for col_name in ("col_todo", "col_doing", "col_done"):
                    col = getattr(tarefas, col_name, None)
                    lst = getattr(col, "lista", None) if col is not None else None

                    if lst is not None:
                        listas.append(lst)

                total = sum(len(lst.selectedItems() or []) for lst in listas)
                _set_selection_count("gerenciador", "tarefas", total)

            except Exception as e:
                logger.error(f"Erro ao contar seleção do módulo Gestão de Tempo: {e}", exc_info=True)

        def _count_selected_eisenhower(eisenhower_widget):
            try:
                list_names = (
                    "quadrant1_list",
                    "quadrant2_list",
                    "quadrant3_list",
                    "quadrant4_list",
                    "quadrant1_completed_list",
                    "quadrant2_completed_list",
                    "quadrant3_completed_list",
                    "quadrant4_completed_list",
                )
                total = 0

                for name in list_names:
                    lst = getattr(eisenhower_widget, name, None)

                    if lst is not None:
                        total += len(lst.selectedItems() or [])

                try:
                    cp = getattr(eisenhower_widget, "calendar_pane", None)
                    panel = getattr(cp, "calendar_panel", None) if cp is not None else None
                    global_list = getattr(panel, "tasks_list", None) if panel is not None else None

                    if global_list is not None:
                        total += len(global_list.selectedItems() or [])

                except Exception:
                    pass

                _set_selection_count("eisenhower", "tarefas", total)

            except Exception as e:
                logger.error(f"Erro ao contar seleção do módulo Matriz Eisenhower: {e}", exc_info=True)

        def _count_selected_feynman(feynman_widget):
            try:
                lista = getattr(feynman_widget, "lista_conceitos", None)
                total = len(lista.selectedItems() or []) if lista is not None else 0
                _set_selection_count("feynman", "conceitos", total)

            except Exception as e:
                logger.error(f"Erro ao contar seleção do módulo Feynman: {e}", exc_info=True)

        def _count_selected_mapa(mapa_widget):
            try:
                scene = getattr(mapa_widget, "scene", None)

                if not _is_qt_alive(scene):
                    _set_selection_count("mapa", "nos", 0)
                    return

                from source.modules.mapa.mp_01_NoConceito import NoConceito
                total = 0

                selected_items = scene.selectedItems() or []

                for item in selected_items:
                    if isinstance(item, NoConceito):
                        total += 1

                _set_selection_count("mapa", "nos", total)

            except RuntimeError as e:
                if "already deleted" in str(e):
                    _set_selection_count("mapa", "nos", 0)
                    return

                logger.error(f"Erro ao contar seleção do módulo Mapas Mentais: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro ao contar seleção do módulo Mapas Mentais: {e}", exc_info=True)

        def _registrar_contadores_modulo(module_key: str, widget):
            try:
                if widget is None:
                    return

                module_token = f"{module_key}:{id(widget)}"

                if module_token in self._status_connected_modules:
                    return

                if module_key == "gerenciador":
                    tarefas = getattr(widget, "tarefas", None)

                    if tarefas is not None:
                        for col_name in ("col_todo", "col_doing", "col_done"):
                            col = getattr(tarefas, col_name, None)
                            lst = getattr(col, "lista", None) if col is not None else None

                            if lst is not None:
                                lst.itemSelectionChanged.connect(partial(_count_selected_tempo, widget))

                        _count_selected_tempo(widget)

                elif module_key == "eisenhower":
                    list_names = (
                        "quadrant1_list",
                        "quadrant2_list",
                        "quadrant3_list",
                        "quadrant4_list",
                        "quadrant1_completed_list",
                        "quadrant2_completed_list",
                        "quadrant3_completed_list",
                        "quadrant4_completed_list",
                    )
                    for name in list_names:
                        lst = getattr(widget, name, None)

                        if lst is not None:
                            lst.itemSelectionChanged.connect(partial(_count_selected_eisenhower, widget))

                    try:
                        cp = getattr(widget, "calendar_pane", None)
                        panel = getattr(cp, "calendar_panel", None) if cp is not None else None
                        global_list = getattr(panel, "tasks_list", None) if panel is not None else None

                        if global_list is not None:
                            global_list.itemSelectionChanged.connect(partial(_count_selected_eisenhower, widget))

                    except Exception:
                        pass

                    _count_selected_eisenhower(widget)

                elif module_key == "feynman":
                    lista = getattr(widget, "lista_conceitos", None)

                    if lista is not None:
                        lista.itemSelectionChanged.connect(partial(_count_selected_feynman, widget))

                    _count_selected_feynman(widget)

                elif module_key == "mapa":
                    scene = getattr(widget, "scene", None)

                    if _is_qt_alive(scene):
                        scene.selectionChanged.connect(partial(_count_selected_mapa, widget))

                    _count_selected_mapa(widget)

                self._status_connected_modules.add(module_token)

            except Exception as e:
                logger.error(f"Erro ao registrar contadores de seleção para módulo '{module_key}': {e}", exc_info=True)

        def _registrar_contadores_tabs_carregadas():
            try:
                lazy = getattr(self, "_lazy_tabs", {}) or {}

                for key, info in lazy.items():
                    if not isinstance(info, dict):
                        continue

                    if not info.get("loaded"):
                        continue

                    attr_name = info.get("attr")
                    widget = getattr(self, attr_name, None) if attr_name else None
                    _registrar_contadores_modulo(key, widget)

            except Exception as e:
                logger.error(f"Erro ao registrar contadores das abas carregadas: {e}", exc_info=True)

        self._render_status_bar_content = _render_status
        self._set_selection_count = _set_selection_count
        self._registrar_contadores_modulo = _registrar_contadores_modulo
        self._registrar_contadores_tabs_carregadas = _registrar_contadores_tabs_carregadas

        self.tabs.currentChanged.connect(self.on_tab_changed)
        self._registrar_contadores_tabs_carregadas()
        self._render_status_bar_content()

    except Exception as e:
        logger.critical(f"Erro crítico ao configurar barra de status: {str(e)}", exc_info=True)
        raise
