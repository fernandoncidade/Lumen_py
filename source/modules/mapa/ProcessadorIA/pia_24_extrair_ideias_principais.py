from typing import Any, Dict, List, Set
from collections import Counter
from source.utils.LogManager import LogManager
from .pia_32_util_texto import (
    jaccard_tokens,
    obter_stopwords,
    tokenizar_significativo,
)
logger = LogManager.get_logger()

def _sentencas_doc(doc: Any) -> List[Any]:
    try:
        sents = list(getattr(doc, "sents", []) or [])

        if sents:
            return sents

    except Exception:
        pass

    return [doc]

def _extrair_ideias_principais(self, doc, texto: str, nivel: int) -> List[Dict]:
    try:
        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))
        sentencas = _sentencas_doc(doc)
        total_sentencas = len(sentencas)

        if not sentencas:
            return []

        cue_pt = {
            "portanto", "assim", "logo", "resumindo", "fundamental",
            "essencial", "importante", "principal", "conclui", "define",
        }

        cue_en = {
            "therefore", "thus", "in summary", "important", "main",
            "fundamental", "essential", "concludes", "defines",
        }

        cue_words = cue_en if idioma.startswith("en") else cue_pt
        freq_tokens: Counter = Counter()

        for sent in sentencas:
            sent_text = getattr(sent, "text", "")

            for tok in set(tokenizar_significativo(sent_text, idioma=idioma, stopwords=stopwords)):
                freq_tokens[tok] += 1

        keywords = {t for t, f in freq_tokens.items() if f >= 2}

        if not keywords:
            keywords = {t for t, _ in freq_tokens.most_common(25)}

        ideias: List[Dict] = []

        for idx, sent in enumerate(sentencas):
            sent_texto = getattr(sent, "text", "").strip()

            if not (25 <= len(sent_texto) <= 360):
                continue

            tokens = tokenizar_significativo(sent_texto, idioma=idioma, stopwords=stopwords)

            if len(tokens) < 5:
                continue

            tokens_set: Set[str] = set(tokens)
            score = 0.0

            pos_rel = idx / max(total_sentencas - 1, 1)

            if idx <= 1:
                score += 0.22

            if pos_rel >= 0.85:
                score += 0.16

            score += max(0.12 - abs(0.40 - pos_rel) * 0.22, 0.01)
            hits_keywords = len(tokens_set & keywords)
            score += min((hits_keywords / max(len(tokens_set), 1)) * 0.42, 0.28)
            sent_lower = sent_texto.lower()

            if any(cue in sent_lower for cue in cue_words):
                score += 0.13

            if any(ch.isdigit() for ch in sent_texto):
                score += 0.05

            try:
                substantivos = [
                    t for t in sent
                    if getattr(t, "pos_", "") in ("NOUN", "PROPN")
                    and not getattr(t, "is_stop", False)
                ]

                verbos = [
                    t for t in sent
                    if getattr(t, "pos_", "") in ("VERB", "AUX")
                    and not getattr(t, "is_stop", False)
                ]

                densidade = (len(substantivos) + len(verbos)) / max(len(sent), 1)
                score += min(densidade * 0.34, 0.24)

            except Exception:
                pass

            tam = len(sent_texto)

            if 70 <= tam <= 220:
                score += 0.12

            elif tam < 35 or tam > 320:
                score -= 0.10

            paragrafo_idx = 0

            try:
                start_char = int(getattr(sent, "start_char", 0))
                paragrafo_idx = (texto[:start_char].count("\n\n") if texto else 0)

            except Exception:
                paragrafo_idx = 0

            ideias.append(
                {
                    "texto": sent_texto,
                    "tipo": "ideia_principal",
                    "importancia": float(min(score, 1.0)),
                    "paragrafo": paragrafo_idx,
                    "posicao_sentenca": idx,
                }
            )

        ideias.sort(key=lambda x: x["importancia"], reverse=True)

        sem_redundancia: List[Dict] = []

        for ideia in ideias:
            redundante = False

            for escolhida in sem_redundancia:
                sim = jaccard_tokens(
                    ideia["texto"],
                    escolhida["texto"],
                    idioma=idioma,
                    stopwords=stopwords,
                )

                if sim >= 0.74:
                    redundante = True
                    break

            if not redundante:
                sem_redundancia.append(ideia)

        limite = {0: 9, 1: 7, 2: 6, 3: 5, 4: 4}.get(nivel, 4)
        return sem_redundancia[:limite]

    except Exception as e:
        logger.error(f"Erro ao extrair ideias principais: {e}", exc_info=True)
        return []
