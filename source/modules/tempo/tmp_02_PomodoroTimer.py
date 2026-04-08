from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Signal, QCoreApplication
from source.utils.LogManager import LogManager
from source.utils.GerenciadorBotoesUI import GerenciadorBotoesUI
from source.utils.SoundManager import SoundManager
from source.modules.tempo.PomodoroTimer import (
    setup_ui,
    atualizar_traducoes,
    atualizar_configuracoes,
    toggle_timer,
    atualizar_timer,
    atualizar_display,
    _executar_alerta,
    finalizar_ciclo,
    resetar_timer,
    resetar_ciclo,
    pular_ciclo,
    _aplicar_tema_dinamico,
    eventFilter
)


class PomodoroTimer(QWidget):
    ciclo_completado = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = LogManager.get_logger()
        try:
            self.tempo_foco = 25 * 60
            self.tempo_descanso_curto = 5 * 60
            self.tempo_descanso_longo = 15 * 60
            self.ciclos_permitidos = 4
            self.tempo_restante = self.tempo_foco
            self.em_foco = True
            self.ciclos_completados = 0
            self.timer_ativo = False
            self.gerenciador_botoes = GerenciadorBotoesUI(self)

            self._sound_mgr = SoundManager.instance()

            self.timer = QTimer()
            self.timer.timeout.connect(self.atualizar_timer)

            self.setup_ui()

            app = QCoreApplication.instance()
            if app:
                app.installEventFilter(self)

            self._aplicar_tema_dinamico()

        except Exception as e:
            self.logger.error(f"Erro ao inicializar PomodoroTimer: {str(e)}", exc_info=True)

    def setup_ui(self):
        return setup_ui(self)

    def atualizar_traducoes(self):
        return atualizar_traducoes(self)

    def atualizar_configuracoes(self):
        return atualizar_configuracoes(self)

    def toggle_timer(self):
        return toggle_timer(self)

    def atualizar_timer(self):
        return atualizar_timer(self)

    def atualizar_display(self):
        return atualizar_display(self)

    def _executar_alerta(self, titulo, texto):
        return _executar_alerta(self, titulo, texto)

    def finalizar_ciclo(self):
        return finalizar_ciclo(self)

    def resetar_timer(self):
        return resetar_timer(self)

    def resetar_ciclo(self):
        return resetar_ciclo(self)

    def pular_ciclo(self):
        return pular_ciclo(self)

    def _aplicar_tema_dinamico(self):
        return _aplicar_tema_dinamico(self)

    def eventFilter(self, obj, event):
        return eventFilter(self, obj, event)
