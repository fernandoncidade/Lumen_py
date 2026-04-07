from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

@staticmethod
def normalizar_prioridade(valor):
    try:
        if not valor:
            return "Importante e Urgente"

        v_raw = str(valor).strip()
        v = v_raw.lower()

        p_iu = "Importante e Urgente"
        p_inu = "Importante, mas Não Urgente"
        p_niu = "Não Importante, mas Urgente"
        p_ninnu = "Não Importante e Não Urgente"

        if v.startswith("🔴"):
            return p_iu

        if v.startswith("🟠"):
            return p_inu

        if v.startswith("🟢"):
            return p_ninnu

        if v.startswith("🟡"):
            if "média" in v or "media" in v or "medium" in v:
                return p_inu

            return p_niu

        v_norm = (
            v.replace("não", "nao")
            .replace("ã", "a")
            .replace("á", "a")
            .replace("â", "a")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ô", "o")
            .replace("ú", "u")
        )
        v_norm = " ".join(v_norm.replace(",", " ").split())

        if "importante" in v_norm and "urgente" in v_norm and "nao urgente" not in v_norm:
            if "nao importante" in v_norm:
                return p_niu
            return p_iu

        if "importante" in v_norm and "nao urgente" in v_norm:
            if "nao importante" in v_norm:
                return p_ninnu
            return p_inu

        if "nao importante" in v_norm and "urgente" in v_norm:
            return p_niu

        if "nao importante" in v_norm and "nao urgente" in v_norm:
            return p_ninnu

        mapa_legado = {
            "alta": p_iu,
            "high": p_iu,
            "media": p_inu,
            "média": p_inu,
            "medium": p_inu,
            "baixa": p_ninnu,
            "low": p_ninnu,
        }
        if v in mapa_legado:
            return mapa_legado[v]

        return p_iu

    except Exception as e:
        logger.error(f"Erro ao normalizar prioridade: {str(e)}", exc_info=True)
        return "Importante e Urgente"
