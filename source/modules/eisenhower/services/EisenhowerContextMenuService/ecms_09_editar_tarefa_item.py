from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from source.modules.eisenhower.services.svc_10_EditTaskDialog import EditTaskDialog
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.modules.tempo.Tarefa import normalizar_prioridade
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def editar_tarefa_item(self, item, list_widget=None):
    try:
        if item is None:
            return

        def _resolve_source():
            try:
                data = item.data(Qt.UserRole) or {}
                if isinstance(data, dict) and data.get("category"):
                    src_list, src_item = self._find_source_item_for_calendar(data)
                    if src_item is not None:
                        return src_list, src_item

            except Exception:
                pass

            lst = list_widget or item.listWidget()
            return lst, item

        src_list, src_item = _resolve_source()
        if src_list is None or src_item is None:
            return

        data = src_item.data(Qt.UserRole) or {}
        initial_text = data.get("text") or self._base_text_from_item(src_item)
        initial_file = data.get("file_path") or ""
        initial_desc = data.get("description") or ""
        initial_date = data.get("date")
        initial_time = data.get("time")

        def _infer_priority(value, src_list_ref):
            try:
                if value is None or value == "":
                    if src_list_ref in (self.app.quadrant1_list, self.app.quadrant1_completed_list):
                        return 1

                    if src_list_ref in (self.app.quadrant2_list, self.app.quadrant2_completed_list):
                        return 2

                    if src_list_ref in (self.app.quadrant3_list, self.app.quadrant3_completed_list):
                        return 3

                    if src_list_ref in (self.app.quadrant4_list, self.app.quadrant4_completed_list):
                        return 4

                    return 1

                if isinstance(value, (int, float)) or (isinstance(value, str) and str(value).isdigit()):
                    pnum = int(value)
                    return pnum if 1 <= pnum <= 4 else 1

                try:
                    pr_norm = normalizar_prioridade(value)

                except Exception:
                    pr_norm = str(value).strip()

                mapping = {
                    "Importante e Urgente": 1,
                    "Importante, mas Não Urgente": 2,
                    "Não Importante, mas Urgente": 3,
                    "Não Importante e Não Urgente": 4,
                }
                return mapping.get(pr_norm, 1)

            except Exception:
                return 1

        initial_priority = _infer_priority(data.get("priority") if data.get("priority") is not None else data.get("prioridade"), src_list)

        dlg = EditTaskDialog(
            self,
            parent=self.app,
            initial_text=initial_text,
            initial_file=initial_file,
            initial_description=initial_desc,
            initial_date=initial_date,
            initial_time=initial_time,
            initial_priority=initial_priority,
        )
        if dlg.exec() != QDialog.Accepted:
            return

        new_text, new_file_path, new_desc, new_date_iso, new_time_str, new_priority = dlg.get_values()
        if not new_text:
            return

        if new_priority is None:
            new_priority = initial_priority

        new_data = dict(data) if isinstance(data, dict) else {}
        new_data["text"] = new_text

        if new_file_path:
            new_data["file_path"] = new_file_path

        else:
            new_data.pop("file_path", None)

        if new_desc:
            new_data["description"] = new_desc

        else:
            new_data.pop("description", None)

        if new_date_iso is not None:
            new_data["date"] = new_date_iso

        else:
            new_data.pop("date", None)

        if new_time_str is not None:
            new_data["time"] = new_time_str

        else:
            new_data.pop("time", None)

        if new_priority is not None:
            new_data["priority"] = int(new_priority)
            prioridade_textos = {
                1: "Importante e Urgente",
                2: "Importante, mas Não Urgente",
                3: "Não Importante, mas Urgente",
                4: "Não Importante e Não Urgente",
            }
            new_data["prioridade"] = prioridade_textos.get(int(new_priority), "Importante e Urgente")

        date_iso = new_data.get("date")
        time_str = new_data.get("time")

        display_text, _dt_tooltip = self._build_display_and_tooltip(new_text, date_iso, time_str)
        tooltip_lines = []

        if _dt_tooltip:
            tooltip_lines.append(_dt_tooltip)

        try:
            fp = new_data.get("file_path")
            if fp:
                tooltip_lines.append((self.get_text("Arquivo") or "Arquivo") + f": {fp}")

        except Exception:
            pass

        try:
            desc_full = new_data.get("description")
            if desc_full:
                preview_lines = [ln for ln in desc_full.splitlines() if ln.strip()]
                preview = "\n".join(preview_lines[:3])
                if preview:
                    tooltip_lines.append((self.get_text("Descrição") or "Descrição") + ":")
                    tooltip_lines.append(preview)

        except Exception:
            pass

        try:
            prio = new_data.get("priority")
            if prio is not None and prio != "":
                try:
                    prio_t = prioridade_para_texto(prio, self.app)

                except Exception:
                    prio_t = str(prio)

                tooltip_lines.append((self.get_text("Prioridade") or "Prioridade") + f": {prio_t}")

        except Exception:
            pass

        tooltip = "\n".join(tooltip_lines) if tooltip_lines else ""

        def _list_has_selectable_items(lst) -> bool:
            try:
                for i in range(lst.count()):
                    it = lst.item(i)
                    if it and (it.flags() & Qt.ItemIsSelectable):
                        return True

                return False

            except Exception:
                return False

        def _ensure_placeholder_for_list(lst):
            try:
                if lst is None:
                    return

                if _list_has_selectable_items(lst):
                    return

                lst.clear()
                if lst in (self.app.quadrant1_list,):
                    self.app.add_placeholder(lst, self.get_text("1º Quadrante"))

                elif lst in (self.app.quadrant2_list,):
                    self.app.add_placeholder(lst, self.get_text("2º Quadrante"))

                elif lst in (self.app.quadrant3_list,):
                    self.app.add_placeholder(lst, self.get_text("3º Quadrante"))

                elif lst in (self.app.quadrant4_list,):
                    self.app.add_placeholder(lst, self.get_text("4º Quadrante"))

                elif lst in (
                    self.app.quadrant1_completed_list,
                    self.app.quadrant2_completed_list,
                    self.app.quadrant3_completed_list,
                    self.app.quadrant4_completed_list,
                ):
                    self.app.add_placeholder(lst, self.get_text("Nenhuma Tarefa Concluída"))

            except Exception:
                pass

        target_list = src_list

        try:
            if isinstance(new_priority, (int, float)):
                prio_idx = int(new_priority) - 1
                keep_completed = self._is_completed_list(src_list)
                target = self._target_list_for_quadrant(prio_idx, keep_completed=keep_completed)
                if target is not None:
                    target_list = target

        except Exception:
            target_list = src_list

        def _build_new_item(check_state):
            from PySide6.QtWidgets import QListWidgetItem
            new_item = QListWidgetItem(display_text)
            new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            new_item.setCheckState(check_state)
            new_item.setData(Qt.UserRole, new_data)

            if tooltip:
                new_item.setToolTip(tooltip)

            try:
                if new_data.get("file_path"):
                    font = new_item.font() or QFont()
                    font.setBold(True)
                    new_item.setFont(font)
                    new_item.setForeground(Qt.blue)

            except Exception:
                pass

            return new_item

        if target_list is not src_list:
            check_state = src_item.checkState()
            row = src_list.row(src_item)

            if row >= 0:
                src_list.takeItem(row)

            try:
                if hasattr(self.app, "cleanup_time_groups"):
                    self.app.cleanup_time_groups(src_list)

            except Exception:
                pass

            _ensure_placeholder_for_list(src_list)
            new_item = _build_new_item(check_state)

            if hasattr(self.app, "insert_task_into_quadrant_list"):
                self.app.insert_task_into_quadrant_list(target_list, new_item)

            else:
                target_list.addItem(new_item)

            try:
                if hasattr(self.app, "cleanup_time_groups"):
                    self.app.cleanup_time_groups(target_list)

            except Exception:
                pass

            try:
                self.app.save_tasks()

            except Exception:
                pass

            try:
                if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
                    self.app.calendar_pane.calendar_panel.update_task_list()

            except Exception:
                pass

            return

        row = src_list.row(src_item)
        check_state = src_item.checkState()
        src_list.takeItem(row)
        new_item = _build_new_item(check_state)

        if hasattr(self.app, "insert_task_into_quadrant_list"):
            self.app.insert_task_into_quadrant_list(src_list, new_item)

        else:
            src_list.addItem(new_item)

        try:
            if hasattr(self.app, "cleanup_time_groups"):
                self.app.cleanup_time_groups(src_list)

        except Exception:
            pass

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
        logger.error(f"Erro ao editar tarefa via menu: {e}", exc_info=True)
