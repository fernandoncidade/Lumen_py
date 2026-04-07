from PySide6.QtWidgets import QWidget, QComboBox
from PySide6.QtCore import Signal, QCoreApplication
import os
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.modules.tempo.GerenciadorTarefas import (
    carregar_tarefas,
    salvar_tarefas,
    setup_ui,
    atualizar_traducoes,
    criar_coluna,
    _on_drop_sincronizar,
    _on_rows_moved,
    _sincronizar_status_pos_movimento,
    adicionar_tarefa,
    _adicionar_tarefa_interna,
    adicionar_tarefa_externa,
    mover_tarefa,
    atualizar_listas,
    mostrar_menu_contexto,
    _ha_tarefas_marcadas,
    remover_tarefa_por_item,
    remover_tarefas_marcadas,
    resetar_contagem_botao,
    mover_tarefas_marcadas,
    mover_tarefa_por_item,
    _ajustar_largura_combo,
    _aplicar_tema_dinamico_inputs,
    eventFilter,
    _update_rounded_mask
)


class GerenciadorTarefas(QWidget):
    listas_atualizadas = Signal()
    tarefa_adicionada = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = LogManager.get_logger()
        try:
            caminho_persistente = obter_caminho_persistente()
            self.arquivo_tarefas = os.path.join(caminho_persistente, "tarefas.json")
            self.tarefas = self.carregar_tarefas()
            self.setup_ui()

            app = QCoreApplication.instance()
            if app:
                app.installEventFilter(self)

                try:
                    if hasattr(app, 'gerenciador_traducao') and app.gerenciador_traducao is not None:
                        try:
                            app.gerenciador_traducao.idioma_alterado.connect(self.atualizar_traducoes)

                        except Exception:
                            pass

                except Exception:
                    pass

            self._aplicar_tema_dinamico_inputs()

        except Exception as e:
            self.logger.error(f"Erro ao inicializar GerenciadorTarefas: {str(e)}", exc_info=True)

    def carregar_tarefas(self):
        return carregar_tarefas(self)

    def salvar_tarefas(self):
        return salvar_tarefas(self)

    def setup_ui(self):
        return setup_ui(self)

    def atualizar_traducoes(self):
        return atualizar_traducoes(self)

    def criar_coluna(self, status):
        return criar_coluna(self, status)

    def _on_drop_sincronizar(self):
        return _on_drop_sincronizar(self)

    def _on_rows_moved(self, lista):
        return _on_rows_moved(self, lista)

    def _sincronizar_status_pos_movimento(self, prioridade_lista=None):
        return _sincronizar_status_pos_movimento(self, prioridade_lista)

    def adicionar_tarefa(self):
        return adicionar_tarefa(self)

    def _adicionar_tarefa_interna(self, titulo: str, prioridade: str, status: str = "Todo", emitir_sinal: bool = True, description: str = None, file_path: str = None, date: str = None, time: str = None):
        return _adicionar_tarefa_interna(self, titulo, prioridade, status, emitir_sinal, description, file_path, date, time)

    def adicionar_tarefa_externa(self, titulo: str, prioridade: str = "Importante e Urgente", description: str = None, file_path: str = None, date: str = None, time: str = None) -> None:
        return adicionar_tarefa_externa(self, titulo, prioridade, description, file_path, date, time)

    def mover_tarefa(self, item, status_atual):
        return mover_tarefa(self, item, status_atual)

    def atualizar_listas(self):
        return atualizar_listas(self)

    def mostrar_menu_contexto(self, pos, lista):
        return mostrar_menu_contexto(self, pos, lista)

    def _ha_tarefas_marcadas(self):
        return _ha_tarefas_marcadas(self)

    def remover_tarefa_por_item(self, item):
        return remover_tarefa_por_item(self, item)

    def remover_tarefas_marcadas(self):
        return remover_tarefas_marcadas(self)

    def resetar_contagem_botao(self):
        return resetar_contagem_botao(self)

    def mover_tarefas_marcadas(self):
        return mover_tarefas_marcadas(self)

    def mover_tarefa_por_item(self, item):
        return mover_tarefa_por_item(self, item)

    def _ajustar_largura_combo(self, combo: QComboBox, padding_extra: int = 42, max_visiveis: int = 6):
        return _ajustar_largura_combo(self, combo, padding_extra, max_visiveis)

    def _aplicar_tema_dinamico_inputs(self):
        return _aplicar_tema_dinamico_inputs(self)

    def eventFilter(self, obj, event):
        return eventFilter(self, obj, event)

    def _update_rounded_mask(self, widget, radius: int = 8):
        return _update_rounded_mask(self, widget, radius)
