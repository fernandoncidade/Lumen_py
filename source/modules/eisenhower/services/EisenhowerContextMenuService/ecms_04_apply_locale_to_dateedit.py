from PySide6.QtWidgets import QDateEdit, QCalendarWidget, QApplication
from PySide6.QtGui import QColor, QPalette
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _apply_locale_to_dateedit(self, de: QDateEdit):
    try:
        loc = self._effective_locale()
        de.setLocale(loc)

        cw = de.calendarWidget()
        if cw is None:
            cw = QCalendarWidget(de)
            de.setCalendarWidget(cw)

        cw.setLocale(loc)

        try:
            qt_app = QApplication.instance()
            if qt_app is not None:
                window_color = qt_app.palette().color(QPalette.Window)

                def _is_light_color(col: QColor) -> bool:
                    try:
                        r, g, b = col.red(), col.green(), col.blue()
                        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                        return lum >= 0.85

                    except Exception:
                        return True

                if True:
                    fill_color = QColor(window_color)

                pal = de.palette()
                pal.setColor(QPalette.Base, fill_color)
                pal.setColor(QPalette.AlternateBase, fill_color)
                de.setPalette(pal)

                try:
                    cw_pal = cw.palette()
                    cw_pal.setColor(QPalette.Base, fill_color)
                    cw_pal.setColor(QPalette.AlternateBase, fill_color)
                    cw.setPalette(cw_pal)

                except Exception as e:
                    logger.error(f"Falha ao aplicar palette no calendário do QDateEdit: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Falha ao aplicar locale no calendário do QDateEdit: {e}", exc_info=True)

        cw.update()
        de.update()

    except Exception as e:
        logger.error(f"Falha ao aplicar locale no calendário do QDateEdit: {e}", exc_info=True)
