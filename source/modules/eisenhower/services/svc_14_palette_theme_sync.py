from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QObject, QEvent


def install_palette_theme_sync(app, logger) -> None:
    try:
        from PySide6.QtWidgets import QApplication

        def _apply_window_as_base(widget):
            if widget is None:
                return

            qt_app = QApplication.instance()
            if qt_app is None:
                return

            window_color = qt_app.palette().color(QPalette.Window)

            def _is_light_color(col: QColor) -> bool:
                try:
                    r, g, b = col.red(), col.green(), col.blue()
                    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                    return lum >= 0.85

                except Exception:
                    return True

            is_light_theme = _is_light_color(window_color)

            try:
                target_widgets = (
                    app.task_input,
                    app.quadrant1_list,
                    app.quadrant2_list,
                    app.quadrant3_list,
                    app.quadrant4_list,
                    app.quadrant1_completed_list,
                    app.quadrant2_completed_list,
                    app.quadrant3_completed_list,
                    app.quadrant4_completed_list,
                )
            except Exception:
                target_widgets = ()

            calendar_base = QColor(window_color)

            try:
                from PySide6.QtWidgets import QDateEdit, QTimeEdit

                if is_light_theme:
                    if isinstance(widget, (QDateEdit, QTimeEdit)):
                        fill_color = QColor(calendar_base)

                    elif widget in target_widgets:
                        fill_color = QColor(245, 245, 245)

                    else:
                        fill_color = QColor(window_color).darker(125)

                else:
                    if widget in target_widgets:
                        fill_color = QColor(calendar_base)

                    elif isinstance(widget, (QDateEdit, QTimeEdit)):
                        fill_color = QColor(calendar_base)

                    else:
                        fill_color = QColor(window_color).darker(125)

            except Exception:
                fill_color = window_color

            try:
                from PySide6.QtWidgets import QLineEdit, QDateEdit, QTimeEdit, QComboBox
                is_native_input = isinstance(widget, (QLineEdit, QDateEdit, QTimeEdit, QComboBox))

            except Exception:
                is_native_input = False

            if is_native_input:
                try:
                    p = widget.palette()
                    if isinstance(widget, QComboBox):
                        p.setColor(QPalette.Button, window_color)

                    try:
                        target_inputs = (
                            getattr(app, "task_input", None),
                            getattr(app, "date_input", None),
                            getattr(app, "time_input", None),
                        )
                        if widget in target_inputs and fill_color is not None:
                            darker = QColor(fill_color).darker(110)
                            p.setColor(QPalette.Base, darker)

                    except Exception:
                        pass

                    widget.setPalette(p)

                    try:
                        if widget is getattr(app, "quadrant_selector", None):
                            view = getattr(widget, "view", None)

                            if callable(view):
                                try:
                                    v = view()

                                    if v is not None:
                                        popup_pal = v.palette()

                                        try:
                                            if fill_color is not None:
                                                try:
                                                    if is_light_theme:
                                                        popup_base = QColor(window_color)

                                                    else:
                                                        popup_base = QColor(fill_color).darker(115)

                                                except Exception:
                                                    popup_base = QColor(fill_color)

                                                popup_pal.setColor(QPalette.Base, popup_base)
                                                popup_pal.setColor(QPalette.AlternateBase, popup_base)

                                        except Exception:
                                            pass

                                        v.setPalette(popup_pal)

                                        try:
                                            v.viewport().setAutoFillBackground(True)
                                            v.viewport().setPalette(popup_pal)

                                        except Exception:
                                            pass

                                except Exception:
                                    pass

                    except Exception:
                        pass

                except Exception:
                    pass

            else:
                pal = widget.palette()
                pal.setColor(QPalette.Base, fill_color)
                pal.setColor(QPalette.AlternateBase, fill_color)

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

                else:
                    try:
                        widget.setAutoFillBackground(True)

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

        def _sync_eisenhower_backgrounds():
            if getattr(app, "_eisenhower_palette_sync_in_progress", False):
                return

            app._eisenhower_palette_sync_in_progress = True
            try:
                _apply_window_as_base(app.task_input)
                _apply_window_as_base(app.quadrant_selector)

                try:
                    _apply_window_as_base(app.date_input)

                except Exception:
                    pass

                try:
                    _apply_window_as_base(app.time_input)

                except Exception:
                    pass

                for w in (
                    app.quadrant1_list,
                    app.quadrant2_list,
                    app.quadrant3_list,
                    app.quadrant4_list,
                    app.quadrant1_completed_list,
                    app.quadrant2_completed_list,
                    app.quadrant3_completed_list,
                    app.quadrant4_completed_list,
                ):
                    _apply_window_as_base(w)

            except Exception as e:
                logger.debug(
                    f"Falha ao sincronizar fundos da Matriz Eisenhower via QPalette: {e}",
                    exc_info=True,
                )

            finally:
                try:
                    app._eisenhower_palette_sync_in_progress = False

                except Exception:
                    pass

        class _PaletteThemeSyncFilter(QObject):
            def eventFilter(self, obj, event):
                et = event.type()
                tipos = (
                    QEvent.ApplicationPaletteChange,
                    QEvent.PaletteChange,
                    QEvent.StyleChange,
                    QEvent.ThemeChange,
                )

                try:
                    tipos = tipos + (QEvent.ColorSchemeChange,)

                except AttributeError:
                    pass

                if et in tipos:
                    if not getattr(app, "_eisenhower_palette_sync_in_progress", False):
                        _sync_eisenhower_backgrounds()

                return super().eventFilter(obj, event)

        _sync_eisenhower_backgrounds()

        app._eisenhower_palette_sync_filter = _PaletteThemeSyncFilter(app)
        qt_app = QApplication.instance()
        if qt_app is not None:
            qt_app.installEventFilter(app._eisenhower_palette_sync_filter)

    except Exception as e:
        logger.debug(f"Falha ao instalar sync de paleta (Eisenhower): {e}", exc_info=True)
