from PySide6.QtWidgets import QComboBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def _ajustar_largura_combo(self, combo: QComboBox, padding_extra: int = 42, max_visiveis: int = 6):
    try:
        fm = combo.fontMetrics()
        max_width = 0
        for i in range(combo.count()):
            txt = combo.itemText(i)
            max_width = max(max_width, fm.horizontalAdvance(txt))

        largura = max_width + padding_extra
        combo.setFixedWidth(largura)
        combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        combo.setMaxVisibleItems(max_visiveis)

        view = combo.view()
        if view is not None:
            view.setMinimumWidth(largura)

    except Exception as e:
        logger.error(f"Erro ao ajustar largura do combo: {str(e)}", exc_info=True)
