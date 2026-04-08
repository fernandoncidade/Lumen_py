from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def atualizar_lista(self):
    try:
        self.lista_conceitos.clear()

        def _first_n_lines(text, n=5):
            if not text:
                return ""

            lines = [l for l in text.splitlines() if l.strip()]
            return "\n".join(lines[:n])

        for conceito in self.conceitos:
            emoji = ["🔴", "🟡", "🟢"][conceito.get('dominio', 0)]
            item = QListWidgetItem(f"{emoji} {conceito.get('titulo', '')}")

            titulo = conceito.get('titulo', '') or ''
            explicacao = conceito.get('explicacao', '') or ''
            lacunas = conceito.get('lacunas', '') or ''
            revisao = conceito.get('revisao', '') or ''

            parts = []
            ft = _first_n_lines(titulo, 5)

            if ft:
                parts.append(QCoreApplication.translate("App", "1️⃣ Conceito") + ":" + "\n" + ft)

            fe = _first_n_lines(explicacao, 5)

            if fe:
                parts.append(QCoreApplication.translate("App", "2️⃣ Explique") + ":" + "\n" + fe)

            fl = _first_n_lines(lacunas, 5)

            if fl:
                parts.append(QCoreApplication.translate("App", "3️⃣ Lacunas") + ":" + "\n" + fl)

            fr = _first_n_lines(revisao, 5)

            if fr:
                parts.append(QCoreApplication.translate("App", "4️⃣ Revisão") + ":" + "\n" + fr)

            tooltip = "\n\n".join(parts)

            if tooltip:
                item.setToolTip(tooltip)

            self.lista_conceitos.addItem(item)

    except Exception as e:
        logger.error(f"Erro ao atualizar lista de conceitos: {str(e)}", exc_info=True)
