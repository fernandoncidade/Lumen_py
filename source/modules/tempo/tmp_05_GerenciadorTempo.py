from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QCoreApplication, QThread
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_06_TimeWorker import _TimeWorker
from source.modules.tempo.GerenciadorTempo import (
    setup_ui,
    _atualizar_rotulo_botao_eisenhower,
    _setup_integracao_eisenhower,
    _on_tarefa_adicionada_gestao_tempo,
    _on_event_bus_tarefa,
    _aplicar_tema_dinamico_inputs,
    eventFilter,
    atualizar_traducoes,
    registrar_pomodoro,
    cleanup,
    __del__,
    atualizar_coluna_doing_timer,
    _ajustar_largura_minima_coluna_esquerda
)


class GerenciadorTempo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = LogManager.get_logger()
        try:
            self._integracao_ids_recebidos = set()
            self._tempo_thread = QThread()
            self._tempo_worker = _TimeWorker()
            self._tempo_worker.moveToThread(self._tempo_thread)
            self._tempo_worker.pomodoro_completed.connect(self.registrar_pomodoro)
            self._tempo_thread.start()

            self.setup_ui()
            self._setup_integracao_eisenhower()

            app = QCoreApplication.instance()
            if app:
                app.installEventFilter(self)

            self._aplicar_tema_dinamico_inputs()

        except Exception as e:
            self.logger.error(f"Erro ao inicializar GerenciadorTempo: {str(e)}", exc_info=True)

    def setup_ui(self):
        setup_ui(self)

    def _atualizar_rotulo_botao_eisenhower(self) -> None:
        _atualizar_rotulo_botao_eisenhower(self)

    def _setup_integracao_eisenhower(self):
        _setup_integracao_eisenhower(self)

    def _on_tarefa_adicionada_gestao_tempo(self, dados: dict):
        _on_tarefa_adicionada_gestao_tempo(self, dados)

    def _on_event_bus_tarefa(self, dados: dict):
        _on_event_bus_tarefa(self, dados)

    def _aplicar_tema_dinamico_inputs(self):
        _aplicar_tema_dinamico_inputs(self)

    def eventFilter(self, obj, event):
        return eventFilter(self, obj, event)

    def atualizar_traducoes(self):
        atualizar_traducoes(self)

    def registrar_pomodoro(self, tipo):
        registrar_pomodoro(self, tipo)

    def cleanup(self):
        cleanup(self)

    def __del__(self):
        __del__(self)

    def atualizar_coluna_doing_timer(self):
        atualizar_coluna_doing_timer(self)

    def _ajustar_largura_minima_coluna_esquerda(self):
        _ajustar_largura_minima_coluna_esquerda(self)
