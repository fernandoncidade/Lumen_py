from PySide6.QtCore import Qt, QCoreApplication, QRect, QItemSelectionModel
from PySide6.QtWidgets import QListWidget, QRubberBand
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class DragDropTaskList(QListWidget):
    def __init__(self, app, is_completed_list: bool, parent=None):
        super().__init__(parent)
        self._app = app
        self._is_completed_list = bool(is_completed_list)
        self._rubber_band = QRubberBand(QRubberBand.Rectangle, self.viewport())
        self._rubber_origin = None
        self._rubber_active = False

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QListWidget.DragDrop)

        try:
            from PySide6.QtWidgets import QAbstractItemView
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.setSelectionBehavior(QAbstractItemView.SelectItems)

        except Exception:
            pass

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                try:
                    pos = event.position().toPoint()

                except Exception:
                    pos = event.pos()

                it = self.itemAt(pos)
                if it is None:
                    if not (event.modifiers() & Qt.ControlModifier):
                        self._rubber_origin = pos
                        self._rubber_active = True
                        self._rubber_band.setGeometry(QRect(self._rubber_origin, self._rubber_origin))
                        self._rubber_band.show()

                        try:
                            self.clearSelection()

                        except Exception:
                            pass

                        event.accept()
                        return

                if it and (it.flags() & Qt.ItemIsSelectable):
                    if event.modifiers() & Qt.ControlModifier:
                        return super().mousePressEvent(event)

                    if it.isSelected():
                        prev_selected = list(self.selectedItems() or [])
                        result = super().mousePressEvent(event)

                        try:
                            for pit in prev_selected:
                                if pit:
                                    pit.setSelected(True)

                            self.setCurrentItem(it)

                        except Exception:
                            pass

                        return result

                    return super().mousePressEvent(event)

            if event.button() == Qt.RightButton:
                it = self.itemAt(event.pos())
                if it and (it.flags() & Qt.ItemIsSelectable):
                    if it.isSelected():
                        event.accept()
                        return

                    try:
                        self.clearSelection()
                        it.setSelected(True)
                        self.setCurrentItem(it)
                        event.accept()
                        return

                    except Exception:
                        pass

        except Exception:
            pass

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if getattr(self, "_rubber_active", False):
            try:
                try:
                    pos = event.position().toPoint()

                except Exception:
                    pos = event.pos()

                rect = QRect(self._rubber_origin, pos).normalized()
                self._rubber_band.setGeometry(rect)
                self._update_rubber_band_selection(rect)
                event.accept()
                return

            except Exception:
                pass

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if getattr(self, "_rubber_active", False):
            try:
                self._rubber_band.hide()

            except Exception:
                pass

            self._rubber_active = False
            self._rubber_origin = None
            event.accept()
            return

        return super().mouseReleaseEvent(event)

    def _update_rubber_band_selection(self, rect: QRect):
        try:
            sel_model = self.selectionModel()
            if sel_model is None:
                return

            sel_model.clearSelection()

            for i in range(self.count()):
                it = self.item(i)
                if not it or not (it.flags() & Qt.ItemIsSelectable):
                    continue

                idx = self.indexFromItem(it)
                if not idx.isValid():
                    continue

                vr = self.visualRect(idx)
                if rect.intersects(vr):
                    sel_model.select(idx, QItemSelectionModel.Select)

        except Exception:
            pass

    def dragEnterEvent(self, event):
        try:
            event.acceptProposedAction()

        except Exception:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        try:
            event.acceptProposedAction()

        except Exception:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        try:
            source = event.source()

            if source is self:
                items = list(self.selectedItems() or [])
                if not items:
                    event.ignore()
                    return

                self.blockSignals(True)
                try:
                    try:
                        pos = event.position().toPoint()

                    except Exception:
                        pos = event.pos()

                    drop_row = self.indexAt(pos).row()
                    if drop_row < 0:
                        drop_row = self.count()

                    for it in items:
                        if not it:
                            continue

                        if not (it.flags() & Qt.ItemIsSelectable):
                            continue

                        try:
                            data = it.data(Qt.UserRole) or {}

                        except Exception:
                            data = {}

                        time_str = data.get("time") if isinstance(data, dict) else None

                        try:
                            self.takeItem(self.row(it))

                        except Exception:
                            pass

                        if time_str and hasattr(self._app, "insert_task_into_quadrant_list"):
                            self._app.insert_task_into_quadrant_list(self, it)

                        else:
                            if drop_row >= self.count():
                                self.addItem(it)

                            else:
                                self.insertItem(drop_row, it)

                            drop_row += 1

                finally:
                    self.blockSignals(False)

                try:
                    self.clearSelection()

                except Exception:
                    pass

                try:
                    if hasattr(self._app, "cleanup_time_groups"):
                        self._app.cleanup_time_groups(self)

                except Exception:
                    pass

                try:
                    if hasattr(self._app, "save_tasks"):
                        self._app.save_tasks()

                    if hasattr(self._app, "calendar_pane") and self._app.calendar_pane:
                        self._app.calendar_pane.calendar_panel.update_task_list()

                except Exception:
                    pass

                event.setDropAction(Qt.CopyAction)
                event.accept()
                return

            if not isinstance(source, QListWidget):
                event.ignore()
                return

            items = list(source.selectedItems() or [])
            if not items:
                event.ignore()
                return

            new_state = Qt.Checked if self._is_completed_list else Qt.Unchecked

            source.blockSignals(True)
            self.blockSignals(True)
            try:
                for it in items:
                    if not it:
                        continue

                    if not (it.flags() & Qt.ItemIsSelectable):
                        continue

                    self._app.move_item_between_lists(it, source, self, new_state)

            finally:
                source.blockSignals(False)
                self.blockSignals(False)

            try:
                source.clearSelection()

            except Exception:
                pass

            try:
                if hasattr(self._app, "save_tasks"):
                    self._app.save_tasks()

                if hasattr(self._app, "calendar_pane") and self._app.calendar_pane:
                    self._app.calendar_pane.calendar_panel.update_task_list()

            except Exception:
                pass

            event.setDropAction(Qt.CopyAction)
            event.accept()

        except Exception as e:
            logger.error(f"Erro no dropEvent (drag&drop Eisenhower): {e}", exc_info=True)
            try:
                super().dropEvent(event)

            except Exception:
                pass
