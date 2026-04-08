from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel,
                               QDateEdit, QTimeEdit, QCheckBox, QFileDialog, QLineEdit, QComboBox)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QDate, QTime, Qt, QUrl
from source.modules.eisenhower.services.svc_01_initUI import FileDropLineEdit
from source.modules.tempo.Tarefa import normalizar_prioridade
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class EditTaskDialog(QDialog):
    def __init__(self, svc, parent=None, initial_text="", initial_file="", initial_description="", initial_date=None, initial_time=None, initial_priority=None):
        super().__init__(parent or svc.app)
        self.svc = svc
        self.setModal(True)
        self.setWindowTitle(self.svc.get_text("Editar Tarefa") or "Editar Tarefa")
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(self.svc.get_text("Tarefa:")))
        self.title = QLineEdit(self)
        self.title.setText(initial_text or "")
        layout.addWidget(self.title)

        layout.addWidget(QLabel(self.svc.get_text("Prioridade:") or "Prioridade:"))
        self.priority_combo = QComboBox(self)
        priority_labels = [
            self.svc.get_text("🔴 Importante e Urgente"),
            self.svc.get_text("🟠 Importante, mas Não Urgente"),
            self.svc.get_text("🟡 Não Importante, mas Urgente"),
            self.svc.get_text("🟢 Não Importante e Não Urgente"),
        ]
        self.priority_combo.addItems(priority_labels)

        def _priority_index(value):
            try:
                if value is None:
                    return 0

                if isinstance(value, (int, float)) or (isinstance(value, str) and str(value).isdigit()):
                    idx = int(value) - 1
                    return idx if 0 <= idx <= 3 else 0

                try:
                    pr_norm = normalizar_prioridade(value)

                except Exception as e:
                    logger.error(f"Error normalizing priority: {e}")
                    pr_norm = str(value).strip()

                mapping = {
                    "Importante e Urgente": 0,
                    "Importante, mas Não Urgente": 1,
                    "Não Importante, mas Urgente": 2,
                    "Não Importante e Não Urgente": 3,
                }
                return mapping.get(pr_norm, 0)

            except Exception as e:
                logger.error(f"Error in _priority_index: {e}")
                return 0

        self.priority_combo.setCurrentIndex(_priority_index(initial_priority))
        layout.addWidget(self.priority_combo)

        layout.addWidget(QLabel(self.svc.get_text("Arquivo vinculado (arraste ou escolha):")))
        hl = QHBoxLayout()
        self.file_field = FileDropLineEdit(self.svc.app, self)
        self.file_field.setText(initial_file and (initial_file.split("\\")[-1] or initial_file) or "")
        self.file_field.setToolTip(initial_file or "")
        hl.addWidget(self.file_field)
        btn_choose = QPushButton(self.svc.get_text("Escolher..."))

        def _choose():
            try:
                path, _ = QFileDialog.getOpenFileName(self, self.svc.get_text("Escolher arquivo"), "", "*")
                if path:
                    self.file_field.setText(path.split("\\")[-1])
                    self.file_field.setToolTip(path)

            except Exception as e:
                logger.error(f"Error choosing file: {e}")

        btn_choose.clicked.connect(_choose)
        btn_clear = QPushButton(self.svc.get_text("Remover"))

        def _clear():
            try:
                self.file_field.clear()
                self.file_field.setToolTip("")

            except Exception as e:
                logger.error(f"Error clearing file field: {e}")

        btn_clear.clicked.connect(_clear)
        btn_open = QPushButton(self.svc.get_text("Abrir") or "Abrir")

        def _open_file():
            fp = self.file_field.toolTip() or None
            if not fp:
                return

            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(fp))

            except Exception as e:
                logger.error(f"Error opening file with QDesktopServices: {e}")

                try:
                    import os
                    import subprocess
                    import sys

                    if sys.platform.startswith("win"):
                        os.startfile(fp)

                    elif sys.platform.startswith("darwin"):
                        subprocess.Popen(["open", fp])

                    else:
                        subprocess.Popen(["xdg-open", fp])

                except Exception as e:
                    logger.error(f"Error opening file with fallback methods: {e}")

        btn_open.clicked.connect(_open_file)
        hl.addWidget(btn_choose)
        hl.addWidget(btn_clear)
        hl.addWidget(btn_open)
        layout.addLayout(hl)

        layout.addWidget(QLabel(self.svc.get_text("Descrição (opcional):")))
        self.desc = QTextEdit(self)
        self.desc.setPlainText(initial_description or "")
        self.desc.setMinimumHeight(120)
        layout.addWidget(self.desc)

        row_date = QHBoxLayout()
        self.cb_date = QCheckBox(self.svc.get_text("Vincular data"), self)
        self.de = QDateEdit(self)
        self.de.setCalendarPopup(True)
        self.de.setDisplayFormat(self.svc.app.date_input.displayFormat() if hasattr(self.svc.app, "date_input") else "dd/MM/yyyy")
        self.de.setDate(QDate.currentDate())
        self.svc._apply_widget_min_height(self.de, "dialog_date_edit")
        self.svc._apply_locale_to_dateedit(self.de)

        try:
            self.cb_date.setChecked(True)

        except Exception as e:
            logger.error(f"Error setting cb_date checked state: {e}")

        row_date.addWidget(self.cb_date)
        row_date.addWidget(self.de)
        layout.addLayout(row_date)

        row_time = QHBoxLayout()
        self.cb_time = QCheckBox(self.svc.get_text("Vincular horário"), self)
        self.te = QTimeEdit(self)
        self.te.setDisplayFormat("HH:mm")
        self.te.setTime(QTime.currentTime())
        self.svc._apply_widget_min_height(self.te, "dialog_time_edit")

        try:
            self.cb_time.setChecked(True)

        except Exception as e:
            logger.error(f"Error setting cb_time checked state: {e}")

        row_time.addWidget(self.cb_time)
        row_time.addWidget(self.te)
        layout.addLayout(row_time)

        if initial_date:
            try:
                qd = QDate.fromString(initial_date, Qt.ISODate)
                if qd.isValid():
                    self.cb_date.setChecked(True)
                    self.de.setDate(qd)

            except Exception as e:
                logger.error(f"Error setting initial date: {e}")

        if initial_time:
            try:
                qt = QTime.fromString(initial_time, "HH:mm")
                if qt.isValid():
                    self.cb_time.setChecked(True)
                    self.te.setTime(qt)

            except Exception as e:
                logger.error(f"Error setting initial time: {e}")

        def _sync_time_enabled():
            self.de.setEnabled(self.cb_date.isChecked())
            self.te.setEnabled(self.cb_date.isChecked() and self.cb_time.isChecked())

        self.cb_date.toggled.connect(lambda _: _sync_time_enabled())
        self.cb_time.toggled.connect(lambda _: _sync_time_enabled())
        _sync_time_enabled()

        btns = QHBoxLayout()
        btns.addStretch(1)
        btn_cancel = QPushButton(self.svc.get_text("Cancelar") or "Cancelar")
        btn_ok = QPushButton(self.svc.get_text("OK") or "OK")
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

        priority = None

        try:
            priority = int(self.priority_combo.currentIndex()) + 1

        except Exception as e:
            logger.error(f"Error getting priority: {e}")
            priority = None

        return self.title.text().strip(), fp, self.desc.toPlainText().strip(), new_date_iso, new_time_str, priority
