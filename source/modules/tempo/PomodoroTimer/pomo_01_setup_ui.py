from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QGroupBox, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        self.label_tempo = QLabel("25:00")
        fonte = QFont("Arial", 48, QFont.Bold)
        self.label_tempo.setFont(fonte)
        self.label_tempo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_tempo)

        self.progress = QProgressBar()
        self.progress.setMaximum(self.tempo_foco)
        self.progress.setValue(self.tempo_foco)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        self.label_status = QLabel()
        fonte_status = QFont("Arial", 14, QFont.Bold)
        self.label_status.setFont(fonte_status)
        self.label_status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_status)

        controles = QHBoxLayout()

        self.btn_iniciar = self.gerenciador_botoes.create_button()
        self.btn_iniciar.clicked.connect(self.toggle_timer)
        controles.addWidget(self.btn_iniciar)

        self.btn_resetar = self.gerenciador_botoes.create_button()
        self.btn_resetar.clicked.connect(self.resetar_timer)
        controles.addWidget(self.btn_resetar)

        self.btn_resetar_ciclo = self.gerenciador_botoes.create_button()
        self.btn_resetar_ciclo.clicked.connect(self.resetar_ciclo)
        controles.addWidget(self.btn_resetar_ciclo)

        self.btn_pular = self.gerenciador_botoes.create_button()
        self.btn_pular.clicked.connect(self.pular_ciclo)
        controles.addWidget(self.btn_pular)

        layout.addLayout(controles)

        self.config_group = QGroupBox()
        config_layout = QHBoxLayout()

        self.label_foco = QLabel()
        fonte_foco = QFont("Arial", 10, QFont.Bold)
        self.label_foco.setFont(fonte_foco)
        config_layout.addWidget(self.label_foco)
        config_layout.setAlignment(self.label_foco, Qt.AlignRight)

        self.spin_foco = QComboBox()
        self.spin_foco.addItems(["1", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100", "105", "110", "115", "120"])
        self.spin_foco.setCurrentText("25")
        self.spin_foco.currentTextChanged.connect(self.atualizar_configuracoes)
        config_layout.addWidget(self.spin_foco)
        config_layout.setAlignment(self.spin_foco, Qt.AlignLeft)

        self.label_descanso = QLabel()
        fonte_descanso = QFont("Arial", 10, QFont.Bold)
        self.label_descanso.setFont(fonte_descanso)
        config_layout.addWidget(self.label_descanso)
        config_layout.setAlignment(self.label_descanso, Qt.AlignRight)

        self.spin_descanso = QComboBox()
        self.spin_descanso.addItems(["1", "3", "5", "7", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"])
        self.spin_descanso.setCurrentText("5")
        self.spin_descanso.currentTextChanged.connect(self.atualizar_configuracoes)
        config_layout.addWidget(self.spin_descanso)
        config_layout.setAlignment(self.spin_descanso, Qt.AlignLeft)

        self.label_ciclos = QLabel()
        fonte_ciclos = QFont("Arial", 10, QFont.Bold)
        self.label_ciclos.setFont(fonte_ciclos)
        config_layout.addWidget(self.label_ciclos)
        config_layout.setAlignment(self.label_ciclos, Qt.AlignRight)

        self.spin_ciclos = QComboBox()
        self.spin_ciclos.addItems([str(i) for i in range(1, 21)])
        self.spin_ciclos.setCurrentText(str(getattr(self, "ciclos_permitidos", 4)))
        self.spin_ciclos.currentTextChanged.connect(self.atualizar_configuracoes)
        config_layout.addWidget(self.spin_ciclos)
        config_layout.setAlignment(self.spin_ciclos, Qt.AlignLeft)

        self.config_group.setLayout(config_layout)
        layout.addWidget(self.config_group)

        self.setLayout(layout)
        self.atualizar_traducoes()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do PomodoroTimer: {str(e)}", exc_info=True)
