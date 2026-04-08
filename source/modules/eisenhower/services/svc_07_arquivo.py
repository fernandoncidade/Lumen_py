from PySide6.QtCore import QCoreApplication
from source.modules.eisenhower.services.Arquivo import (
    novo as _arq_novo,
    limpar_tudo as _arq_limpar_tudo,
    _parse_text_date_time as _arq_parse_text_date_time,
    abrir_arquivo as _arq_abrir_arquivo,
    salvar_como as _arq_salvar_como,
)
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class Arquivo:
    def __init__(self, app=None):
        self.app = app

    def set_app(self, app):
        self.app = app

    def _resolve_app(self, app):
        app = app or self.app
        if app is None:
            raise RuntimeError("App instance is required")
        return app

    @staticmethod
    def get_text(text):
        return QCoreApplication.translate("App", text)

    def _clear_all_lists(self, app=None):
        app = self._resolve_app(app)
        for lst in (
            app.quadrant1_list,
            app.quadrant2_list,
            app.quadrant3_list,
            app.quadrant4_list,
            app.quadrant1_completed_list,
            app.quadrant2_completed_list,
            app.quadrant3_completed_list,
            app.quadrant4_completed_list,
        ):
            lst.clear()

    def _add_placeholders_after_clear(self, app=None):
        app = self._resolve_app(app)
        app.add_placeholder(app.quadrant1_list, self.get_text("1º Quadrante"))
        app.add_placeholder(app.quadrant2_list, self.get_text("2º Quadrante"))
        app.add_placeholder(app.quadrant3_list, self.get_text("3º Quadrante"))
        app.add_placeholder(app.quadrant4_list, self.get_text("4º Quadrante"))
        app.add_placeholder(app.quadrant1_completed_list, self.get_text("Nenhuma Tarefa Concluída"))
        app.add_placeholder(app.quadrant2_completed_list, self.get_text("Nenhuma Tarefa Concluída"))
        app.add_placeholder(app.quadrant3_completed_list, self.get_text("Nenhuma Tarefa Concluída"))
        app.add_placeholder(app.quadrant4_completed_list, self.get_text("Nenhuma Tarefa Concluída"))

    def novo(self, app=None):
        return _arq_novo(self, app)

    def limpar_tudo(self, app=None):
        return _arq_limpar_tudo(self, app)

    def sair(self, app=None):
        from PySide6.QtWidgets import QApplication
        QApplication.quit()

    def _parse_text_date_time(self, raw_text: str, app=None):
        return _arq_parse_text_date_time(self, raw_text, app)

    def abrir_arquivo(self, app=None):
        return _arq_abrir_arquivo(self, app)

    def salvar_como(self, app=None):
        return _arq_salvar_como(self, app)

_arquivo_singleton = Arquivo()

def novo(app):
    return Arquivo(app).novo(app)

def limpar_tudo(app):
    return Arquivo(app).limpar_tudo(app)

def sair(app=None):
    return Arquivo(app).sair(app)

def abrir_arquivo(app):
    return Arquivo(app).abrir_arquivo(app)

def salvar_como(app):
    return Arquivo(app).salvar_como(app)
