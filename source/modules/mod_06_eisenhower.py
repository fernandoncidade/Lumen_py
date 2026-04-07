import os
from PySide6.QtCore import QCoreApplication, QThread
from PySide6.QtWidgets import QWidget
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao
from source.modules.eisenhower import (
    _EisenhowerWorker,
    initUI,
    _hide_legacy_calendar_button,
    _is_group_header,
    _time_group_label,
    _time_key,
    insert_task_into_quadrant_list,
    cleanup_time_groups,
    add_task_add,
    _setup_integracao_gestao_tempo,
    _on_event_bus_tarefa,
    _lista_por_prioridade,
    _adicionar_tarefa_integrada_do_tempo,
    _stop_eisenhower_thread,
    cleanup,
    remove_task_remove,
    save_tasks_save,
    load_tasks_load,
    atualizar_textos_atualizar,
    open_calendar,
    handle_item_checked,
    move_item_between_lists,
    add_placeholder,
    definir_idioma,
    atualizar_placeholders,
    show_context_menu,
    novo,
    limpar_tudo,
    sair,
    abrir_arquivo,
    salvar_como
)
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class EisenhowerMatrixApp(QWidget):
    def __init__(self, gerenciador_traducao=None, embedded=True):
        super().__init__()
        self.embedded = embedded
        if gerenciador_traducao is not None:
            self.gerenciador_traducao = gerenciador_traducao
            self.gerenciador_traducao.idioma_alterado.connect(self.atualizar_textos)

        else:
            self.gerenciador_traducao = GerenciadorTraducao()
            self.gerenciador_traducao.idioma_alterado.connect(self.atualizar_textos)
            self.gerenciador_traducao.aplicar_traducao()

        self.tasks_path = os.path.join(obter_caminho_persistente(), "tasks.json")

        self.initUI()
        self.load_tasks()
        self._integracao_ids_recebidos = set()
        self._setup_integracao_gestao_tempo()

        try:
            self._eisenhower_thread = QThread()
            self._eisenhower_worker = _EisenhowerWorker()
            self._eisenhower_worker.moveToThread(self._eisenhower_thread)
            self._eisenhower_worker.error.connect(lambda e: logger.error(f"Worker error (Eisenhower): {e}"))
            self._eisenhower_thread.start()

            try:
                app = QCoreApplication.instance()
                if app is not None:
                    app.aboutToQuit.connect(self._stop_eisenhower_thread)

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao iniciar thread do Eisenhower: {e}", exc_info=True)

        if not self.embedded:
            self.criar_menu_configuracoes()

    def criar_menu_configuracoes(self):
        return

    def definir_idioma(self, codigo_idioma):
        definir_idioma(self, codigo_idioma)

    def initUI(self):
        initUI(self)

    def _hide_legacy_calendar_button(self):
        _hide_legacy_calendar_button(self)

    def add_placeholder(self, list_widget, text):
        add_placeholder(self, list_widget, text)

    def _is_group_header(self, item):
        return _is_group_header(self, item)

    def _time_group_label(self, time_str: str) -> str:
        return _time_group_label(self, time_str)

    def _time_key(self, time_str: str):
        return _time_key(self, time_str)

    def insert_task_into_quadrant_list(self, lst, item):
        insert_task_into_quadrant_list(self, lst, item)

    def cleanup_time_groups(self, lst):
        cleanup_time_groups(self, lst)

    def add_task(self):
        add_task_add(self)

    def _setup_integracao_gestao_tempo(self):
        _setup_integracao_gestao_tempo(self)

    def _on_event_bus_tarefa(self, dados: dict):
        _on_event_bus_tarefa(self, dados)

    def _lista_por_prioridade(self, prioridade: str):
        return _lista_por_prioridade(self, prioridade)

    def _adicionar_tarefa_integrada_do_tempo(self, titulo: str, prioridade: str):
        _adicionar_tarefa_integrada_do_tempo(self, titulo, prioridade)

    def handle_item_checked(self, item, source_list, target_list):
        handle_item_checked(self, item, source_list, target_list)

    def move_item_between_lists(self, item, source, target, new_check_state):
        move_item_between_lists(self, item, source, target, new_check_state)

    def remove_task(self, item, list_widget, confirm: bool = True):
        remove_task_remove(self, item, list_widget, confirm)

    def save_tasks(self):
        save_tasks_save(self)

    def load_tasks(self):
        load_tasks_load(self)

    def atualizar_textos(self):
        atualizar_textos_atualizar(self)

    def atualizar_placeholders(self):
        atualizar_placeholders(self)

    def exibir_sobre(self):
        try:
            from source.modules.mod_07_exibir_public import exibir_sobre as _exibir_sobre
            _exibir_sobre(self)

        except Exception as e:
            logger.error(f"Erro ao exibir sobre: {e}", exc_info=True)

    def show_context_menu(self, point, list_widget):
        show_context_menu(self, point, list_widget)

    def open_calendar(self):
        open_calendar(self)

    def nova_sessao(self):
        novo(self)

    def abrir_arquivo(self):
        abrir_arquivo(self)

    def salvar_como(self):
        salvar_como(self)

    def limpar_tudo(self):
        limpar_tudo(self)

    def sair_app(self):
        sair(self)

    def _stop_eisenhower_thread(self):
        _stop_eisenhower_thread(self)

    def cleanup(self):
        cleanup(self)
