from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        adicionar = QHBoxLayout()

        self.input_tarefa = QLineEdit()
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

        kanban = QHBoxLayout()
        self.col_todo = self.criar_coluna("Todo")
        kanban.addWidget(self.col_todo)

        self.col_doing = self.criar_coluna("Doing")
        kanban.addWidget(self.col_doing)

        self.col_done = self.criar_coluna("Done")
        kanban.addWidget(self.col_done)

        layout.addLayout(kanban)

        self.setLayout(layout)
        self.atualizar_traducoes()
        self.atualizar_listas()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do GerenciadorTarefas: {str(e)}", exc_info=True)
