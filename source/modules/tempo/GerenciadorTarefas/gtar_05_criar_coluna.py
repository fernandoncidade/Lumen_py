from PySide6.QtWidgets import QVBoxLayout, QListWidget, QGroupBox
from PySide6.QtCore import Qt
from source.modules.tempo.tmp_04_KanbanListWidget import _KanbanListWidget
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def criar_coluna(self, status):
    try:
        grupo = QGroupBox()
        layout = QVBoxLayout()

        lista = _KanbanListWidget()
        lista.setDragEnabled(True)
        lista.setAcceptDrops(True)
        lista.setDropIndicatorShown(True)
        lista.setDefaultDropAction(Qt.MoveAction)
        lista.setDragDropMode(QListWidget.DragDrop)

        lista.tarefas_soltadas.connect(self._on_drop_sincronizar)
        lista.itemDoubleClicked.connect(lambda item: self.mover_tarefa(item, status))

        lista.setContextMenuPolicy(Qt.CustomContextMenu)
        lista.customContextMenuRequested.connect(lambda pos, l=lista: self.mostrar_menu_contexto(pos, l))

        try:
            model = lista.model()
            model.rowsMoved.connect(lambda *args, l=lista: self._on_rows_moved(l))

        except Exception:
            pass

        layout.addWidget(lista)
        grupo.setLayout(layout)

        grupo.lista = lista
        grupo.status = status

        try:
            radius = 10
            grupo._rounded_radius = radius
            self._update_rounded_mask(grupo, radius)

            try:
                self._update_rounded_mask(grupo.lista, max(0, radius - 2))
                vp = getattr(grupo.lista, "viewport", None)
                if callable(vp):
                    self._update_rounded_mask(grupo.lista.viewport(), max(0, radius - 2))

            except Exception:
                pass

        except Exception:
            pass

        return grupo

    except Exception as e:
        logger.error(f"Erro ao criar coluna '{status}': {str(e)}", exc_info=True)
        return QGroupBox()
