import re
from source.utils.LogManager import LogManager
from .pia_32_util_texto import remover_acentos
logger = LogManager.get_logger()

def _detectar_idioma_texto(self, texto: str) -> str:
    try:
        idioma_padrao = getattr(self, "idioma_detectado", "pt") or "pt"

        if not texto or len(texto.strip()) < 20:
            idioma_final = "en" if str(idioma_padrao).lower().startswith("en") else "pt"
            self.idioma_detectado = idioma_final
            return idioma_final

        amostra = texto[:30_000]
        texto_lower = amostra.lower()
        texto_sem_acentos = remover_acentos(texto_lower)
        tokens = re.findall(r"[a-zA-ZÀ-ÿ']+", texto_lower)

        if not tokens:
            idioma_final = "en" if str(idioma_padrao).lower().startswith("en") else "pt"
            self.idioma_detectado = idioma_final
            return idioma_final

        funcionais_pt = {
            "de", "da", "do", "que", "para", "com", "uma", "como", "mais", "nao",
            "nos", "das", "dos", "estao", "ser", "foi", "tambem", "entre",
        }

        funcionais_en = {
            "the", "and", "of", "to", "in", "for", "with", "that", "this", "from",
            "are", "was", "were", "been", "have", "has", "into", "their",
        }

        marcadores_pt = {
            "capitulo", "secao", "introducao", "conclusao", "metodologia",
            "referencias", "sumario", "indice", "figura", "tabela",
        }

        marcadores_en = {
            "chapter", "section", "introduction", "conclusion", "methodology",
            "references", "summary", "index", "figure", "table",
        }

        score_pt = sum(1 for t in tokens if remover_acentos(t) in funcionais_pt) * 1.1
        score_en = sum(1 for t in tokens if t.lower() in funcionais_en) * 1.1
        score_pt += sum(2.6 for m in marcadores_pt if m in texto_sem_acentos)
        score_en += sum(2.6 for m in marcadores_en if m in texto_sem_acentos)
        acentos_pt = len(re.findall(r"[ãõáéíóúâêôç]", texto_lower))
        score_pt += min(acentos_pt, 40) * 0.12

        try:
            lang_modelo = str(getattr(getattr(self, "nlp", None), "lang", "")).lower()

            if lang_modelo.startswith("pt"):
                score_pt += 0.8

            elif lang_modelo.startswith("en"):
                score_en += 0.8

        except Exception:
            pass

        escala = max(len(tokens) ** 0.5, 1.0)
        score_pt_norm = score_pt / escala
        score_en_norm = score_en / escala

        if abs(score_pt_norm - score_en_norm) < 0.08:
            if acentos_pt >= 4:
                self.idioma_detectado = "pt"
                return "pt"

            idioma_final = "en" if str(idioma_padrao).lower().startswith("en") else "pt"
            self.idioma_detectado = idioma_final
            return idioma_final

        idioma_final = "pt" if score_pt_norm > score_en_norm else "en"
        self.idioma_detectado = idioma_final
        return idioma_final

    except Exception as e:
        logger.error(f"Erro ao detectar idioma do texto: {e}", exc_info=True)
        idioma_final = "en" if str(getattr(self, "idioma_detectado", "pt")).lower().startswith("en") else "pt"
        self.idioma_detectado = idioma_final
        return idioma_final
