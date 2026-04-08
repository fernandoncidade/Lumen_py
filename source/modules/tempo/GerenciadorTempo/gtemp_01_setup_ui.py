from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QGroupBox, QSplitter, QWidget, QAbstractItemView
from PySide6.QtCore import Qt, QTimer
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_02_PomodoroTimer import PomodoroTimer
from source.modules.tempo.tmp_03_GerenciadorTarefas import GerenciadorTarefas
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        left_col = QVBoxLayout()
        left_col.setContentsMargins(0, 0, 0, 0)

        self.pomodoro = PomodoroTimer(self)
        self.pomodoro.ciclo_completado.connect(self._tempo_worker.on_pomodoro)
        left_col.addWidget(self.pomodoro)

        header = QHBoxLayout()
        self.label_tarefas = QLabel()
        self.label_tarefas.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px;")
        header.addWidget(self.label_tarefas, 1)
        left_col.addLayout(header)

        self.tarefas = GerenciadorTarefas(self)
        self.tarefas.listas_atualizadas.connect(self.atualizar_coluna_doing_timer)

        try:
            self.tarefas.tarefa_adicionada.connect(self._on_tarefa_adicionada_gestao_tempo)

        except Exception:
            pass

        left_col.addWidget(self.tarefas)

        self.col_doing_timer_group = QGroupBox()
        doing_timer_layout = QVBoxLayout()
        self.col_doing_timer_list = QListWidget()
        self.col_doing_timer_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.col_doing_timer_list.setSelectionBehavior(QAbstractItemView.SelectItems)

        try:
            self.col_doing_timer_list.setSelectionRectVisible(True)

        except Exception:
            pass

        self.col_doing_timer_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.col_doing_timer_list.itemDoubleClicked.connect(self._abrir_arquivo_vinculado_coluna_doing_timer)
        self.col_doing_timer_list.customContextMenuRequested.connect(self._mostrar_menu_contexto_coluna_doing_timer)
        self.col_doing_timer_list.setDragDropMode(QListWidget.NoDragDrop)
        doing_timer_layout.addWidget(self.col_doing_timer_list)
        self.col_doing_timer_group.setLayout(doing_timer_layout)

        left_widget = QWidget(self)
        left_widget.setLayout(left_col)
        self.left_widget = left_widget

        self.main_splitter = QSplitter(Qt.Horizontal, self)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.addWidget(left_widget)
        self.main_splitter.addWidget(self.col_doing_timer_group)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, False)
        self.main_splitter.setStretchFactor(0, 3)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setHandleWidth(6)

        self._ajustar_largura_minima_coluna_esquerda()
        self.col_doing_timer_group.setMinimumWidth(280)
        self.main_splitter.setSizes([1080, 360])

        layout.addWidget(self.main_splitter)

        self.setLayout(layout)
        self.atualizar_traducoes()
        QTimer.singleShot(0, self._ajustar_largura_minima_coluna_esquerda)
        QTimer.singleShot(50, self._ajustar_largura_minima_coluna_esquerda)
        self.atualizar_coluna_doing_timer()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do GerenciadorTempo: {str(e)}", exc_info=True)
