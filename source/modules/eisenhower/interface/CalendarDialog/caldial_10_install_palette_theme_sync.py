from PySide6.QtCore import QObject, QEvent
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication, QComboBox
from source.utils.LogManager import LogManager

def install_palette_theme_sync(owner, logger=None):
    if logger is None:
        logger = LogManager.get_logger()

    try:
        def _apply_window_as_base(widget):
            if widget is None:
                return

            qt_app = QApplication.instance()
            if qt_app is None:
                return

            window_color = qt_app.palette().color(QPalette.Window)
            pal = widget.palette()
            pal.setColor(QPalette.Base, window_color)
            pal.setColor(QPalette.AlternateBase, window_color)

            try:
                if isinstance(widget, QComboBox):
                    pal.setColor(QPalette.Button, window_color)

            except Exception:
                pass

            widget.setPalette(pal)

            vp = getattr(widget, "viewport", None)
            if callable(vp):
                try:
                    widget.viewport().setAutoFillBackground(True)
                    widget.viewport().setPalette(pal)

                except Exception:
                    pass

            view = getattr(widget, "view", None)
            if callable(view):
                try:
                    v = view()
                    if v is not None:
                        v.setPalette(pal)
                        try:
                            v.viewport().setAutoFillBackground(True)
                            v.viewport().setPalette(pal)

                        except Exception:
                            pass

                except Exception:
                    pass

        def _sync_calendar_backgrounds():
            try:
                _apply_window_as_base(getattr(owner, "tasks_list", None))
                _apply_window_as_base(getattr(owner, "filter_combo", None))

            except Exception as e:
                logger.debug(f"Falha ao sincronizar fundos do CalendarDialog via QPalette: {e}", exc_info=True)

        class _PaletteThemeSyncFilter(QObject):
            def eventFilter(self, obj, event):
                et = event.type()
                if et in (QEvent.ApplicationPaletteChange, QEvent.PaletteChange, QEvent.ThemeChange):
                    _sync_calendar_backgrounds()

                return super().eventFilter(obj, event)

        _sync_calendar_backgrounds()

        owner._calendar_palette_sync_filter = _PaletteThemeSyncFilter(owner)
        qt_app = QApplication.instance()
        if qt_app is not None:
            qt_app.installEventFilter(owner._calendar_palette_sync_filter)

    except Exception as e:
        logger.debug(f"Falha ao instalar sync de paleta (CalendarDialog): {e}", exc_info=True)
