from PySide6.QtWidgets import QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt, QCoreApplication
from .ui_11_RotatedTabButton import RotatedTabButton
from .ui_12_CalendarPanel import CalendarPanel
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)


class Calendar(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        try:
            self.app = app
            self._expanded = False
            self._panel_width = 360
            self._layout_margins = (0, 11, 0, 0)

            layout = QHBoxLayout(self)
            layout.setContentsMargins(*self._layout_margins)
            layout.setSpacing(0)

            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

            self.toggle_button = RotatedTabButton(get_text("Mostrar Calendário"), self)
            self.toggle_button.setMinimumWidth(25)
            layout.addWidget(self.toggle_button, 0, Qt.AlignLeft | Qt.AlignTop)

            self.calendar_panel = CalendarPanel(app, self)
            self.calendar_panel.setMinimumWidth(max(self.calendar_panel.minimumSizeHint().width(), 300))
            self.calendar_panel.setMaximumWidth(16777215)
            self.calendar_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            layout.addWidget(self.calendar_panel, 1)

            self.calendar_panel.setVisible(False)
            self.setMinimumWidth(self.effective_min_width())

            if hasattr(self.app, "gerenciador_traducao"):
                self.app.gerenciador_traducao.idioma_alterado.connect(self.on_language_changed)

        except Exception as e:
            logger.error(f"Erro ao inicializar Calendar: {e}", exc_info=True)

    def effective_min_width(self) -> int:
        try:
            left, _top, right, _bottom = self._layout_margins
            btn_w = max(self.toggle_button.minimumWidth(), self.toggle_button.sizeHint().width())
            panel_w = 0

            if self._expanded and self.calendar_panel is not None:
                panel_w = max(self.calendar_panel.minimumWidth(), self.calendar_panel.minimumSizeHint().width())

            return left + btn_w + panel_w + right

        except Exception as e:
            logger.error(f"Erro ao calcular largura minima efetiva: {e}", exc_info=True)
            return 25

    def _sync_splitter_sizes_after_toggle(self):
        try:
            splitter = getattr(self.app, "main_splitter", None)

            if splitter is None:
                return

            sizes = splitter.sizes()
            if len(sizes) < 2:
                return

            left_min = max(self.minimumWidth(), self.effective_min_width())
            right_widget = splitter.widget(1)
            right_min = right_widget.minimumWidth() if right_widget is not None else 0
            total = max(0, int(sizes[0]) + int(sizes[1]))

            if self._expanded:
                target_left = max(int(sizes[0]), left_min)

            else:
                target_left = left_min

            max_left = max(left_min, total - right_min)
            target_left = min(target_left, max_left)
            target_right = max(right_min, total - target_left)

            if target_left + target_right != total:
                target_right = max(right_min, total - target_left)
                target_left = max(left_min, total - target_right)

            splitter.setSizes([int(target_left), int(target_right)])

        except Exception as e:
            logger.error(f"Erro ao sincronizar tamanhos do splitter: {e}", exc_info=True)

    def _update_splitter_interaction(self):
        try:
            splitter = getattr(self.app, "main_splitter", None)

            if splitter is None:
                return

            if self._expanded:
                splitter.setHandleWidth(6)

                try:
                    splitter.handle(1).setEnabled(True)

                except Exception:
                    pass

            else:
                splitter.setHandleWidth(0)

                try:
                    splitter.handle(1).setEnabled(False)

                except Exception:
                    pass

        except Exception as e:
            logger.error(f"Erro ao atualizar interacao do splitter: {e}", exc_info=True)

    def toggle_panel(self, open_if_hidden=False):
        try:
            if open_if_hidden and not self._expanded:
                self._expanded = True

            else:
                self._expanded = not self._expanded

            self.calendar_panel.setVisible(self._expanded)

            if self._expanded:
                hint_w = max(self.calendar_panel.sizeHint().width(), self.calendar_panel.minimumSizeHint().width(), 300)
                self._panel_width = max(self._panel_width, hint_w)
                self.toggle_button.setText(get_text("Recolher Calendário"))

            else:
                self.toggle_button.setText(get_text("Mostrar Calendário"))

            self.setMinimumWidth(self.effective_min_width())
            self.updateGeometry()
            self._sync_splitter_sizes_after_toggle()
            self._update_splitter_interaction()

        except Exception as e:
            logger.error(f"Erro ao alternar painel de calendário: {e}", exc_info=True)

    def on_language_changed(self):
        try:
            self.toggle_button.setText(get_text("Recolher Calendário") if self._expanded else get_text("Mostrar Calendário"))

            try:
                self.calendar_panel._on_language_changed()

            except Exception:
                pass

        except Exception as e:
            logger.error(f"Erro ao atualizar idioma do calendário: {e}", exc_info=True)
