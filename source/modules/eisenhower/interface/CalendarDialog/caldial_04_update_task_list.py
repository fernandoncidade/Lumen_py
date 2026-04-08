from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QDate, QCoreApplication, QLocale
from PySide6.QtGui import QFont
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.modules.eisenhower.interface.CalendarDialog.caldial_03_collect_tasks import _collect_tasks
from source.modules.eisenhower.interface.CalendarDialog.caldial_05_update_badge_counts import _update_badge_counts
from source.modules.eisenhower.interface.CalendarDialog.caldial_09_apply_highlighted_dates import _apply_highlighted_dates
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def update_task_list(self):
    try:
        self.tasks_list.clear()
        _apply_highlighted_dates(self)
        _update_badge_counts(self)
        
        try:
            if hasattr(self, "get_filter_reference_date"):
                selected_date = self.get_filter_reference_date()

            else:
                selected_date = self.calendar.selectedDate()

        except Exception:
            selected_date = self.calendar.selectedDate()

        filter_mode = self.filter_combo.currentData()
        filtered = []
        tasks_all = _collect_tasks(self)

        try:
            def _emoji_from_priority(prio) -> str:
                try:
                    label = prioridade_para_texto(prio, self)

                    if label:
                        emoji = str(label).strip()[:1]

                        if emoji in {"🔴", "🟠", "🟡", "🟢"}:
                            return emoji

                except Exception:
                    pass

                return ""

            show_priority = True

            try:
                show_priority = bool(getattr(self, "show_priority_checkbox", None) and self.show_priority_checkbox.isChecked())

            except Exception:
                show_priority = True

            tooltip_map = {}
            tasks_by_date_data = {}
            month_tooltip_map = {}

            for task in tasks_all:
                ds = task.get("date")

                if not ds:
                    continue

                text = (task.get("text") or "").strip()

                if not text:
                    continue

                time_str = task.get("time") or ""
                emoji = _emoji_from_priority(task.get("priority")) if show_priority else ""
                status_text = get_text("Concluída") if task.get("completed") else get_text("Pendente")

                if time_str:
                    line = f"{emoji} {time_str} — {text} ({status_text})".strip()

                else:
                    line = f"{emoji} {text} ({status_text})".strip()

                tooltip_map.setdefault(ds, []).append(line)
                tasks_by_date_data.setdefault(ds, []).append(task)

                try:
                    qd = QDate.fromString(ds, Qt.ISODate)

                    if qd.isValid():
                        month_key = (qd.year(), qd.month())
                        date_for_month = qd.toString(self._date_format)

                        if time_str:
                            month_line = f"{emoji} {date_for_month} {time_str} — {text} ({status_text})".strip()

                        else:
                            month_line = f"{emoji} {date_for_month} — {text} ({status_text})".strip()

                        month_tooltip_map.setdefault(month_key, []).append(month_line)

                except Exception:
                    pass

            for ds, lines in tooltip_map.items():
                lines.sort()

            for month_key, lines in month_tooltip_map.items():
                lines.sort()

            if hasattr(self, "calendar") and hasattr(self.calendar, "set_task_tooltip_map"):
                self.calendar.set_task_tooltip_map(tooltip_map)

                if hasattr(self.calendar, "set_tasks_by_date_data"):
                    self.calendar.set_tasks_by_date_data(tasks_by_date_data)

            try:
                should_set_year_tooltip = False

                if hasattr(self, "year_calendar") and hasattr(self.year_calendar, "set_month_tooltip_map"):
                    view_mode = ""

                    try:
                        if hasattr(self, "calendar_view_mode"):
                            view_mode = self.calendar_view_mode() or ""

                        else:
                            view_mode = getattr(self, "_calendar_view_mode", "") or ""

                    except Exception:
                        view_mode = ""

                    should_set_year_tooltip = filter_mode in {"month", "year"} and str(view_mode) == "year"

                    if should_set_year_tooltip:
                        self.year_calendar.set_month_tooltip_map(month_tooltip_map)

                    else:
                        self.year_calendar.set_month_tooltip_map({})

            except Exception as e:
                logger.error(f"Erro ao atualizar tooltip mensal do calendário anual: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao atualizar tooltip do calendário: {e}", exc_info=True)

        for task in tasks_all:
            date_str = task.get("date")

            if not date_str:
                continue

            qdate = QDate.fromString(date_str, Qt.ISODate)

            if not qdate.isValid():
                continue

            if filter_mode == "day" and qdate != selected_date:
                continue

            if filter_mode == "week":
                selected_start_of_week = selected_date.addDays(-(selected_date.dayOfWeek() % 7))
                task_start_of_week = qdate.addDays(-(qdate.dayOfWeek() % 7))

                if selected_start_of_week != task_start_of_week:
                    continue

            if filter_mode == "month":
                if qdate.month() != selected_date.month() or qdate.year() != selected_date.year():
                    continue

            if filter_mode == "year" and qdate.year() != selected_date.year():
                continue

            filtered.append((qdate, task))

        if not filtered:
            placeholder = QListWidgetItem(get_text("Nenhuma tarefa para o período selecionado."))
            placeholder.setFlags((placeholder.flags() & ~Qt.ItemIsSelectable) & ~Qt.ItemIsEnabled)
            self.tasks_list.addItem(placeholder)
            return

        filtered.sort(key=lambda entry: (entry[0], entry[1]["time"] or "", entry[1]["text"].lower()))
        should_insert_month_headers = filter_mode in {"month", "year"}
        last_month_key = None

        try:
            if hasattr(self, "calendar") and hasattr(self.calendar, "locale"):
                list_locale = self.calendar.locale()

            else:
                list_locale = QLocale.system()

        except Exception:
            list_locale = QLocale.system()

        for qdate, task in filtered:
            if should_insert_month_headers:
                month_key = (qdate.year(), qdate.month())

                if month_key != last_month_key:
                    month_name = list_locale.standaloneMonthName(qdate.month(), QLocale.LongFormat) or list_locale.monthName(qdate.month(), QLocale.LongFormat)

                    if not month_name:
                        month_name = qdate.toString("MMMM")

                    header_item = QListWidgetItem(f"{month_name.capitalize()} {qdate.year()}")
                    header_item.setFlags((header_item.flags() & ~Qt.ItemIsSelectable) & ~Qt.ItemIsEnabled)
                    header_font = header_item.font() or QFont()
                    header_font.setBold(True)
                    header_item.setFont(header_font)
                    self.tasks_list.addItem(header_item)
                    last_month_key = month_key

            status_text = get_text("Concluída") if task.get("completed") else get_text("Pendente")
            date_str = qdate.toString(self._date_format)
            time_str = task.get("time")

            if time_str:
                dt_str = f"{date_str} {time_str}"

            else:
                dt_str = date_str

            emoji = ""

            try:
                if show_priority:
                    emoji = _emoji_from_priority(task.get("priority"))

            except Exception:
                emoji = ""

            item_text = f"{emoji} {dt_str} — {task['text']} — [{status_text}]".strip()
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            try:
                item.setData(Qt.UserRole, task)

            except Exception:
                pass

            try:
                fp = task.get("file_path")
                if fp:
                    font = item.font() or QFont()
                    font.setBold(True)
                    item.setFont(font)

                    try:
                        item.setForeground(Qt.blue)

                    except Exception:
                        pass

            except Exception:
                pass

            try:
                tooltip_lines = []
                fp = task.get("file_path")

                if fp:
                    tooltip_lines.append(f"{get_text('Arquivo') or 'Arquivo'}: {fp}")

                if date_str:
                    tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_str}")

                if time_str:
                    tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

                desc = task.get("description")

                if desc:
                    tooltip_lines.append(f"{get_text('Descrição') or 'Descrição'}: {desc}")

                prio = task.get("priority")

                if prio is not None and prio != "":
                    try:
                        prio_t = prioridade_para_texto(prio, self)

                    except Exception:
                        prio_t = str(prio)

                    tooltip_lines.append(f"{get_text('Prioridade') or 'Prioridade'}: {prio_t}")

                if tooltip_lines:
                    try:
                        item.setToolTip("\n".join(tooltip_lines))

                    except Exception:
                        pass

            except Exception:
                pass

            self.tasks_list.addItem(item)

    except Exception as e:
        logger.error(f"Erro ao atualizar lista de tarefas do calendário: {e}", exc_info=True)
