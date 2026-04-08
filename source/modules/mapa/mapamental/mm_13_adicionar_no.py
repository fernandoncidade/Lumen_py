import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QDialogButtonBox
from PySide6.QtCore import QCoreApplication, QPointF
from source.utils.LogManager import LogManager
from source.modules.mapa.mp_01_NoConceito import NoConceito
from source.modules.mapa.mp_03_MapaMental import MapaScene
logger = LogManager.get_logger()


class _DropLineEdit(QLineEdit):
    def __init__(self, owner_dialog):
        super().__init__(owner_dialog)
        self._owner_dialog = owner_dialog
        self.setAcceptDrops(True)
        self.setPlaceholderText(QCoreApplication.translate("App", "Arraste um arquivo aqui para vincular (opcional)"))

    def dragEnterEvent(self, event):
        try:
            md = event.mimeData()

            if md.hasUrls():
                event.acceptProposedAction()

            else:
                super().dragEnterEvent(event)

        except Exception:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        try:
            md = event.mimeData()

            if md.hasUrls():
                event.acceptProposedAction()

            else:
                super().dragMoveEvent(event)

        except Exception:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        try:
            md = event.mimeData()

            if md.hasUrls():
                urls = md.urls()

                if urls:
                    path = urls[0].toLocalFile()

                    if path and os.path.isfile(path):
                        self._owner_dialog._on_file_dropped(path)
                        event.acceptProposedAction()
                        return

        except Exception:
            pass

        super().dropEvent(event)


class _AdicionarNoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._linked_path = None
        self.setWindowTitle(QCoreApplication.translate("App", "Novo Conceito"))

        layout = QVBoxLayout()

        label = QLabel(
            QCoreApplication.translate("App", "Digite o conceito:\nEx: 'Tensão de Cisalhamento', 'Momento Fletor'"))

        layout.addWidget(label)

        self.input_texto = _DropLineEdit(self)
        layout.addWidget(self.input_texto)

        self.drop_info = QLabel(QCoreApplication.translate("App", "Solte um arquivo no campo acima para vincular (opcional)"))
        layout.addWidget(self.drop_info)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)

        self.setLayout(layout)

    def _on_file_dropped(self, path: str):
        try:
            titulo = os.path.splitext(os.path.basename(path))[0]
            if titulo:
                self.input_texto.setText(titulo)

            resp = QMessageBox.question(
                self,
                QCoreApplication.translate("App", "Vincular arquivo"),
                QCoreApplication.translate("App", "Deseja vincular este arquivo ao nó que será criado?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )

            if resp == QMessageBox.StandardButton.Yes:
                self._linked_path = path
                self.drop_info.setText(QCoreApplication.translate("App", "Arquivo vinculado:") + f" {os.path.basename(path)}")

            else:
                self._linked_path = None
                self.drop_info.setText(QCoreApplication.translate("App", "Arquivo não vinculado."))

        except Exception as e:
            logger.debug(f"Erro ao processar arquivo soltado: {e}", exc_info=True)

    def get_texto(self) -> str:
        return self.input_texto.text().strip()

    def get_linked_path(self) -> str | None:
        return self._linked_path

def adicionar_no(self):
    try:
        dialogo = _AdicionarNoDialog(self)
        if dialogo.exec() != QDialog.Accepted:
            return

        texto = dialogo.get_texto()
        if texto:
            if self.nos:
                ultimo = self.nos[-1]
                x = ultimo.scenePos().x() + 150
                y = ultimo.scenePos().y()

            else:
                x, y = 0, 0

            no = NoConceito(x, y, texto)
            if isinstance(self.scene, MapaScene):
                pos = self.scene.snap(QPointF(x, y))
                no.setPos(pos)

            try:
                caminho = dialogo.get_linked_path()
                if caminho:
                    no.set_arquivo_vinculado(caminho)

            except Exception:
                pass

            self.scene.addItem(no)
            self.nos.append(no)
            self._expandir_area_se_necessario(no)

            try:
                if getattr(self, "_modo_navegacao_hierarquia", False):
                    parent_map = getattr(self, "_hierarquia_parent", None) or {}
                    children_map = getattr(self, "_hierarquia_children", None) or {}

                    parent = None
                    try:
                        selecionados = [
                            item for item in self.scene.selectedItems()
                            if isinstance(item, NoConceito) and item is not no
                        ]
                        if selecionados:
                            parent = selecionados[0]

                    except Exception:
                        parent = None

                    if parent is None:
                        parent = getattr(self, "_hierarquia_root", None)

                    if parent is None:
                        self._hierarquia_root = no
                        parent_map[no] = None
                        children_map.setdefault(no, [])

                    else:
                        parent_map[no] = parent
                        filhos = children_map.setdefault(parent, [])
                        if no not in filhos:
                            filhos.append(no)

                        children_map.setdefault(no, [])

                        try:
                            self._nos_expandidos.add(parent)

                        except Exception:
                            pass

                    self._hierarquia_parent = parent_map
                    self._hierarquia_children = children_map

                    if hasattr(self, "_instalar_handlers_nos"):
                        self._instalar_handlers_nos()

                    if hasattr(self, "_aplicar_visibilidade_por_foco"):
                        self._aplicar_visibilidade_por_foco(parent or no, abrir_foco=True)

                    if hasattr(self, "_atualizar_visibilidade_linhas"):
                        self._atualizar_visibilidade_linhas()

            except Exception:
                pass

            if hasattr(self.view, "animate_focus_on"):
                self.view.animate_focus_on(no)

    except Exception as e:
        logger.error(f"Erro ao adicionar nó: {str(e)}", exc_info=True)
