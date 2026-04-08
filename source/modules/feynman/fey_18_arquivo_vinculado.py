import os
import subprocess
import sys
from PySide6.QtCore import Qt, QCoreApplication, QUrl, QPoint, QObject, QEvent
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel
from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

PREVIEW_ROLE = Qt.UserRole + 1


class _FeynmanTooltipArquivoVinculado(QFrame):
    def __init__(self):
        super().__init__(None, Qt.ToolTip)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

    def _clear(self):
        while self._layout.count():
            child = self._layout.takeAt(0)
            widget = child.widget()

            if widget is not None:
                widget.deleteLater()

    def _add_section(self, titulo, conteudo, negrito=False):
        if not conteudo:
            return

        label_titulo = QLabel(f"{titulo}:")
        label_titulo.setWordWrap(True)

        if negrito:
            fonte = label_titulo.font()
            fonte.setBold(True)
            label_titulo.setFont(fonte)

        label_conteudo = QLabel(conteudo)
        label_conteudo.setWordWrap(True)
        self._layout.addWidget(label_titulo)
        self._layout.addWidget(label_conteudo)

    def configurar(self, secoes):
        self._clear()
        primeira = True

        for secao in secoes:
            titulo = secao.get("titulo")
            conteudo = secao.get("conteudo")
            negrito = secao.get("negrito", False)

            if not conteudo:
                continue

            if not primeira:
                separador = QFrame()
                separador.setFrameShape(QFrame.HLine)
                separador.setFrameShadow(QFrame.Sunken)
                self._layout.addWidget(separador)

            self._add_section(titulo, conteudo, negrito=negrito)
            primeira = False


class _ListaConceitosHoverFilter(QObject):
    def __init__(self, owner):
        super().__init__(owner)
        self._owner = owner

    def eventFilter(self, obj, event):
        try:
            et = event.type()

            if et in (QEvent.Leave, QEvent.FocusOut, QEvent.Hide, QEvent.Wheel, QEvent.Resize):
                self._owner.ocultar_tooltip_arquivo_vinculado()

            if et == QEvent.MouseMove:
                item = self._owner.lista_conceitos.itemAt(event.pos())

                if item is None:
                    self._owner.ocultar_tooltip_arquivo_vinculado()

        except Exception:
            pass

        return super().eventFilter(obj, event)


def _obter_conceito_do_item(self, item):
    try:
        if item is None:
            return None

        try:
            conceito = item.data(Qt.UserRole)

            if isinstance(conceito, dict):
                return conceito

        except Exception:
            pass

        titulo = item.text().replace('🔴 ', '').replace('🟡 ', '').replace('🟢 ', '').strip()
        return next((c for c in self.conceitos if c.get('titulo') == titulo), None)

    except Exception:
        return None

def abrir_arquivo_conceito(self, item):
    try:
        conceito = _obter_conceito_do_item(self, item)

        if not conceito:
            return

        caminho = (conceito.get('arquivo_vinculado') or '').strip()

        if not caminho:
            return

        if not os.path.exists(caminho):
            MessageBox.feynman_linked_file_not_found(self, caminho)
            return

        try:
            if QDesktopServices.openUrl(QUrl.fromLocalFile(caminho)):
                return

        except Exception:
            pass

        try:
            if sys.platform.startswith("win"):
                os.startfile(caminho)
                return

            if sys.platform.startswith("darwin"):
                subprocess.Popen(["open", caminho])
                return

            subprocess.Popen(["xdg-open", caminho])

        except Exception as e:
            logger.error(f"Erro ao abrir arquivo vinculado no Método Feynman: {e}", exc_info=True)
            MessageBox.feynman_linked_file_open_error(self)

    except Exception as e:
        logger.error(f"Erro ao abrir arquivo do conceito no Método Feynman: {e}", exc_info=True)

def on_lista_conceitos_double_click(self, item):
    try:
        self.abrir_arquivo_conceito(item)

    except Exception as e:
        logger.error(f"Erro ao processar duplo clique na lista de conceitos: {e}", exc_info=True)


def mostrar_tooltip_arquivo_vinculado(self, item):
    try:
        if item is None:
            self.ocultar_tooltip_arquivo_vinculado()
            return

        preview = item.data(PREVIEW_ROLE)

        if not isinstance(preview, dict):
            self.ocultar_tooltip_arquivo_vinculado()
            return

        secoes = [
            {
                "titulo": QCoreApplication.translate("App", "1️⃣ Conceito"),
                "conteudo": preview.get("conceito", "")
            },
            {
                "titulo": QCoreApplication.translate("App", "2️⃣ Explique"),
                "conteudo": preview.get("explique", "")
            },
            {
                "titulo": QCoreApplication.translate("App", "3️⃣ Lacunas"),
                "conteudo": preview.get("lacunas", "")
            },
            {
                "titulo": QCoreApplication.translate("App", "4️⃣ Revisão"),
                "conteudo": preview.get("revisao", "")
            },
            {
                "titulo": QCoreApplication.translate("App", "📎 Arquivo Vinculado"),
                "conteudo": preview.get("arquivo_vinculado", ""),
                "negrito": True
            },
        ]

        if not hasattr(self, "_feynman_tooltip_widget") or self._feynman_tooltip_widget is None:
            self._feynman_tooltip_widget = _FeynmanTooltipArquivoVinculado()

        self._feynman_tooltip_widget.configurar(secoes)
        self._feynman_tooltip_widget.adjustSize()
        pos = QApplication.instance().cursor().pos() + QPoint(14, 18)

        screen = QApplication.screenAt(pos) or QApplication.primaryScreen()

        if screen is not None:
            geo = screen.availableGeometry()
            w = self._feynman_tooltip_widget.width()
            h = self._feynman_tooltip_widget.height()
            x = min(pos.x(), geo.right() - w)
            y = min(pos.y(), geo.bottom() - h)
            x = max(x, geo.left())
            y = max(y, geo.top())
            pos = QPoint(x, y)

        self._feynman_tooltip_widget.move(pos)
        self._feynman_tooltip_widget.show()

    except Exception as e:
        logger.error(f"Erro ao mostrar tooltip de arquivo vinculado: {e}", exc_info=True)


def ocultar_tooltip_arquivo_vinculado(self):
    try:
        tooltip = getattr(self, "_feynman_tooltip_widget", None)

        if tooltip is not None:
            tooltip.hide()

    except Exception as e:
        logger.error(f"Erro ao ocultar tooltip de arquivo vinculado: {e}", exc_info=True)


def configurar_tooltip_arquivo_vinculado(self):
    try:
        self.lista_conceitos.setMouseTracking(True)
        self.lista_conceitos.viewport().setMouseTracking(True)
        self.lista_conceitos.itemEntered.connect(self.mostrar_tooltip_arquivo_vinculado)

        self._feynman_hover_filter = _ListaConceitosHoverFilter(self)
        self.lista_conceitos.viewport().installEventFilter(self._feynman_hover_filter)

    except Exception as e:
        logger.error(f"Erro ao configurar tooltip de arquivo vinculado: {e}", exc_info=True)
