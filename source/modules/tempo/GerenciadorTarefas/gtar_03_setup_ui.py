from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTabWidget, QCheckBox, QStyle, QStyleOptionButton, QSizePolicy, QLayout
from PySide6.QtCore import Qt, QRect
from .gtar_26_FileDropLineEdit import FileDropLineEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class _IndicatorOnlyCheckBox(QCheckBox):
    def hitButton(self, pos):
        try:
            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, opt, self)
            spacing = self.style().pixelMetric(QStyle.PM_CheckBoxLabelSpacing, opt, self)
            text = self.text() or ""
            text_width = self.fontMetrics().horizontalAdvance(text)
            text_height = self.fontMetrics().height()
            text_x = indicator_rect.right() + max(0, spacing)
            text_y = int((self.height() - text_height) / 2)
            text_rect = QRect(text_x, text_y, max(0, text_width), max(0, text_height))
            clickable_rect = indicator_rect.united(text_rect)
            return clickable_rect.contains(pos)

        except Exception:
            return super().hitButton(pos)

def setup_ui(self):
    try:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinimumSize)

        linha_entrada = QHBoxLayout()

        self.input_tarefa = FileDropLineEdit(self, self)
        self.input_tarefa.returnPressed.connect(self.adicionar_tarefa)

        try:
            fm = self.input_tarefa.fontMetrics()
            target_h = int(fm.height() * 1) + 10
            self.input_tarefa.setMinimumHeight(max(24, target_h))

        except Exception:
            self.input_tarefa.setMinimumHeight(24)

        linha_entrada.addWidget(self.input_tarefa)

        self.combo_prioridade = QComboBox()
        linha_entrada.addWidget(self.combo_prioridade)

        layout.addLayout(linha_entrada)

        linha_botoes = QHBoxLayout()
        linha_botoes.setAlignment(Qt.AlignLeft)
        linha_botoes.setSizeConstraint(QLayout.SetMinimumSize)

        try:
            self.btn_adicionar = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_adicionar = QPushButton()

        self.btn_adicionar.clicked.connect(self.adicionar_tarefa)
        linha_botoes.addWidget(self.btn_adicionar)

        try:
            self._input_ref_height = max(1, int(self.btn_adicionar.sizeHint().height()))

            if hasattr(self, "input_tarefa") and self.input_tarefa is not None:
                self.input_tarefa.setFixedHeight(self._input_ref_height)

            if hasattr(self, "combo_prioridade") and self.combo_prioridade is not None:
                self.combo_prioridade.setFixedHeight(self._input_ref_height)

        except Exception:
            self._input_ref_height = 0

        try:
            self.btn_mover = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_mover = QPushButton()

        self.btn_mover.clicked.connect(self.mover_tarefas_marcadas)
        linha_botoes.addWidget(self.btn_mover)

        try:
            self.btn_remover = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_remover = QPushButton()

        self.btn_remover.clicked.connect(self.remover_tarefas_marcadas)
        linha_botoes.addWidget(self.btn_remover)

        try:
            self.btn_resetar_contagem = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_resetar_contagem = QPushButton()

        self.btn_resetar_contagem.clicked.connect(self.resetar_contagem_botao)
        linha_botoes.addWidget(self.btn_resetar_contagem)

        self.chk_fluxo_tarefas_concluidas = _IndicatorOnlyCheckBox()
        self.chk_fluxo_tarefas_concluidas.setChecked(False)
        self.chk_fluxo_tarefas_concluidas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        linha_botoes.addWidget(self.chk_fluxo_tarefas_concluidas)

        linha_botoes.addStretch()
        self._layout_linha_botoes = linha_botoes
        self._botoes_linha_principal = [
            self.btn_adicionar,
            self.btn_mover,
            self.btn_remover,
            self.btn_resetar_contagem,
        ]

        def _ajustar_linha_botoes():
            try:
                botoes = getattr(self, "_botoes_linha_principal", None) or []

                if not botoes:
                    return

                checkbox = getattr(self, "chk_fluxo_tarefas_concluidas", None)
                layout_botoes = getattr(self, "_layout_linha_botoes", None)

                if layout_botoes is None:
                    return

                spacing = layout_botoes.spacing()

                if spacing < 0:
                    spacing = 6

                margins = layout_botoes.contentsMargins()
                largura_checkbox = 0

                if checkbox is not None:
                    largura_checkbox = max(checkbox.minimumSizeHint().width(), checkbox.sizeHint().width())
                    checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    checkbox.setMinimumWidth(largura_checkbox)
                    checkbox.setMaximumWidth(largura_checkbox)

                largura_botoes = 0

                for btn in botoes:
                    largura_botoes += max(btn.minimumWidth(), btn.sizeHint().width())

                total_widgets = len(botoes) + (1 if checkbox is not None else 0)
                espacamentos = spacing * max(0, total_widgets - 1)
                largura_requerida = (
                    margins.left()
                    + margins.right()
                    + largura_botoes
                    + largura_checkbox
                    + espacamentos
                )

                largura_minima_atual = self.minimumWidth()
                self.setMinimumWidth(max(0, largura_requerida))

                if self.minimumWidth() != largura_minima_atual:
                    self.updateGeometry()

            except Exception:
                pass

        self._ajustar_linha_botoes = _ajustar_linha_botoes

        layout.addLayout(linha_botoes)

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
        self._ajustar_linha_botoes()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do GerenciadorTarefas: {str(e)}", exc_info=True)
