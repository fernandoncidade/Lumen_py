from PySide6.QtWidgets import QMenu, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QFileDialog, QDateEdit, QTimeEdit, QCheckBox, QSpinBox, QCalendarWidget
from PySide6.QtCore import QCoreApplication, Qt, QDate, QTime, QUrl, QLocale
from PySide6.QtGui import QAction, QDesktopServices
from source.modules.eisenhower.services.svc_01_initUI import FileDropLineEdit
from source.utils.LogManager import LogManager
from source.utils.task_identity import task_identity_signature
logger = LogManager.get_logger()

def mostrar_menu_contexto(self, pos, lista):
    try:
        item = lista.itemAt(pos)

        if not item:
            return

        menu = QMenu(lista)

        def _strip_emoji(s: str) -> str:
            return (s or '').replace('🔴 ', '').replace('🟠 ', '').replace('🟡 ', '').replace('🟢 ', '').strip()

        def _collect_selected_items():
            selecionados = []
            vistos = set()

            for lst in (self.col_todo.lista, self.col_doing.lista, self.col_done.lista):
                try:
                    for it in lst.selectedItems() or []:
                        tid = it.data(Qt.UserRole)
                        titulo = _strip_emoji(it.text().split('\n')[0])
                        chave = tid or titulo

                        if chave in vistos:
                            continue

                        vistos.add(chave)
                        selecionados.append(it)

                except Exception:
                    pass

                for i in range(lst.count()):
                    it = lst.item(i)

                    if it and it.checkState() == Qt.Checked:
                        tid = it.data(Qt.UserRole)
                        titulo = _strip_emoji(it.text().split('\n')[0])
                        chave = tid or titulo

                        if chave in vistos:
                            continue

                        vistos.add(chave)
                        selecionados.append(it)

            return selecionados

        selecionados = _collect_selected_items()

        if not selecionados:
            selecionados = [item]

        selecionados_count = len(selecionados)

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

                class EditTaskDialog(QDialog):
                    def __init__(self, parent=None, initial_text="", initial_file="", initial_description="", initial_date=None, initial_time=None, initial_pomodoros=0, initial_priority=None):
                        super().__init__(parent or self)
                        self.setModal(True)
                        self.setWindowTitle(QCoreApplication.translate("App", "Editar Tarefa") or "Editar Tarefa")
                        layout = QVBoxLayout(self)

                        layout.addWidget(QLabel(QCoreApplication.translate("App", "Tarefa:")))
                        self.title = QLineEdit(self)
                        self.title.setText(initial_text or "")
                        layout.addWidget(self.title)

                        layout.addWidget(QLabel(QCoreApplication.translate("App", "Prioridade:")))
                        self.combo_prioridade = QComboBox(self)
                        self.combo_prioridade.addItems([
                            QCoreApplication.translate("App", "🔴 Importante e Urgente"),
                            QCoreApplication.translate("App", "🟠 Importante, mas Não Urgente"),
                            QCoreApplication.translate("App", "🟡 Não Importante, mas Urgente"),
                            QCoreApplication.translate("App", "🟢 Não Importante e Não Urgente"),
                        ])

                        try:
                            from source.modules.tempo.tmp_01_Tarefa import Tarefa
                            prioridade_norm = Tarefa.normalizar_prioridade(initial_priority or "")

                        except Exception:
                            prioridade_norm = (initial_priority or "")

                        idx_map = {
                            "Importante e Urgente": 0,
                            "Importante, mas Não Urgente": 1,
                            "Não Importante, mas Urgente": 2,
                            "Não Importante e Não Urgente": 3,
                        }

                        self.combo_prioridade.setCurrentIndex(idx_map.get(prioridade_norm, 0))
                        layout.addWidget(self.combo_prioridade)

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
                        self._apply_date_display_format()
                        self.de.setDate(QDate.currentDate())
                        self._apply_locale_to_dateedit()
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
                        self._install_dynamic_language_sync()

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

                    def _effective_locale(self) -> QLocale:
                        try:
                            app = QCoreApplication.instance()

                            if app is not None and hasattr(app, "gerenciador_traducao") and app.gerenciador_traducao is not None:
                                idioma = app.gerenciador_traducao.obter_idioma_atual()

                                if idioma and idioma.startswith("pt"):
                                    return QLocale(QLocale.Portuguese, QLocale.Brazil)

                                if idioma and idioma.startswith("en"):
                                    return QLocale(QLocale.English, QLocale.UnitedStates)

                        except Exception as e:
                            logger.error(f"Erro ao obter locale efetivo do diálogo de edição: {str(e)}", exc_info=True)

                        return QLocale.system()

                    def _effective_date_format(self) -> str:
                        try:
                            app = QCoreApplication.instance()

                            if app is not None and hasattr(app, "gerenciador_traducao") and app.gerenciador_traducao is not None:
                                idioma = app.gerenciador_traducao.obter_idioma_atual()

                                if idioma and idioma.startswith("pt"):
                                    return "dd/MM/yyyy"

                                if idioma and idioma.startswith("en"):
                                    return "MM/dd/yyyy"

                        except Exception as e:
                            logger.error(f"Erro ao obter formato de data efetivo do diálogo de edição: {str(e)}", exc_info=True)

                        return "dd/MM/yyyy"

                    def _apply_date_display_format(self):
                        try:
                            self.de.setDisplayFormat(self._effective_date_format())

                        except Exception as e:
                            logger.error(f"Erro ao aplicar display format no diálogo de edição: {str(e)}", exc_info=True)

                    def _apply_locale_to_dateedit(self):
                        try:
                            loc = self._effective_locale()
                            self.de.setLocale(loc)
                            self._apply_date_display_format()
                            self.de.setCalendarPopup(True)

                            cw = self.de.calendarWidget()

                            if cw is None:
                                cw = QCalendarWidget(self.de)
                                self.de.setCalendarWidget(cw)

                            cw.setLocale(loc)
                            cw.setFirstDayOfWeek(loc.firstDayOfWeek())
                            cw.update()
                            self.de.update()

                        except Exception as e:
                            logger.error(f"Erro ao aplicar locale no calendário de edição de tarefa: {str(e)}", exc_info=True)

                    def _on_language_changed(self, _=None):
                        try:
                            self._apply_date_display_format()
                            self._apply_locale_to_dateedit()

                        except Exception as e:
                            logger.error(f"Erro ao atualizar locale após troca de idioma no diálogo de edição: {str(e)}", exc_info=True)

                    def _install_dynamic_language_sync(self):
                        try:
                            app = QCoreApplication.instance()

                            if app is not None and hasattr(app, "gerenciador_traducao") and app.gerenciador_traducao is not None:
                                if not getattr(self, "_language_sync_connected", False):
                                    app.gerenciador_traducao.idioma_alterado.connect(self._on_language_changed)
                                    self._language_sync_connected = True

                        except Exception as e:
                            logger.error(f"Erro ao conectar atualização dinâmica de idioma no diálogo de edição: {str(e)}", exc_info=True)

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

                        return self.title.text().strip(), fp, self.desc.toPlainText().strip(), new_date_iso, new_time_str, pomodoros_val, self.combo_prioridade.currentText()

                initial_text = getattr(alvo, 'titulo', '') or ''
                initial_file = getattr(alvo, 'file_path', '') or ''
                initial_desc = getattr(alvo, 'descricao', '') or ''
                initial_date = getattr(alvo, 'date', None)
                initial_time = getattr(alvo, 'time', None)
                initial_priority = getattr(alvo, 'prioridade', None)

                dlg = EditTaskDialog(parent=self, initial_text=initial_text, initial_file=initial_file, initial_description=initial_desc, initial_date=initial_date, initial_time=initial_time, initial_pomodoros=getattr(alvo, 'pomodoros_completados', 0), initial_priority=initial_priority)

                if dlg.exec() != QDialog.Accepted:
                    return

                new_text, new_file_path, new_desc, new_date_iso, new_time_str, new_pomodoros, new_prioridade = dlg.get_values()

                if not new_text:
                    return

                try:
                    try:
                        from source.modules.tempo.tmp_01_Tarefa import Tarefa
                        alvo.prioridade = Tarefa.normalizar_prioridade(new_prioridade)

                    except Exception:
                        alvo.prioridade = new_prioridade

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

                    def _resolve_tarefa(it):
                        tarefa_id = it.data(Qt.UserRole)

                        if tarefa_id:
                            for t in getattr(self, 'tarefas', []):
                                if getattr(t, 'id', None) == tarefa_id:
                                    return t

                        titulo_item = (
                            it.text().split('\n')[0]
                            .replace('🔴 ', '')
                            .replace('🟠 ', '')
                            .replace('🟡 ', '')
                            .replace('🟢 ', '')
                        )

                        for t in getattr(self, 'tarefas', []):
                            if getattr(t, 'titulo', None) == titulo_item:
                                return t

                        return None

                    itens = list(selecionados or [])

                    if not itens:
                        itens = [item]

                    enviados = 0
                    vistos = set()

                    for it in itens:
                        alvo = _resolve_tarefa(it)

                        if not alvo:
                            continue

                        chave = task_identity_signature(alvo)

                        if chave in vistos:
                            continue

                        vistos.add(chave)

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
                            'id': getattr(alvo, 'id', None),
                            'titulo': titulo,
                            'prioridade': prioridade_norm,
                            'date': date_iso,
                            'time': time_str,
                            'description': description,
                            'file_path': file_path,
                        }

                        try:
                            get_event_bus().send_tarefa(payload)
                            enviados += 1

                        except Exception as e:
                            logger.debug(f"Falha ao enviar tarefa ao Eisenhower: {e}", exc_info=True)

                    if enviados > 0:
                        try:
                            msg = QCoreApplication.translate('App', 'Tarefa enviada com sucesso para 🗂️ Matriz Eisenhower! 🗂️')

                            if enviados > 1:
                                msg = QCoreApplication.translate('App', '{n} tarefas enviadas com sucesso para 🗂️ Matriz Eisenhower! 🗂️').format(n=enviados)

                            QMessageBox.information(self, QCoreApplication.translate('App', 'Sucesso') or 'Sucesso', msg)

                        except Exception:
                            pass

                except Exception as e:
                    logger.error(f"Erro ao compartilhar tarefa com Eisenhower: {str(e)}", exc_info=True)

            compartilhar_acao.triggered.connect(_compartilhar_eisenhower)
            menu.addAction(compartilhar_acao)

        except Exception:
            pass

        if selecionados_count > 1:
            ac_mover_marcadas = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa(s) Marcadas"), self)
            ac_mover_marcadas.triggered.connect(self.mover_tarefas_marcadas)
            menu.addAction(ac_mover_marcadas)

            ac_remover_marcadas = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa(s) Marcadas"), self)
            ac_remover_marcadas.triggered.connect(self.remover_tarefas_marcadas)
            menu.addAction(ac_remover_marcadas)

        else:
            ac_mover_unico = QAction(QCoreApplication.translate("App", "🔀 Mover Tarefa"), self)
            ac_mover_unico.triggered.connect(lambda: self.mover_tarefa_por_item(item))
            menu.addAction(ac_mover_unico)

            ac_remover = QAction(QCoreApplication.translate("App", "🗑️ Remover Tarefa"), self)
            ac_remover.triggered.connect(lambda: self.remover_tarefa_por_item(item))
            menu.addAction(ac_remover)

        menu.exec(lista.mapToGlobal(pos))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {str(e)}", exc_info=True)
