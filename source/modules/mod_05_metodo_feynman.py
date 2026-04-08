from PySide6.QtWidgets import QWidget
from source.utils.LogManager import LogManager
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.utils.GerenciadorBotoesUI import GerenciadorBotoesUI
from source.utils.EventBus import get_event_bus
import os
from source.modules.feynman import (FeynmanWorker, carregar_conceitos, setup_ui, atualizar_traducoes, 
                                    novo_conceito, limpar_campos, salvar_conceito_atual, 
                                    selecionar_conceito, deletar_conceito, atualizar_lista, 
                                    salvar_conceitos, mostrar_menu_contexto, redefinir_dominio,
                                    receber_conceito_mapa_mental, _on_conceitos_loaded, 
                                    _stop_feynman_thread, cleanup, abrir_arquivo_conceito,
                                    vincular_arquivo_conceito, remover_arquivo_vinculado,
                                    on_lista_conceitos_double_click)


class MetodoFeynman(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = LogManager.get_logger()
        try:
            caminho_persistente = obter_caminho_persistente()
            self.arquivo_conceitos = os.path.join(caminho_persistente, "conceitos_feynman.json")
            self.conceitos = carregar_conceitos(self)
            self.gerenciador_botoes = GerenciadorBotoesUI(self)
            setup_ui(self)

            from PySide6.QtCore import QThread, QCoreApplication

            self.event_bus = get_event_bus()
            self.event_bus.conceito_atualizado.connect(self.receber_conceito_mapa_mental)

            try:
                self.event_bus.drain_pending_conceitos()

            except Exception:
                pass

            self.logger.info("MetodoFeynman conectado ao EventBus")

        except Exception as e:
            self.logger.error(f"Erro ao inicializar MetodoFeynman: {str(e)}", exc_info=True)

        try:
            self._feynman_thread = QThread()
            self._feynman_worker = FeynmanWorker()
            self._feynman_worker.moveToThread(self._feynman_thread)
            self._feynman_worker.conceitos_loaded.connect(self._on_conceitos_loaded)
            self._feynman_worker.save_finished.connect(lambda ok: None)
            self._feynman_worker.error.connect(lambda e: self.logger.error(f"Worker error (Feynman): {e}"))
            self._feynman_thread.start()

            def _carregar_conceitos_via_worker():
                try:
                    arquivo = getattr(self, 'arquivo_conceitos', None)
                    self._feynman_worker.request_load.emit(arquivo)

                except Exception as e:
                    self.logger.error(f"Erro ao solicitar carregamento de conceitos: {e}", exc_info=True)

            def _salvar_conceitos_via_worker():
                try:
                    arquivo = getattr(self, 'arquivo_conceitos', None)
                    self._feynman_worker.request_save.emit(arquivo, getattr(self, 'conceitos', []))

                except Exception as e:
                    self.logger.error(f"Erro ao solicitar salvamento de conceitos: {e}", exc_info=True)

            self.carregar_conceitos = _carregar_conceitos_via_worker
            self.salvar_conceitos = _salvar_conceitos_via_worker

            try:
                app = QCoreApplication.instance()
                if app is not None:
                    app.aboutToQuit.connect(self._stop_feynman_thread)

            except Exception:
                pass

        except Exception as e:
            self.logger.error(f"Erro ao iniciar thread do Método Feynman: {e}", exc_info=True)

    def receber_conceito_mapa_mental(self, dados: dict):
        receber_conceito_mapa_mental(self, dados)

    def atualizar_traducoes(self):
        atualizar_traducoes(self)

    def novo_conceito(self):
        novo_conceito(self)

    def limpar_campos(self):
        limpar_campos(self)

    def salvar_conceito_atual(self):
        salvar_conceito_atual(self)

    def selecionar_conceito(self, item):
        selecionar_conceito(self, item)

    def deletar_conceito(self):
        deletar_conceito(self)

    def atualizar_lista(self):
        atualizar_lista(self)

    def salvar_conceitos(self):
        salvar_conceitos(self)

    def mostrar_menu_contexto(self, position):
        mostrar_menu_contexto(self, position)

    def redefinir_dominio(self, item, novo_nivel):
        redefinir_dominio(self, item, novo_nivel)

    def vincular_arquivo_conceito(self, item):
        vincular_arquivo_conceito(self, item)

    def remover_arquivo_vinculado(self, item):
        remover_arquivo_vinculado(self, item)

    def _on_conceitos_loaded(self, conceitos):
        _on_conceitos_loaded(self, conceitos)

    def _stop_feynman_thread(self):
        _stop_feynman_thread(self)

    def cleanup(self):
        cleanup(self)

    def abrir_arquivo_conceito(self, item):
        abrir_arquivo_conceito(self, item)

    def on_lista_conceitos_double_click(self, item):
        on_lista_conceitos_double_click(self, item)
