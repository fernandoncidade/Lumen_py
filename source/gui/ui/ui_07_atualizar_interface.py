from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_interface(self, codigo_idioma):
    try:
        self.setWindowTitle(QCoreApplication.translate("App", "Lúmen"))
        if not hasattr(self, 'tabs'):
            return

        titles = {
            "leitor": QCoreApplication.translate("App", "📖 Leitor Acessível"),
            "gerenciador": QCoreApplication.translate("App", "⏱️ Gestão de Tempo"),
            "mapa": QCoreApplication.translate("App", "🧠 Mapas Mentais"),
            "feynman": QCoreApplication.translate("App", "🎓 Método Feynman"),
            "eisenhower": QCoreApplication.translate("App", "🗂️ Matriz Eisenhower"),
        }

        for i in range(self.tabs.count()):
            key = self.tabs.tabBar().tabData(i)
            if key in titles:
                self.tabs.setTabText(i, titles[key])

        self.atualizar_menu()

        if hasattr(self, 'status_bar'):
            tab_name = self.tabs.tabText(self.tabs.currentIndex())
            self.status_bar.showMessage(QCoreApplication.translate("App", "Módulo ativo: {tab_name}").format(tab_name=tab_name))

        if hasattr(self, 'menu_sobre'):
            self.menu_sobre.setTitle(QCoreApplication.translate("App", "ℹ️ Sobre"))

        if hasattr(self, 'action_sobre_app'):
            self.action_sobre_app.setText(QCoreApplication.translate("App", "ℹ️ Sobre o Aplicativo"))

    except Exception as e:
        logger.error(f"Erro ao atualizar interface: {str(e)}", exc_info=True)
