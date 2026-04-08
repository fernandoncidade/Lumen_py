from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text: str) -> str:
    return QCoreApplication.translate("App", text)

def prioridade_para_texto(prio, app=None) -> str:
    try:
        labels = {
            1: get_text("🔴 Importante e Urgente"),
            2: get_text("🟠 Importante, mas Não Urgente"),
            3: get_text("🟡 Não Importante, mas Urgente"),
            4: get_text("🟢 Não Importante e Não Urgente"),
        }

        if isinstance(prio, (int,)):
            return labels.get(prio, get_text("🔴 Importante e Urgente"))

        try:
            pint = int(str(prio))
            return labels.get(pint, get_text("🔴 Importante e Urgente"))

        except Exception as e:
            logger.debug(f"Erro ao converter prioridade para inteiro: {e}", exc_info=True)

        s = (str(prio) or "").strip()
        for val in labels.values():
            if s == val:
                return val

        s_no_emoji = s.lstrip('🔴🟠🟡🟢').strip()

        mapping = {
            "Importante e Urgente": labels[1],
            "Importante, mas Não Urgente": labels[2],
            "Não Importante, mas Urgente": labels[3],
            "Não Importante e Não Urgente": labels[4],
        }

        if s in mapping:
            return mapping[s]

        if s_no_emoji in mapping:
            return mapping[s_no_emoji]

        if s:
            return get_text(s)

        return ""

    except Exception as e:
        logger.debug(f"Erro ao converter prioridade para inteiro: {e}", exc_info=True)
        try:
            return QCoreApplication.translate("App", str(prio))

        except Exception as e:
            logger.debug(f"Erro ao converter prioridade para inteiro: {e}", exc_info=True)
            return str(prio or "")
