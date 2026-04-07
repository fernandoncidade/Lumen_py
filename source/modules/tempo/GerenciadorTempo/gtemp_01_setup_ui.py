from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QGroupBox, QPushButton
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_02_PomodoroTimer import PomodoroTimer
from source.modules.tempo.tmp_03_GerenciadorTarefas import GerenciadorTarefas
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        topo = QHBoxLayout()

        self.pomodoro = PomodoroTimer(self)
        self.pomodoro.ciclo_completado.connect(self._tempo_worker.on_pomodoro)
        topo.addWidget(self.pomodoro, 2)

        self.col_doing_timer_group = QGroupBox()
        doing_timer_layout = QVBoxLayout()
        self.col_doing_timer_list = QListWidget()
        self.col_doing_timer_list.setDragDropMode(QListWidget.NoDragDrop)
        doing_timer_layout.addWidget(self.col_doing_timer_list)
        self.col_doing_timer_group.setLayout(doing_timer_layout)
        topo.addWidget(self.col_doing_timer_group, 1)

        layout.addLayout(topo)

        header = QHBoxLayout()
        self.label_tarefas = QLabel()
        self.label_tarefas.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px;")
        header.addWidget(self.label_tarefas, 1)

        self.btn_eisenhower_integrado = QPushButton()
        self.btn_eisenhower_integrado.setCheckable(True)
        self.btn_eisenhower_integrado.setChecked(False)

        try:
            self.btn_eisenhower_integrado.toggled.connect(lambda _: self._atualizar_rotulo_botao_eisenhower())

        except Exception:
            pass

        header.addWidget(self.btn_eisenhower_integrado, 0)
        layout.addLayout(header)

        self.tarefas = GerenciadorTarefas(self)
        self.tarefas.listas_atualizadas.connect(self.atualizar_coluna_doing_timer)

        try:
            self.tarefas.tarefa_adicionada.connect(self._on_tarefa_adicionada_gestao_tempo)

        except Exception:
            pass

        layout.addWidget(self.tarefas)

        self.setLayout(layout)
        self.atualizar_traducoes()
        self.atualizar_coluna_doing_timer()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do GerenciadorTempo: {str(e)}", exc_info=True)
