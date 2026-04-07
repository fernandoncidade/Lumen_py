from PySide6.QtWidgets import QMenu, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QFileDialog, QDateEdit, QTimeEdit, QCheckBox, QSpinBox
from PySide6.QtCore import QCoreApplication, Qt, QDate, QTime, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from source.modules.eisenhower.services.svc_01_initUI import FileDropLineEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, pos, lista):
    try:
        item = lista.itemAt(pos)
        if not item:
            return

        menu = QMenu(lista)

        ac_mover_unico = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa"), self)
        ac_mover_unico.triggered.connect(lambda: self.mover_tarefa_por_item(item))
        menu.addAction(ac_mover_unico)

        def _editar_tarefa():
            try:
                tarefa_id = item.data(Qt.UserRole)
                alvo = None
                for t in getattr(self, 'tarefas', []):
                    if getattr(t, 'id', None) == tarefa_id:
                        alvo = t
                        break

                if not alvo:
                    titulo_item = (
                        item.text().split('\n')[0]
                        .replace('🔴 ', '')
                        .replace('🟠 ', '')
                        .replace('🟡 ', '')
                        .replace('🟢 ', '')
                    )
                    for t in getattr(self, 'tarefas', []):
                        if getattr(t, 'titulo', None) == titulo_item:
                            alvo = t
                            break

                if not alvo:
                    return

                def _strip_emoji(s: str) -> str:
                    return (s or '').replace('🔴 ', '').replace('🟠 ', '').replace('🟡 ', '').replace('🟢 ', '').strip()

                class EditTaskDialog(QDialog):
                    def __init__(self, parent=None, initial_text="", initial_file="", initial_description="", initial_date=None, initial_time=None, initial_pomodoros=0):
                        super().__init__(parent or self)
                        self.setModal(True)
                        self.setWindowTitle(QCoreApplication.translate("App", "Editar Tarefa") or "Editar Tarefa")
                        layout = QVBoxLayout(self)

                        layout.addWidget(QLabel(QCoreApplication.translate("App", "Tarefa:")))
                        self.title = QLineEdit(self)
                        self.title.setText(initial_text or "")
                        layout.addWidget(self.title)

                        layout.addWidget(QLabel(QCoreApplication.translate("App", "Arquivo vinculado (arraste ou escolha):")))
                        hl = QHBoxLayout()
                        self.file_field = FileDropLineEdit(self, self)
                        self.file_field.setText(initial_file and (initial_file.split("\\")[-1] or initial_file) or "")
                        self.file_field.setToolTip(initial_file or "")
                        hl.addWidget(self.file_field)
                        btn_choose = QPushButton(QCoreApplication.translate("App", "Escolher...") or "Escolher...")

                        def _choose():
                            try:
                                path, _ = QFileDialog.getOpenFileName(self, QCoreApplication.translate("App", "Escolher arquivo"), "", "*")
                                if path:
                                    self.file_field.setText(path.split("\\")[-1])
                                    self.file_field.setToolTip(path)

                            except Exception as e:
                                logger.error(f"Erro ao escolher arquivo: {str(e)}", exc_info=True)

                        btn_choose.clicked.connect(_choose)
                        btn_clear = QPushButton(QCoreApplication.translate("App", "Remover") or "Remover")

                        def _clear():
                            try:
                                self.file_field.clear()
                                self.file_field.setToolTip("")

                            except Exception as e:
                                logger.error(f"Erro ao limpar campo de arquivo: {str(e)}", exc_info=True)

                        btn_clear.clicked.connect(_clear)
                        btn_open = QPushButton(QCoreApplication.translate("App", "Abrir") or "Abrir")

                        def _open_file():
                            fp = self.file_field.toolTip() or None
                            if not fp:
                                return

                            try:
                                QDesktopServices.openUrl(QUrl.fromLocalFile(fp))

                            except Exception as e:
                                logger.error(f"Erro ao abrir arquivo: {str(e)}", exc_info=True)

                                try:
                                    import os, subprocess, sys
                                    if sys.platform.startswith("win"):
                                        os.startfile(fp)

                                    elif sys.platform.startswith("darwin"):
                                        subprocess.Popen(["open", fp])

                                    else:
                                        subprocess.Popen(["xdg-open", fp])

                                except Exception as e2:
                                    logger.error(f"Erro ao abrir arquivo com método alternativo: {str(e2)}", exc_info=True)

                        btn_open.clicked.connect(_open_file)
                        hl.addWidget(btn_choose)
                        hl.addWidget(btn_clear)
                        hl.addWidget(btn_open)
                        layout.addLayout(hl)

                        layout.addWidget(QLabel(QCoreApplication.translate("App", "Descrição (opcional):")))
                        self.desc = QTextEdit(self)
                        self.desc.setPlainText(initial_description or "")
                        self.desc.setMinimumHeight(120)
                        layout.addWidget(self.desc)

                        row_date = QHBoxLayout()
                        self.cb_date = QCheckBox(QCoreApplication.translate("App", "Vincular data"), self)
                        self.de = QDateEdit(self)
                        self.de.setCalendarPopup(True)
                        self.de.setDisplayFormat("dd/MM/yyyy")
                        self.de.setDate(QDate.currentDate())
                        row_date.addWidget(self.cb_date)
                        row_date.addWidget(self.de)
                        layout.addLayout(row_date)

                        row_time = QHBoxLayout()
                        self.cb_time = QCheckBox(QCoreApplication.translate("App", "Vincular horário"), self)
                        self.te = QTimeEdit(self)
                        self.te.setDisplayFormat("HH:mm")
                        self.te.setTime(QTime.currentTime())
                        row_time.addWidget(self.cb_time)
                        row_time.addWidget(self.te)
                        layout.addLayout(row_time)

                        try:
                            self.cb_date.setChecked(True)

                        except Exception as e:
                            logger.error(f"Erro ao definir estado do checkbox de data: {str(e)}", exc_info=True)

                        try:
                            self.cb_time.setChecked(True)

                        except Exception as e:
                            logger.error(f"Erro ao definir estado do checkbox de horário: {str(e)}", exc_info=True)

                        if initial_date:
                            try:
                                qd = QDate.fromString(initial_date, Qt.ISODate)
                                if qd.isValid():
                                    self.cb_date.setChecked(True)
                                    self.de.setDate(qd)

                            except Exception as e:
                                logger.error(f"Erro ao definir data inicial: {str(e)}", exc_info=True)

                        if initial_time:
                            try:
                                qt = QTime.fromString(initial_time, "HH:mm")
                                if qt.isValid():
                                    self.cb_time.setChecked(True)
                                    self.te.setTime(qt)

                            except Exception as e:
                                logger.error(f"Erro ao definir horário inicial: {str(e)}", exc_info=True)

                        def _sync_time_enabled():
                            self.de.setEnabled(self.cb_date.isChecked())
                            self.te.setEnabled(self.cb_date.isChecked() and self.cb_time.isChecked())

                        self.cb_date.toggled.connect(lambda _: _sync_time_enabled())
                        self.cb_time.toggled.connect(lambda _: _sync_time_enabled())
                        _sync_time_enabled()

                        try:
                            row_pomo = QHBoxLayout()
                            lbl_pomo = QLabel(QCoreApplication.translate("App", "Pomodoros concluídos:"))
                            row_pomo.addWidget(lbl_pomo)
                            row_pomo.addStretch(1)
                            self.spin_pomodoros = QSpinBox(self)
                            self.spin_pomodoros.setMinimum(0)
                            self.spin_pomodoros.setMaximum(9999)

                            try:
                                self.spin_pomodoros.setValue(int(initial_pomodoros or 0))

                            except Exception:
                                self.spin_pomodoros.setValue(0)

                            row_pomo.addWidget(self.spin_pomodoros)
                            layout.addLayout(row_pomo)

                        except Exception as e:
                            logger.error(f"Erro ao criar campo de pomodoros no diálogo: {str(e)}", exc_info=True)

                        btns = QHBoxLayout()
                        btns.addStretch(1)
                        btn_cancel = QPushButton(QCoreApplication.translate("App", "Cancelar") or "Cancelar")
                        btn_ok = QPushButton(QCoreApplication.translate("App", "OK") or "OK")
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

                        pomodoros_val = None

                        try:
                            pomodoros_val = int(getattr(self, 'spin_pomodoros', None).value()) if hasattr(self, 'spin_pomodoros') else None

                        except Exception:
                            pomodoros_val = None

                        return self.title.text().strip(), fp, self.desc.toPlainText().strip(), new_date_iso, new_time_str, pomodoros_val

                initial_text = getattr(alvo, 'titulo', '') or ''
                initial_file = getattr(alvo, 'file_path', '') or ''
                initial_desc = getattr(alvo, 'descricao', '') or ''
                initial_date = getattr(alvo, 'date', None)
                initial_time = getattr(alvo, 'time', None)

                dlg = EditTaskDialog(parent=self, initial_text=initial_text, initial_file=initial_file, initial_description=initial_desc, initial_date=initial_date, initial_time=initial_time, initial_pomodoros=getattr(alvo, 'pomodoros_completados', 0))
                if dlg.exec() != QDialog.Accepted:
                    return

                new_text, new_file_path, new_desc, new_date_iso, new_time_str, new_pomodoros = dlg.get_values()
                if not new_text:
                    return

                try:
                    alvo.titulo = new_text
                    alvo.descricao = new_desc

                    try:
                        if new_pomodoros is not None:
                            alvo.pomodoros_completados = int(new_pomodoros)

                    except Exception as e:
                        logger.error(f"Erro ao aplicar pomodoros na tarefa: {str(e)}", exc_info=True)

                    if new_file_path:
                        alvo.file_path = new_file_path

                    else:
                        alvo.file_path = None

                    if new_date_iso is not None:
                        alvo.date = new_date_iso

                    else:
                        alvo.date = None

                    if new_time_str is not None:
                        alvo.time = new_time_str

                    else:
                        alvo.time = None

                except Exception as e:
                    logger.error(f"Erro ao aplicar campos na tarefa: {str(e)}", exc_info=True)

                try:
                    self.salvar_tarefas()

                except Exception as e:
                    logger.error(f"Erro ao salvar tarefas: {str(e)}", exc_info=True)

                try:
                    self.atualizar_listas()

                except Exception as e:
                    logger.error(f"Erro ao atualizar listas: {str(e)}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro ao editar tarefa: {str(e)}", exc_info=True)

        ac_editar = QAction(QCoreApplication.translate("App", "✏️ Editar Tarefa"), self)
        ac_editar.triggered.connect(_editar_tarefa)
        menu.addAction(ac_editar)

        try:
            compartilhar_acao = QAction(QCoreApplication.translate("App", "🗂️ Compartilhar com Eisenhower") or "🗂️ Compartilhar com Eisenhower", self)

            def _compartilhar_eisenhower():
                try:
                    from uuid import uuid4
                    from source.utils.EventBus import get_event_bus
                    from source.modules.tempo.tmp_01_Tarefa import Tarefa
                    from PySide6.QtWidgets import QMessageBox

                    tarefa_id = item.data(Qt.UserRole)
                    alvo = None
                    for t in getattr(self, 'tarefas', []):
                        if getattr(t, 'id', None) == tarefa_id:
                            alvo = t
                            break

                    if not alvo:
                        titulo_item = (
                            item.text().split('\n')[0]
                            .replace('🔴 ', '')
                            .replace('🟠 ', '')
                            .replace('🟡 ', '')
                            .replace('🟢 ', '')
                        )
                        for t in getattr(self, 'tarefas', []):
                            if getattr(t, 'titulo', None) == titulo_item:
                                alvo = t
                                break

                    if not alvo:
                        return

                    titulo = getattr(alvo, 'titulo', '') or ''
                    prioridade_raw = getattr(alvo, 'prioridade', None) or 'Importante e Urgente'
                    prioridade_norm = Tarefa.normalizar_prioridade(prioridade_raw)
                    date_iso = getattr(alvo, 'date', None)
                    time_str = getattr(alvo, 'time', None)
                    description = getattr(alvo, 'descricao', None)
                    file_path = getattr(alvo, 'file_path', None)

                    payload = {
                        'integration_id': str(uuid4()),
                        'origin': 'tempo',
                        'titulo': titulo,
                        'prioridade': prioridade_norm,
                        'date': date_iso,
                        'time': time_str,
                        'description': description,
                        'file_path': file_path,
                    }

                    try:
                        get_event_bus().send_tarefa(payload)

                        try:
                            QMessageBox.information(self, QCoreApplication.translate('App', 'Sucesso') or 'Sucesso', QCoreApplication.translate('App', 'Tarefa enviada com sucesso para 🗂️ Matriz Eisenhower! 🗂️'))

                        except Exception:
                            pass

                    except Exception as e:
                        logger.debug(f"Falha ao enviar tarefa ao Eisenhower: {e}", exc_info=True)

                except Exception as e:
                    logger.error(f"Erro ao compartilhar tarefa com Eisenhower: {str(e)}", exc_info=True)

            compartilhar_acao.triggered.connect(_compartilhar_eisenhower)
            menu.addAction(compartilhar_acao)

        except Exception:
            pass

        if self._ha_tarefas_marcadas():
            ac_mover_marcadas = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa(s) Marcadas"), self)
            ac_mover_marcadas.triggered.connect(self.mover_tarefas_marcadas)
            menu.addAction(ac_mover_marcadas)

        ac_remover = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa"), self)
        ac_remover.triggered.connect(lambda: self.remover_tarefa_por_item(item))
        menu.addAction(ac_remover)

        if self._ha_tarefas_marcadas():
            ac_remover_marcadas = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa(s) Marcadas"), self)
            ac_remover_marcadas.triggered.connect(self.remover_tarefas_marcadas)
            menu.addAction(ac_remover_marcadas)

        menu.exec(lista.mapToGlobal(pos))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {str(e)}", exc_info=True)
