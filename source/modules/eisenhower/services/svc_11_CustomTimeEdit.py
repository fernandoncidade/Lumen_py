from PySide6.QtCore import QTime
from PySide6.QtWidgets import QTimeEdit
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class CustomTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWrapping(True)
        self._last_time = self.time()

    def stepBy(self, steps):
        current_time = self.time()
        current_section = self.currentSection()

        try:
            if current_section == QTimeEdit.MinuteSection:
                total_minutes = current_time.hour() * 60 + current_time.minute()
                total_minutes += steps

                if total_minutes < 0:
                    total_minutes = 1439

                elif total_minutes >= 1440:
                    total_minutes = 0

                new_hour = total_minutes // 60
                new_minute = total_minutes % 60
                new_time = QTime(new_hour, new_minute, current_time.second())
                self.setTime(new_time)

            else:
                super().stepBy(steps)

            self._last_time = self.time()

        except Exception as e:
            logger.error(f"Error in CustomTimeEdit.stepBy: {e}", exc_info=True)
