from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDateEdit, QTimeEdit, QCheckBox, QDialogButtonBox, QApplication
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtCore import Qt, QDate, QTime
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _edit_date_time_dialog(self, item):
    try:
        data = item.data(Qt.UserRole) or {}
        current_date_iso = data.get("date")
        current_time = data.get("time")

        dlg = QDialog(self.app)
        dlg.setWindowTitle(self.get_text("Editar data/horário..."))
        layout = QVBoxLayout(dlg)

        row_date = QHBoxLayout()
        cb_date = QCheckBox(self.get_text("Vincular data"), dlg)
        de = QDateEdit(dlg)
        de.setCalendarPopup(True)
        de.setDisplayFormat(self.app.date_input.displayFormat() if hasattr(self.app, "date_input") else "dd/MM/yyyy")
        de.setDate(QDate.currentDate())
        self._apply_widget_min_height(de, "dialog_date_edit")
        self._apply_locale_to_dateedit(de)

        if current_date_iso:
            qd = QDate.fromString(current_date_iso, Qt.ISODate)
            if qd.isValid():
                cb_date.setChecked(True)
                de.setDate(qd)

            else:
                cb_date.setChecked(False)

        else:
            cb_date.setChecked(False)

        de.setEnabled(cb_date.isChecked())
        cb_date.toggled.connect(de.setEnabled)

        row_date.addWidget(cb_date)
        row_date.addWidget(de)
        layout.addLayout(row_date)

        row_time = QHBoxLayout()
        cb_time = QCheckBox(self.get_text("Vincular horário"), dlg)
        te = QTimeEdit(dlg)
        te.setDisplayFormat("HH:mm")
        te.setTime(QTime.currentTime())
        self._apply_widget_min_height(te, "dialog_time_edit")

        try:
            qt_app = QApplication.instance()
            if qt_app is not None:
                window_color = qt_app.palette().color(QPalette.Window)

                def _is_light_color(col: QColor) -> bool:
                    try:
                        r, g, b = col.red(), col.green(), col.blue()
                        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                        return lum >= 0.85

                    except Exception:
                        return True

                try:
                    fill_color = QColor(window_color)

                except Exception:
                    fill_color = window_color

                pal_te = te.palette()
                pal_te.setColor(QPalette.Base, fill_color)
                pal_te.setColor(QPalette.AlternateBase, fill_color)
                te.setPalette(pal_te)

        except Exception:
            pass

        if current_time:
            qt = QTime.fromString(current_time, "HH:mm")
            if qt.isValid():
                cb_time.setChecked(True)
                te.setTime(qt)

            else:
                cb_time.setChecked(False)

        else:
            cb_time.setChecked(False)

        def _sync_time_enabled():
            te.setEnabled(cb_date.isChecked() and cb_time.isChecked())

        cb_time.toggled.connect(lambda _: _sync_time_enabled())
        cb_date.toggled.connect(lambda _: _sync_time_enabled())
        _sync_time_enabled()

        row_time.addWidget(cb_time)
        row_time.addWidget(te)
        layout.addLayout(row_time)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dlg)

        try:
            ok_btn = buttons.button(QDialogButtonBox.Ok)
            cancel_btn = buttons.button(QDialogButtonBox.Cancel)
            if ok_btn:
                ok_btn.setText(self.get_text("OK"))

            if cancel_btn:
                cancel_btn.setText(self.get_text("Cancelar"))

        except Exception:
            pass

        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        try:
            if hasattr(self.app, "gerenciador_traducao"):
                def _on_idioma_alterado(_=None):
                    dlg.setWindowTitle(self.get_text("Editar data/horário..."))
                    cb_date.setText(self.get_text("Vincular data"))
                    cb_time.setText(self.get_text("Vincular horário"))
                    self._apply_locale_to_dateedit(de)

                    try:
                        ok_btn = buttons.button(QDialogButtonBox.Ok)
                        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
                        if ok_btn:
                            ok_btn.setText(self.get_text("OK"))

                        if cancel_btn:
                            cancel_btn.setText(self.get_text("Cancelar"))

                    except Exception:
                        pass

                self.app.gerenciador_traducao.idioma_alterado.connect(_on_idioma_alterado)

        except Exception:
            pass

        if dlg.exec() != QDialog.Accepted:
            return

        new_date_iso = None
        new_time_str = None

        if cb_date.isChecked():
            new_date_iso = de.date().toString(Qt.ISODate)
            if cb_time.isChecked():
                new_time_str = te.time().toString("HH:mm")

        base_text = self._base_text_from_item(item)
        display_text, tooltip = self._build_display_and_tooltip(base_text, new_date_iso, new_time_str)

        new_data = dict(data) if isinstance(data, dict) else {}
        new_data["text"] = base_text
        new_data["date"] = new_date_iso
        new_data["time"] = new_time_str

        lst = item.listWidget()
        try:
            if isinstance(data, dict) and data.get("category"):
                src_lst, src_item = self._find_source_item_for_calendar(data)
                if src_lst is not None and src_item is not None:
                    lst = src_lst
                    item = src_item

        except Exception:
            pass

        if lst is None:
            return

        row = lst.row(item)
        check_state = item.checkState()

        lst.takeItem(row)
        try:
            if hasattr(self.app, "cleanup_time_groups"):
                self.app.cleanup_time_groups(lst)

        except Exception:
            pass

        from PySide6.QtWidgets import QListWidgetItem
        new_item = QListWidgetItem(display_text)
        new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        new_item.setCheckState(check_state)
        new_item.setData(Qt.UserRole, new_data)

        try:
            tooltip_lines = []
            if tooltip:
                tooltip_lines.append(tooltip)

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

            if tooltip_lines:
                new_item.setToolTip("\n".join(tooltip_lines))

        except Exception:
            try:
                if tooltip:
                    new_item.setToolTip(tooltip)

            except Exception:
                pass

        try:
            if new_data.get("file_path"):
                font = new_item.font() or QFont()
                font.setBold(True)
                new_item.setFont(font)

                try:
                    new_item.setForeground(Qt.blue)

                except Exception:
                    pass

        except Exception:
            pass

        if hasattr(self.app, "insert_task_into_quadrant_list"):
            self.app.insert_task_into_quadrant_list(lst, new_item)

        else:
            lst.addItem(new_item)

        try:
            if hasattr(self.app, "cleanup_time_groups"):
                self.app.cleanup_time_groups(lst)

        except Exception:
            pass

        self.app.save_tasks()
        if hasattr(self.app, "calendar_pane") and self.app.calendar_pane:
            self.app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao editar data/horário via menu: {e}", exc_info=True)
