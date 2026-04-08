from PySide6.QtWidgets import QVBoxLayout, QListWidget, QGroupBox, QAbstractItemView
from PySide6.QtCore import Qt
from source.modules.tempo.tmp_04_KanbanListWidget import _KanbanListWidget
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
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
        lista.setSelectionMode(QAbstractItemView.ExtendedSelection)
        lista.setSelectionBehavior(QAbstractItemView.SelectItems)

        try:
            lista.setSelectionRectVisible(True)

        except Exception:
            pass

        lista.tarefas_soltadas.connect(self._on_drop_sincronizar)

        def _open_linked_file(item):
            try:
                if item is None:
                    return

                tarefa_id = item.data(Qt.UserRole)
                alvo = None

                for t in getattr(self, 'tarefas', []):
                    if getattr(t, 'id', None) == tarefa_id:
                        alvo = t
                        break

                if not alvo:
                    titulo_item = (item.text() or "").split('\n')[0]
                    titulo_item = titulo_item.replace('🔴 ', '').replace('🟠 ', '').replace('🟡 ', '').replace('🟢 ', '').strip()

                    for t in getattr(self, 'tarefas', []):
                        if getattr(t, 'titulo', '').strip() == titulo_item:
                            alvo = t
                            break

                if not alvo:
                    return

                path = getattr(alvo, 'file_path', None)

                if not path:
                    return

                import os, subprocess

                if os.path.exists(path):
                    try:
                        if os.name == 'nt':
                            os.startfile(path)

                        else:
                            subprocess.Popen(["xdg-open", path])

                    except Exception as e:
                        logger.error(f"Erro ao abrir arquivo vinculado (Gestão de Tempo): {str(e)}", exc_info=True)

                        try:
                            subprocess.Popen([path], shell=True)

                        except Exception as e2:
                            logger.error(f"Erro ao abrir arquivo vinculado (Gestão de Tempo): {str(e2)}", exc_info=True)

                else:
                    MessageBox.warning_file_not_found(self)

            except Exception as e:
                logger.error(f"Erro ao abrir arquivo vinculado (Gestão de Tempo): {str(e)}", exc_info=True)

        lista.itemDoubleClicked.connect(lambda item: _open_linked_file(item))
        lista.setContextMenuPolicy(Qt.CustomContextMenu)
        lista.customContextMenuRequested.connect(lambda pos, l=lista: self.mostrar_menu_contexto(pos, l))

        try:
            model = lista.model()
            model.rowsMoved.connect(lambda *args, l=lista: self._on_rows_moved(l))

        except Exception as e:
            logger.error(f"Erro ao conectar rowsMoved: {str(e)}", exc_info=True)

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

            except Exception as e:
                logger.error(f"Erro ao atualizar máscara arredondada da viewport: {str(e)}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao atualizar máscara arredondada do grupo: {str(e)}", exc_info=True)

        return grupo

    except Exception as e:
        logger.error(f"Erro ao criar coluna '{status}': {str(e)}", exc_info=True)
        return QGroupBox()
