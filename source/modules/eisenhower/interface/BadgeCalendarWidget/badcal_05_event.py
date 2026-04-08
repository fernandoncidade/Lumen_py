from PySide6.QtWidgets import QToolTip, QMenu, QCalendarWidget
from PySide6.QtCore import Qt, QCoreApplication, QEvent
from PySide6.QtGui import QAction
from source.modules.eisenhower.services.svc_06_EisenhowerContextMenuService import editar_tarefa_por_dados, remover_tarefa_por_dados, remover_todas_por_data
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def event(self, event):
    try:
        if event.type() == QEvent.ToolTip:
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            qd = self._date_at_pos(pos)
            if qd and qd.isValid():
                ds = qd.toString(Qt.ISODate)
                lines = self._tasks_by_date.get(ds) or []
                if lines:
                    QToolTip.showText(event.globalPos(), "\n".join(lines), self)
                    return True

            QToolTip.hideText()
            event.ignore()
            return True

        if event.type() == QEvent.ContextMenu:
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            qd = self._date_at_pos(pos)
            if qd and qd.isValid():
                date_iso = qd.toString(Qt.ISODate)
                tasks = list(self._tasks_by_date_data.get(date_iso) or [])
                tasks.sort(key=lambda t: (t.get("time") or "", (t.get("text") or "").lower()))

                show_priority = True
                try:
                    owner = getattr(self, "owner", None)
                    if owner is not None and hasattr(owner, "show_priority_checkbox"):
                        show_priority = bool(owner.show_priority_checkbox.isChecked())

                except Exception:
                    show_priority = True

                menu = QMenu(self)
                edit_menu = menu.addMenu(get_text("✏️ Editar Tarefa") or "✏️ Editar Tarefa")
                remove_menu = menu.addMenu(get_text("🗑️ Remover Tarefa") or "🗑️ Remover Tarefa")

                if tasks:
                    for task in tasks:
                        label = (task.get("text") or "").strip() or get_text("(Sem título)")
                        time_str = task.get("time") or ""
                        emoji = ""
                        if show_priority:
                            try:
                                prio_label = prioridade_para_texto(task.get("priority"), getattr(self, "owner", None))
                                if prio_label:
                                    cand = str(prio_label).strip()[:1]
                                    if cand in {"🔴", "🟠", "🟡", "🟢"}:
                                        emoji = cand

                            except Exception:
                                emoji = ""

                        if time_str:
                            label = f"{time_str} — {label}"

                        if emoji:
                            label = f"{emoji} {label}"

                        act_edit = QAction(label, self)
                        act_edit.triggered.connect(lambda _=False, t=task: editar_tarefa_por_dados(getattr(self, "app", None), t))
                        edit_menu.addAction(act_edit)

                        act_remove = QAction(label, self)
                        act_remove.triggered.connect(lambda _=False, t=task: remover_tarefa_por_dados(getattr(self, "app", None), t, True))
                        remove_menu.addAction(act_remove)

                    remove_menu.addSeparator()
                    act_remove_all = QAction(get_text("Remover Todas") or "Remover Todas", self)
                    act_remove_all.triggered.connect(lambda _=False, ds=date_iso: remover_todas_por_data(getattr(self, "app", None), ds))
                    remove_menu.addAction(act_remove_all)

                else:
                    act_empty_edit = QAction(get_text("Nenhuma tarefa neste dia."), self)
                    act_empty_edit.setEnabled(False)
                    edit_menu.addAction(act_empty_edit)

                    act_empty_remove = QAction(get_text("Nenhuma tarefa neste dia."), self)
                    act_empty_remove.setEnabled(False)
                    remove_menu.addAction(act_empty_remove)

                global_pos = event.globalPos() if hasattr(event, "globalPos") else self.mapToGlobal(pos)
                menu.exec(global_pos)
                return True

    except Exception as e:
        logger.error(f"Erro ao exibir tooltip no calendário: {e}", exc_info=True)

    return QCalendarWidget.event(self, event)
