from PySide6.QtWidgets import QMenu, QApplication
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
from source.utils.TaskIdentity import task_identity_signature
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, point, list_widget):
    try:
        item = list_widget.itemAt(point)

        if not item:
            return

        if not bool(item.flags() & Qt.ItemIsSelectable):
            return

        def _selected_items():
            try:
                items = list(list_widget.selectedItems() or [])

            except Exception:
                items = []

            if item not in items:
                items = [item]

            return [it for it in items if it and (it.flags() & Qt.ItemIsSelectable)]

        def _resolve_source(it):
            try:
                data = it.data(Qt.UserRole) or {}

                if isinstance(data, dict) and data.get("category"):
                    src_list, src_item = self._find_source_item_for_calendar(data)

                    if src_list is not None and src_item is not None:
                        return src_list, src_item

            except Exception:
                pass

            return list_widget, it

        def _resolved_selection():
            resolved = []

            for it in _selected_items():
                src_list, src_item = _resolve_source(it)

                if src_list is not None and src_item is not None:
                    resolved.append((src_list, src_item))

            return resolved

        menu = QMenu(list_widget)
        editar_acao = QAction(self.get_text("✏️ Editar Tarefa") or "✏️ Editar Tarefa", self.app)
        editar_acao.triggered.connect(lambda: self.editar_tarefa_item(item, list_widget))
        menu.addAction(editar_acao)

        try:
            compartilhar_acao = QAction(self.get_text("⏱️ Compartilhar com Pomodoro") or "⏱️ Compartilhar com Pomodoro", self.app)

            def _compartilhar():
                try:
                    from uuid import uuid4
                    from source.utils.EventBus import get_event_bus
                    from source.modules.tempo.tmp_01_Tarefa import Tarefa

                    enviados = 0
                    vistos = set()

                    for _, it in _resolved_selection():
                        data = it.data(Qt.UserRole) or {}
                        chave = task_identity_signature(data)

                        if chave in vistos:
                            continue

                        vistos.add(chave)
                        titulo = (data.get("text") or self._base_text_from_item(it) or "").strip()

                        if not titulo:
                            continue

                        pr = data.get("priority") or data.get("prioridade")

                        if isinstance(pr, (int, float)) or (isinstance(pr, str) and str(pr).isdigit()):
                            try:
                                pnum = int(pr)

                            except Exception:
                                pnum = 1

                            mapa = {
                                1: "🔴 Importante e Urgente",
                                2: "🟠 Importante, mas Não Urgente",
                                3: "🟡 Não Importante, mas Urgente",
                                4: "🟢 Não Importante e Não Urgente",
                            }
                            prioridade_raw = mapa.get(pnum, mapa[1])

                        else:
                            prioridade_raw = pr or "Importante e Urgente"

                        prioridade_norm = Tarefa.normalizar_prioridade(prioridade_raw)
                        date_iso = data.get("date")
                        time_str = data.get("time")
                        description = data.get("description") or data.get("desc") or None
                        file_path = data.get("file_path") or None

                        payload = {
                            "integration_id": str(uuid4()),
                            "origin": "eisenhower",
                            "id": data.get("id"),
                            "titulo": titulo,
                            "prioridade": prioridade_norm,
                            "date": date_iso,
                            "time": time_str,
                            "description": description,
                            "file_path": file_path,
                        }

                        try:
                            get_event_bus().send_tarefa(payload)
                            enviados += 1

                        except Exception as e:
                            logger.error(f"Falha ao enviar tarefa ao Gerenciador de Tempo: {e}", exc_info=True)

                    if enviados:
                        try:
                            MessageBox.eisen_share_pomodoro_success(self.app, enviados)

                        except Exception:
                            pass

                except Exception as e:
                    logger.error(f"Erro ao compartilhar tarefa com Pomodoro: {e}", exc_info=True)

            compartilhar_acao.triggered.connect(_compartilhar)
            menu.addAction(compartilhar_acao)

        except Exception:
            pass

        try:
            opts = self._quadrant_options()
            mover_menu = QMenu(self.get_text("🔀 Mover para outro quadrante"), self.app)

            for idx, label in enumerate(opts):
                a = QAction(label, self.app)

                def _make_handler(i):
                    def _handler():
                        try:
                            moved = False

                            for source_list, source_item in _resolved_selection():
                                target = self._target_list_for_quadrant(i, keep_completed=None)

                                if target is None or target is source_list:
                                    continue

                                target_is_completed = self._is_completed_list(target)
                                new_state = Qt.Checked if target_is_completed else Qt.Unchecked
                                source_list.blockSignals(True)
                                target.blockSignals(True)

                                try:
                                    self.app.move_item_between_lists(source_item, source_list, target, new_state)
                                    moved = True

                                finally:
                                    source_list.blockSignals(False)
                                    target.blockSignals(False)

                            if moved:
                                try:
                                    self.app.save_tasks()

                                except Exception:
                                    pass

                                try:
                                    if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
                                        self.app.calendar_pane.calendar_panel.update_task_list()

                                except Exception:
                                    pass

                        except Exception as e:
                            logger.error(f"Erro ao mover tarefa de quadrante via submenu: {e}", exc_info=True)

                    return _handler

                a.triggered.connect(_make_handler(idx))
                mover_menu.addAction(a)

            menu.addMenu(mover_menu)

        except Exception:
            mover_acao = QAction(self.get_text("🔀 Mover para outro quadrante"), self.app)
            mover_acao.triggered.connect(lambda: [self._move_to_quadrant(src_item, src_list) for src_list, src_item in _resolved_selection()])
            menu.addAction(mover_acao)

        menu.addSeparator()
        remover_acao = QAction(self.get_text("🗑️ Remover Tarefa"), self.app)

        def _remover_selecionadas():
            try:
                items = _selected_items()

                if not items:
                    return

                try:
                    if len(items) == 1:
                        ok = MessageBox.eisen_confirm_remove_single_task(self.app, items[0].text())

                    else:
                        ok = MessageBox.eisen_confirm_remove_multiple_tasks(self.app, len(items))

                    if not ok:
                        return

                except Exception:
                    pass

                resolved = _resolved_selection()

                if not resolved:
                    return

                seen = set()
                removed_count = 0

                for src_list, src_item in resolved:
                    try:
                        if src_list is None or src_item is None:
                            continue

                        key = (id(src_list), id(src_item))

                        if key in seen:
                            continue

                        seen.add(key)

                        if self.app.remove_task(src_item, src_list, confirm=False, show_success=False):
                            removed_count += 1

                    except Exception:
                        continue

                if removed_count > 0:
                    try:
                        try:
                            QApplication.beep()

                        except Exception:
                            pass

                        MessageBox.eisen_remove_task_success(self.app)

                    except Exception:
                        pass

            except Exception as e:
                logger.error(f"Erro ao remover tarefas selecionadas: {e}", exc_info=True)

        remover_acao.triggered.connect(_remover_selecionadas)
        menu.addAction(remover_acao)
        menu.exec(list_widget.mapToGlobal(point))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {e}", exc_info=True)
