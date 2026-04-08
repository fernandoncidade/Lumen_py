from PySide6.QtWidgets import (QMenu, QInputDialog, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QDateEdit, 
                               QTimeEdit, QCheckBox, QDialogButtonBox, QCalendarWidget, QApplication, QFileDialog, QLineEdit, QMessageBox)
from PySide6.QtGui import QAction, QColor, QPalette, QFont, QDesktopServices
from PySide6.QtCore import QCoreApplication, Qt, QDate, QTime, QLocale, QUrl
from source.modules.eisenhower.services.svc_01_initUI import FileDropLineEdit
from source.modules.eisenhower.services.svc_09_prioridade_display import prioridade_para_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def _compute_widget_height(app, widget, name: str | None = None) -> int:
    try:
        if hasattr(app, "widget_heights") and isinstance(app.widget_heights, dict) and name in app.widget_heights:
            v = int(app.widget_heights.get(name) or 0)
            if v > 0:
                return v

        if hasattr(app, "widget_height_override") and isinstance(app.widget_height_override, int) and app.widget_height_override > 0:
            return int(app.widget_height_override)

        fm = widget.fontMetrics()
        return max(26, int(fm.height() * 1.2))

    except Exception:
        return 28

def _apply_widget_min_height(app, widget, name: str | None = None):
    try:
        h = _compute_widget_height(app, widget, name)
        widget.setMinimumHeight(h)

    except Exception:
        pass

def _effective_locale(app) -> QLocale:
    try:
        if hasattr(app, "date_input") and app.date_input is not None:
            return app.date_input.locale()

    except Exception:
        pass

    try:
        if hasattr(app, "gerenciador_traducao"):
            idioma = app.gerenciador_traducao.obter_idioma_atual()
            if idioma and idioma.startswith("pt"):
                return QLocale(QLocale.Portuguese, QLocale.Brazil)

            if idioma and idioma.startswith("en"):
                return QLocale(QLocale.English, QLocale.UnitedStates)

    except Exception:
        pass

    return QLocale.system()

def _apply_locale_to_dateedit(app, de: QDateEdit):
    try:
        loc = _effective_locale(app)
        de.setLocale(loc)

        cw = de.calendarWidget()
        if cw is None:
            cw = QCalendarWidget(de)
            de.setCalendarWidget(cw)

        cw.setLocale(loc)

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

                if True:
                    fill_color = QColor(window_color)

                pal = de.palette()
                pal.setColor(QPalette.Base, fill_color)
                pal.setColor(QPalette.AlternateBase, fill_color)
                de.setPalette(pal)

                try:
                    cw_pal = cw.palette()
                    cw_pal.setColor(QPalette.Base, fill_color)
                    cw_pal.setColor(QPalette.AlternateBase, fill_color)
                    cw.setPalette(cw_pal)

                except Exception:
                    pass

        except Exception:
            pass

        cw.update()
        de.update()

    except Exception as e:
        logger.debug(f"Falha ao aplicar locale no calendário do QDateEdit: {e}", exc_info=True)

def _is_completed_list(app, lst) -> bool:
    return lst in (
        app.quadrant1_completed_list,
        app.quadrant2_completed_list,
        app.quadrant3_completed_list,
        app.quadrant4_completed_list,
    )

def _quadrant_options(app):
    return [
        app.quadrant1_label.text(),
        app.quadrant2_label.text(),
        app.quadrant3_label.text(),
        app.quadrant4_label.text(),
    ]

def _target_list_for_quadrant(app, quadrant_index: int, keep_completed: bool):
    pending = [app.quadrant1_list, app.quadrant2_list, app.quadrant3_list, app.quadrant4_list]
    done = [app.quadrant1_completed_list, app.quadrant2_completed_list, app.quadrant3_completed_list, app.quadrant4_completed_list]
    if 0 <= quadrant_index < 4:
        return done[quadrant_index] if keep_completed else pending[quadrant_index]

    return None

def _find_source_item_for_calendar(app, task_dict):
    try:
        if not isinstance(task_dict, dict):
            return None, None

        cat = task_dict.get("category")
        if not cat:
            return None, None

        completed = bool(task_dict.get("completed"))
        labels = [
            getattr(app, "quadrant1_label", None).text() if getattr(app, "quadrant1_label", None) is not None else None,
            getattr(app, "quadrant2_label", None).text() if getattr(app, "quadrant2_label", None) is not None else None,
            getattr(app, "quadrant3_label", None).text() if getattr(app, "quadrant3_label", None) is not None else None,
            getattr(app, "quadrant4_label", None).text() if getattr(app, "quadrant4_label", None) is not None else None,
        ]
        pending = [getattr(app, "quadrant1_list", None), getattr(app, "quadrant2_list", None), getattr(app, "quadrant3_list", None), getattr(app, "quadrant4_list", None)]
        done = [getattr(app, "quadrant1_completed_list", None), getattr(app, "quadrant2_completed_list", None), getattr(app, "quadrant3_completed_list", None), getattr(app, "quadrant4_completed_list", None)]

        for idx, label in enumerate(labels):
            try:
                if not label:
                    continue

                if not str(cat).startswith(label):
                    continue

                src_list = done[idx] if completed else pending[idx]
                if src_list is None:
                    continue

                for i in range(src_list.count()):
                    it = src_list.item(i)
                    if not it:
                        continue

                    if not (it.flags() & Qt.ItemIsSelectable):
                        continue

                    d = it.data(Qt.UserRole) or {}
                    if (str(d.get("text") or "").strip() == str(task_dict.get("text") or "").strip()) and (d.get("date") or "") == (task_dict.get("date") or "") and (d.get("time") or "") == (task_dict.get("time") or ""):
                        return src_list, it

            except Exception:
                continue

    except Exception:
        pass

    return None, None

def editar_tarefa_item(app, item, list_widget=None):
    try:
        if item is None:
            return

        def _resolve_source():
            try:
                data = item.data(Qt.UserRole) or {}
                if isinstance(data, dict) and data.get("category"):
                    src_list, src_item = _find_source_item_for_calendar(app, data)
                    if src_item is not None:
                        return src_list, src_item

            except Exception:
                pass

            lst = list_widget or item.listWidget()
            return lst, item

        src_list, src_item = _resolve_source()
        if src_list is None or src_item is None:
            return

        class EditTaskDialog(QDialog):
            def __init__(self, parent=None, initial_text="", initial_file="", initial_description="", initial_date=None, initial_time=None):
                super().__init__(parent or app)
                self.setModal(True)
                self.setWindowTitle(get_text("Editar Tarefa") or "Editar Tarefa")
                layout = QVBoxLayout(self)

                layout.addWidget(QLabel(get_text("Tarefa:")))
                self.title = QLineEdit(self)
                self.title.setText(initial_text or "")
                layout.addWidget(self.title)

                layout.addWidget(QLabel(get_text("Arquivo vinculado (arraste ou escolha):")))
                hl = QHBoxLayout()
                self.file_field = FileDropLineEdit(app, self)
                self.file_field.setText(initial_file and (initial_file.split("\\")[-1] or initial_file) or "")
                self.file_field.setToolTip(initial_file or "")
                hl.addWidget(self.file_field)
                btn_choose = QPushButton(get_text("Escolher..."))

                def _choose():
                    try:
                        path, _ = QFileDialog.getOpenFileName(self, get_text("Escolher arquivo"), "", "*")
                        if path:
                            self.file_field.setText(path.split("\\")[-1])
                            self.file_field.setToolTip(path)

                    except Exception:
                        pass

                btn_choose.clicked.connect(_choose)
                btn_clear = QPushButton(get_text("Remover"))

                def _clear():
                    try:
                        self.file_field.clear()
                        self.file_field.setToolTip("")

                    except Exception:
                        pass

                btn_clear.clicked.connect(_clear)
                btn_open = QPushButton(get_text("Abrir") or "Abrir")

                def _open_file():
                    fp = self.file_field.toolTip() or None
                    if not fp:
                        return

                    try:
                        QDesktopServices.openUrl(QUrl.fromLocalFile(fp))

                    except Exception:
                        try:
                            import os, subprocess, sys
                            if sys.platform.startswith("win"):
                                os.startfile(fp)

                            elif sys.platform.startswith("darwin"):
                                subprocess.Popen(["open", fp])

                            else:
                                subprocess.Popen(["xdg-open", fp])

                        except Exception:
                            pass

                btn_open.clicked.connect(_open_file)
                hl.addWidget(btn_choose)
                hl.addWidget(btn_clear)
                hl.addWidget(btn_open)
                layout.addLayout(hl)

                layout.addWidget(QLabel(get_text("Descrição (opcional):")))
                self.desc = QTextEdit(self)
                self.desc.setPlainText(initial_description or "")
                self.desc.setMinimumHeight(120)
                layout.addWidget(self.desc)

                row_date = QHBoxLayout()
                self.cb_date = QCheckBox(get_text("Vincular data"), self)
                self.de = QDateEdit(self)
                self.de.setCalendarPopup(True)
                self.de.setDisplayFormat(app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy")
                self.de.setDate(QDate.currentDate())
                _apply_widget_min_height(app, self.de, "dialog_date_edit")
                _apply_locale_to_dateedit(app, self.de)

                try:
                    self.cb_date.setChecked(True)

                except Exception:
                    pass

                row_date.addWidget(self.cb_date)
                row_date.addWidget(self.de)
                layout.addLayout(row_date)

                row_time = QHBoxLayout()
                self.cb_time = QCheckBox(get_text("Vincular horário"), self)
                self.te = QTimeEdit(self)
                self.te.setDisplayFormat("HH:mm")
                self.te.setTime(QTime.currentTime())
                _apply_widget_min_height(app, self.te, "dialog_time_edit")

                try:
                    self.cb_time.setChecked(True)

                except Exception:
                    pass

                row_time.addWidget(self.cb_time)
                row_time.addWidget(self.te)
                layout.addLayout(row_time)

                if initial_date:
                    try:
                        qd = QDate.fromString(initial_date, Qt.ISODate)
                        if qd.isValid():
                            self.cb_date.setChecked(True)
                            self.de.setDate(qd)

                    except Exception:
                        pass

                if initial_time:
                    try:
                        qt = QTime.fromString(initial_time, "HH:mm")
                        if qt.isValid():
                            self.cb_time.setChecked(True)
                            self.te.setTime(qt)

                    except Exception:
                        pass

                def _sync_time_enabled():
                    self.de.setEnabled(self.cb_date.isChecked())
                    self.te.setEnabled(self.cb_date.isChecked() and self.cb_time.isChecked())

                self.cb_date.toggled.connect(lambda _: _sync_time_enabled())
                self.cb_time.toggled.connect(lambda _: _sync_time_enabled())
                _sync_time_enabled()

                btns = QHBoxLayout()
                btns.addStretch(1)
                btn_cancel = QPushButton(get_text("Cancelar") or "Cancelar")
                btn_ok = QPushButton(get_text("OK") or "OK")
                btn_cancel.clicked.connect(self.reject)
                btn_ok.clicked.connect(self.accept)
                btns.addWidget(btn_cancel)
                btns.addWidget(btn_ok)
                layout.addLayout(btns)

            def get_values(self):
                fp = self.file_field.toolTip() or None
                new_date_iso = None
                new_time_str = None
                if self.cb_date.isChecked():
                    new_date_iso = self.de.date().toString(Qt.ISODate)
                    if self.cb_time.isChecked():
                        new_time_str = self.te.time().toString("HH:mm")

                return self.title.text().strip(), fp, self.desc.toPlainText().strip(), new_date_iso, new_time_str

        data = src_item.data(Qt.UserRole) or {}
        initial_text = data.get("text") or _base_text_from_item(src_item)
        initial_file = data.get("file_path") or ""
        initial_desc = data.get("description") or ""
        initial_date = data.get("date")
        initial_time = data.get("time")

        dlg = EditTaskDialog(parent=app, initial_text=initial_text, initial_file=initial_file, initial_description=initial_desc, initial_date=initial_date, initial_time=initial_time)
        if dlg.exec() != QDialog.Accepted:
            return

        new_text, new_file_path, new_desc, new_date_iso, new_time_str = dlg.get_values()
        if not new_text:
            return

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

        date_iso = new_data.get("date")
        time_str = new_data.get("time")

        display_text, _dt_tooltip = _build_display_and_tooltip(app, new_text, date_iso, time_str)
        tooltip_lines = []
        if _dt_tooltip:
            tooltip_lines.append(_dt_tooltip)

        try:
            fp = new_data.get("file_path")
            if fp:
                tooltip_lines.append((get_text("Arquivo") or "Arquivo") + f": {fp}")

        except Exception:
            pass

        try:
            desc_full = new_data.get("description")
            if desc_full:
                preview_lines = [ln for ln in desc_full.splitlines() if ln.strip()]
                preview = "\n".join(preview_lines[:3])
                if preview:
                    tooltip_lines.append((get_text("Descrição") or "Descrição") + ":")
                    tooltip_lines.append(preview)

        except Exception:
            pass

        tooltip = "\n".join(tooltip_lines) if tooltip_lines else ""

        row = src_list.row(src_item)
        check_state = src_item.checkState()
        src_list.takeItem(row)

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

        if hasattr(app, "insert_task_into_quadrant_list"):
            app.insert_task_into_quadrant_list(src_list, new_item)

        else:
            src_list.addItem(new_item)

        try:
            if hasattr(app, "cleanup_time_groups"):
                app.cleanup_time_groups(src_list)

        except Exception:
            pass

        try:
            app.save_tasks()

        except Exception:
            pass

        try:
            if hasattr(app, "calendar_pane") and app.calendar_pane:
                app.calendar_pane.calendar_panel.update_task_list()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao editar tarefa via menu: {e}", exc_info=True)

def editar_tarefa_por_dados(app, task_data: dict):
    try:
        if not isinstance(task_data, dict):
            return

        src_list, src_item = _find_source_item_for_calendar(app, task_data)
        if src_item is None:
            return

        editar_tarefa_item(app, src_item, src_list)

    except Exception as e:
        logger.error(f"Erro ao editar tarefa via dados: {e}", exc_info=True)

def remover_tarefa_item(app, item, list_widget=None, confirm: bool = True) -> bool:
    try:
        if item is None:
            return False

        lst = list_widget or item.listWidget()
        if lst is None:
            return False

        data = item.data(Qt.UserRole) or {}
        if isinstance(data, dict) and data.get("category"):
            src_list, src_item = _find_source_item_for_calendar(app, data)
            if src_list is not None and src_item is not None:
                removed = app.remove_task(src_item, src_list, confirm)
            else:
                removed = app.remove_task(item, lst, confirm)

        else:
            removed = app.remove_task(item, lst, confirm)

        if removed:
            try:
                app.save_tasks()

            except Exception:
                pass

            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception:
                pass

        return bool(removed)

    except Exception as e:
        logger.error(f"Erro ao remover tarefa via menu: {e}", exc_info=True)
        return False

def remover_tarefa_por_dados(app, task_data: dict, confirm: bool = True) -> bool:
    try:
        if not isinstance(task_data, dict):
            return False

        src_list, src_item = _find_source_item_for_calendar(app, task_data)
        if src_item is None or src_list is None:
            return False

        return remover_tarefa_item(app, src_item, src_list, confirm)

    except Exception as e:
        logger.error(f"Erro ao remover tarefa via dados: {e}", exc_info=True)
        return False

def remover_todas_por_data(app, date_iso: str) -> int:
    try:
        if not date_iso:
            return 0

        try:
            resp = QMessageBox.question(
                app,
                get_text("Remover Tarefas") or "Remover Tarefas",
                get_text("Deseja remover todas as tarefas do dia selecionado?") or "Deseja remover todas as tarefas do dia selecionado?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if resp != QMessageBox.Yes:
                return 0

        except Exception:
            pass

        removed = 0
        lists = [
            getattr(app, "quadrant1_list", None),
            getattr(app, "quadrant2_list", None),
            getattr(app, "quadrant3_list", None),
            getattr(app, "quadrant4_list", None),
            getattr(app, "quadrant1_completed_list", None),
            getattr(app, "quadrant2_completed_list", None),
            getattr(app, "quadrant3_completed_list", None),
            getattr(app, "quadrant4_completed_list", None),
        ]

        for lst in lists:
            if lst is None:
                continue

            for i in range(lst.count() - 1, -1, -1):
                it = lst.item(i)
                if not it or not (it.flags() & Qt.ItemIsSelectable):
                    continue

                data = it.data(Qt.UserRole) or {}
                if (data.get("date") or "") == date_iso:
                    try:
                        lst.takeItem(i)
                        removed += 1

                    except Exception:
                        pass

        try:
            if hasattr(app, "cleanup_time_groups"):
                for lst in lists:
                    if lst is not None:
                        app.cleanup_time_groups(lst)

        except Exception:
            pass

        try:
            if hasattr(app, "atualizar_placeholders"):
                app.atualizar_placeholders()

        except Exception:
            pass

        try:
            app.save_tasks()

        except Exception:
            pass

        try:
            if hasattr(app, "calendar_pane") and app.calendar_pane:
                app.calendar_pane.calendar_panel.update_task_list()

        except Exception:
            pass

        return removed

    except Exception as e:
        logger.error(f"Erro ao remover todas as tarefas por data: {e}", exc_info=True)
        return 0

def _base_text_from_item(item) -> str:
    data = item.data(Qt.UserRole) or {}
    base = (data.get("text") or "").strip()
    if base:
        return base

    txt = (item.text() or "").strip()
    if " — " in txt:
        return txt.split(" — ", 1)[0].strip()

    return txt

def _build_display_and_tooltip(app, base_text: str, date_iso: str | None, time_str: str | None):
    display_text = base_text
    tooltip_lines = []

    if date_iso:
        qd = QDate.fromString(date_iso, Qt.ISODate)
        if qd.isValid():
            date_human = qd.toString(app.date_input.displayFormat())
            if time_str:
                display_text = f"{base_text} — {date_human} {time_str}"

            else:
                display_text = f"{base_text} — {date_human}"

            tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

    if time_str:
        tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

    return display_text, ("\n".join(tooltip_lines) if tooltip_lines else "")

def _edit_date_time_dialog(app, item):
    try:
        data = item.data(Qt.UserRole) or {}
        current_date_iso = data.get("date")
        current_time = data.get("time")

        dlg = QDialog(app)
        dlg.setWindowTitle(get_text("Editar data/horário..."))
        layout = QVBoxLayout(dlg)

        row_date = QHBoxLayout()
        cb_date = QCheckBox(get_text("Vincular data"), dlg)
        de = QDateEdit(dlg)
        de.setCalendarPopup(True)
        de.setDisplayFormat(app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy")
        de.setDate(QDate.currentDate())
        _apply_widget_min_height(app, de, "dialog_date_edit")
        _apply_locale_to_dateedit(app, de)

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
        cb_time = QCheckBox(get_text("Vincular horário"), dlg)
        te = QTimeEdit(dlg)
        te.setDisplayFormat("HH:mm")
        te.setTime(QTime.currentTime())
        _apply_widget_min_height(app, te, "dialog_time_edit")

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
                ok_btn.setText(get_text("OK"))

            if cancel_btn:
                cancel_btn.setText(get_text("Cancelar"))

        except Exception:
            pass

        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        try:
            if hasattr(app, "gerenciador_traducao"):
                def _on_idioma_alterado(_=None):
                    dlg.setWindowTitle(get_text("Editar data/horário..."))
                    cb_date.setText(get_text("Vincular data"))
                    cb_time.setText(get_text("Vincular horário"))
                    _apply_locale_to_dateedit(app, de)

                    try:
                        ok_btn = buttons.button(QDialogButtonBox.Ok)
                        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
                        if ok_btn:
                            ok_btn.setText(get_text("OK"))

                        if cancel_btn:
                            cancel_btn.setText(get_text("Cancelar"))

                    except Exception:
                        pass

                app.gerenciador_traducao.idioma_alterado.connect(_on_idioma_alterado)

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

        base_text = _base_text_from_item(item)
        display_text, tooltip = _build_display_and_tooltip(app, base_text, new_date_iso, new_time_str)

        new_data = dict(data) if isinstance(data, dict) else {}
        new_data["text"] = base_text
        new_data["date"] = new_date_iso
        new_data["time"] = new_time_str

        lst = item.listWidget()
        try:
            if isinstance(data, dict) and data.get("category"):
                src_lst, src_item = _find_source_item_for_calendar(app, data)
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
            if hasattr(app, "cleanup_time_groups"):
                app.cleanup_time_groups(lst)

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
                    tooltip_lines.append((get_text("Arquivo") or "Arquivo") + f": {fp}")

            except Exception:
                pass

            try:
                desc_full = new_data.get("description")
                if desc_full:
                    preview_lines = [ln for ln in desc_full.splitlines() if ln.strip()]
                    preview = "\n".join(preview_lines[:3])
                    if preview:
                        tooltip_lines.append((get_text("Descrição") or "Descrição") + ":")
                        tooltip_lines.append(preview)

            except Exception:
                pass

            try:
                prio = new_data.get("priority")
                if prio is not None and prio != "":
                    try:
                        prio_t = prioridade_para_texto(prio, app)

                    except Exception:
                        prio_t = str(prio)

                    tooltip_lines.append((get_text("Prioridade") or "Prioridade") + f": {prio_t}")

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

        if hasattr(app, "insert_task_into_quadrant_list"):
            app.insert_task_into_quadrant_list(lst, new_item)

        else:
            lst.addItem(new_item)

        try:
            if hasattr(app, "cleanup_time_groups"):
                app.cleanup_time_groups(lst)

        except Exception:
            pass

        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao editar data/horário via menu: {e}", exc_info=True)

def _move_to_quadrant(app, item, source_list):
    try:
        opts = _quadrant_options(app)
        chosen, ok = QInputDialog.getItem(
            app,
            get_text("Mover tarefa"),
            get_text("Selecione o quadrante:"),
            opts,
            0,
            False
        )
        if not ok or not chosen:
            return

        try:
            idx = opts.index(chosen)

        except ValueError:
            return

        keep_completed = _is_completed_list(app, source_list)
        target = _target_list_for_quadrant(app, idx, keep_completed=keep_completed)
        if target is None or target is source_list:
            return

        new_state = Qt.Checked if keep_completed else Qt.Unchecked

        source_list.blockSignals(True)
        target.blockSignals(True)

        try:
            app.move_item_between_lists(item, source_list, target, new_state)

        finally:
            source_list.blockSignals(False)
            target.blockSignals(False)

        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao mover tarefa de quadrante via menu: {e}", exc_info=True)

def mostrar_menu_contexto(app, point, list_widget):
    try:
        item = list_widget.itemAt(point)
        if not item:
            return

        if not bool(item.flags() & Qt.ItemIsSelectable):
            return

        menu = QMenu(list_widget)

        editar_acao = QAction(get_text("✏️ Editar Tarefa...") or "✏️ Editar Tarefa...", app)
        editar_acao.triggered.connect(lambda: editar_tarefa_item(app, item, list_widget))
        menu.addAction(editar_acao)

        try:
            compartilhar_acao = QAction(get_text("⏱️ Compartilhar com Pomodoro...") or "⏱️ Compartilhar com Pomodoro...", app)

            def _compartilhar():
                try:
                    from uuid import uuid4
                    from source.utils.EventBus import get_event_bus
                    from source.modules.tempo.tmp_01_Tarefa import Tarefa

                    data = item.data(Qt.UserRole) or {}
                    titulo = (data.get("text") or _base_text_from_item(item) or "").strip()
                    if not titulo:
                        return

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
                        "titulo": titulo,
                        "prioridade": prioridade_norm,
                        "date": date_iso,
                        "time": time_str,
                        "description": description,
                        "file_path": file_path,
                    }

                    try:
                        get_event_bus().send_tarefa(payload)
                        try:
                            QMessageBox.information(app, get_text("Sucesso") or "Sucesso", get_text("Tarefa enviada com sucesso para ⏱️ Gestão de Tempo - Pomodoro!⏱️"))

                        except Exception:
                            pass

                    except Exception as e:
                        logger.debug(f"Falha ao enviar tarefa ao Gerenciador de Tempo: {e}", exc_info=True)

                except Exception as e:
                    logger.error(f"Erro ao compartilhar tarefa com Pomodoro: {e}", exc_info=True)

            compartilhar_acao.triggered.connect(_compartilhar)
            menu.addAction(compartilhar_acao)

        except Exception:
            pass

        try:
            opts = _quadrant_options(app)
            mover_menu = QMenu(get_text("🔀 Mover para outro quadrante"), app)

            try:
                data_for_resolution = item.data(Qt.UserRole) or {}
                src_list_for_move, src_item_for_move = (None, None)
                if isinstance(data_for_resolution, dict) and data_for_resolution.get("category"):
                    src_list_for_move, src_item_for_move = _find_source_item_for_calendar(app, data_for_resolution)

                if src_list_for_move is None:
                    src_list_for_move = list_widget
                    src_item_for_move = item

            except Exception:
                src_list_for_move = list_widget
                src_item_for_move = item

            for idx, label in enumerate(opts):
                a = QAction(label, app)
                def _make_handler(i, source_list=src_list_for_move, source_item=src_item_for_move):
                    def _handler():
                        try:
                            keep_completed = _is_completed_list(app, source_list)
                            target = _target_list_for_quadrant(app, i, keep_completed=keep_completed)
                            if target is None or target is source_list:
                                return

                            new_state = Qt.Checked if keep_completed else Qt.Unchecked

                            source_list.blockSignals(True)
                            target.blockSignals(True)

                            try:
                                app.move_item_between_lists(source_item, source_list, target, new_state)

                            finally:
                                source_list.blockSignals(False)
                                target.blockSignals(False)

                            try:
                                app.save_tasks()

                            except Exception:
                                pass

                            try:
                                if hasattr(app, "calendar_pane") and app.calendar_pane:
                                    app.calendar_pane.calendar_panel.update_task_list()

                            except Exception:
                                pass

                        except Exception as e:
                            logger.error(f"Erro ao mover tarefa de quadrante via submenu: {e}", exc_info=True)

                    return _handler

                a.triggered.connect(_make_handler(idx))
                mover_menu.addAction(a)

            menu.addMenu(mover_menu)

        except Exception:
            mover_acao = QAction(get_text("🔀 Mover para outro quadrante"), app)
            mover_acao.triggered.connect(lambda: _move_to_quadrant(app, item, list_widget))
            menu.addAction(mover_acao)

        menu.addSeparator()
        remover_acao = QAction(get_text("🗑️ Remover Tarefa"), app)
        remover_acao.triggered.connect(lambda: remover_tarefa_item(app, item, list_widget, True))

        menu.addAction(remover_acao)
        menu.exec(list_widget.mapToGlobal(point))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {e}", exc_info=True)

def show_context_menu(app, point, list_widget):
    return mostrar_menu_contexto(app, point, list_widget)
