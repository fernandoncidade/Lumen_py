from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTabWidget
from source.modules.eisenhower.services.svc_01_initUI import FileDropLineEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        adicionar = QHBoxLayout()

        self.input_tarefa = FileDropLineEdit(self, self)
        self.input_tarefa.returnPressed.connect(self.adicionar_tarefa)

        try:
            fm = self.input_tarefa.fontMetrics()
            target_h = int(fm.height() * 1) + 10
            self.input_tarefa.setMinimumHeight(max(24, target_h))

        except Exception:
            self.input_tarefa.setMinimumHeight(24)

        adicionar.addWidget(self.input_tarefa)

        self.combo_prioridade = QComboBox()
        adicionar.addWidget(self.combo_prioridade)

        self.btn_adicionar = QPushButton()
        self.btn_adicionar.clicked.connect(self.adicionar_tarefa)
        adicionar.addWidget(self.btn_adicionar)

        self.btn_mover = QPushButton()
        self.btn_mover.clicked.connect(self.mover_tarefas_marcadas)
        adicionar.addWidget(self.btn_mover)

        self.btn_remover = QPushButton()
        self.btn_remover.clicked.connect(self.remover_tarefas_marcadas)
        adicionar.addWidget(self.btn_remover)

        self.btn_resetar_contagem = QPushButton()
        self.btn_resetar_contagem.clicked.connect(self.resetar_contagem_botao)
        adicionar.addWidget(self.btn_resetar_contagem)

        layout.addLayout(adicionar)

        self.col_todo = self.criar_coluna("Todo")
        self.col_doing = self.criar_coluna("Doing")
        self.col_done = self.criar_coluna("Done")

        class _AutoOpenTabWidget(QTabWidget):
            def __init__(self, owner, parent=None):
                super().__init__(parent)
                self._owner = owner
                self.setAcceptDrops(True)

            def dragEnterEvent(self, event):
                try:
                    event.acceptProposedAction()

                except Exception:
                    pass

            def dragMoveEvent(self, event):
                try:
                    tb = self.tabBar()
                    pos = tb.mapFrom(self, event.pos())
                    idx = tb.tabAt(pos)

                    if idx is not None and idx >= 0 and idx != self.currentIndex():
                        self.setCurrentIndex(idx)

                    event.acceptProposedAction()

                except Exception:
                    try:
                        super().dragMoveEvent(event)

                    except Exception:
                        pass

            def dropEvent(self, event):
                try:
                    tb = self.tabBar()
                    pos = tb.mapFrom(self, event.pos())
                    idx = tb.tabAt(pos)

                    if idx is not None and idx >= 0:
                        self.setCurrentIndex(idx)
                        target_list = None

                        try:
                            tab_widget = self.widget(idx)

                            if hasattr(tab_widget, "lista"):
                                target_list = tab_widget.lista

                            else:
                                from PySide6.QtWidgets import QListWidget
                                target_list = tab_widget.findChild(QListWidget) if tab_widget is not None else None

                        except Exception:
                            target_list = None

                        if target_list is not None:
                            try:
                                from PySide6.QtCore import Qt
                                from PySide6.QtWidgets import QListWidget

                                source_list = event.source()

                                if isinstance(source_list, QListWidget) and source_list is not target_list:
                                    items = source_list.selectedItems() or []

                                    if not items and source_list.currentItem() is not None:
                                        items = [source_list.currentItem()]

                                    for item in items:
                                        row = source_list.row(item)

                                        if row >= 0:
                                            moved = source_list.takeItem(row)

                                            if moved is not None:
                                                target_list.addItem(moved)

                                    if hasattr(self._owner, "_sincronizar_status_pos_movimento"):
                                        self._owner._sincronizar_status_pos_movimento(prioridade_lista=target_list)

                                    if hasattr(self._owner, "atualizar_listas") and callable(self._owner.atualizar_listas):
                                        self._owner.atualizar_listas()

                                    elif hasattr(self._owner, "listas_atualizadas"):
                                        try:
                                            self._owner.listas_atualizadas.emit()

                                        except Exception:
                                            pass

                                    event.setDropAction(Qt.MoveAction)
                                    event.accept()
                                    return

                            except Exception:
                                pass

                    event.ignore()

                except Exception:
                    try:
                        super().dropEvent(event)

                    except Exception:
                        pass

        tabs = _AutoOpenTabWidget(self)
        tabs.addTab(self.col_todo, "📋 A Fazer")
        tabs.addTab(self.col_doing, "⚙️ Em Progresso")
        tabs.addTab(self.col_done, "✅ Concluído")

        self.status_tabs = tabs

        layout.addWidget(tabs)

        self.setLayout(layout)
        self.atualizar_traducoes()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do GerenciadorTarefas: {str(e)}", exc_info=True)
