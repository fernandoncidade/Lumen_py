from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QGroupBox, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from source.utils.LogManager import LogManager
from source.utils.IconUtils import get_icon_path
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
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(self.label_status)

        controles = QHBoxLayout()

        self.btn_iniciar = self.gerenciador_botoes.create_button()
        self.btn_iniciar.setIcon(QIcon(get_icon_path("play")))
        self.btn_iniciar.clicked.connect(self.toggle_timer)
        controles.addWidget(self.btn_iniciar)

        self.btn_resetar = self.gerenciador_botoes.create_button()
        self.btn_resetar.setIcon(QIcon(get_icon_path("reset")))
        self.btn_resetar.clicked.connect(self.resetar_timer)
        controles.addWidget(self.btn_resetar)

        self.btn_resetar_ciclo = self.gerenciador_botoes.create_button()
        self.btn_resetar_ciclo.setIcon(QIcon(get_icon_path("reset")))
        self.btn_resetar_ciclo.clicked.connect(self.resetar_ciclo)
        controles.addWidget(self.btn_resetar_ciclo)

        self.btn_pular = self.gerenciador_botoes.create_button()
        self.btn_pular.setIcon(QIcon(get_icon_path("skip")))
        self.btn_pular.clicked.connect(self.pular_ciclo)
        controles.addWidget(self.btn_pular)

        layout.addLayout(controles)

        self.config_group = QGroupBox()
        config_layout = QHBoxLayout()

        self.label_foco = QLabel()
        config_layout.addWidget(self.label_foco)

        self.spin_foco = QComboBox()
        self.spin_foco.addItems(["1", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"])
        self.spin_foco.setCurrentText("25")
        self.spin_foco.currentTextChanged.connect(self.atualizar_configuracoes)
        config_layout.addWidget(self.spin_foco)

        self.label_descanso = QLabel()
        config_layout.addWidget(self.label_descanso)

        self.spin_descanso = QComboBox()
        self.spin_descanso.addItems(["1", "3", "5", "7", "10", "15", "20", "25", "30"])
        self.spin_descanso.setCurrentText("5")
        self.spin_descanso.currentTextChanged.connect(self.atualizar_configuracoes)
        config_layout.addWidget(self.spin_descanso)

        self.config_group.setLayout(config_layout)
        layout.addWidget(self.config_group)

        self.setLayout(layout)
        self.atualizar_traducoes()

    except Exception as e:
        logger.error(f"Erro ao configurar interface do PomodoroTimer: {str(e)}", exc_info=True)
