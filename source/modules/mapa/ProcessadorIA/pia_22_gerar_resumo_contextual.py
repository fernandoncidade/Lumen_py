from typing import Any, Dict, List, Set
import numpy as np
from source.utils.LogManager import LogManager
from .pia_32_util_texto import obter_stopwords, tokenizar_significativo, jaccard_tokens
logger = LogManager.get_logger()

def _obter_sentencas(doc: Any) -> List[Any]:
    try:
        sentencas = list(getattr(doc, "sents", []) or [])

        if sentencas:
            return sentencas

    except Exception:
        pass

    return [doc]

def _selecionar_sentencas_mmr(
    candidatas: List[Dict],
    limite: int,
    idioma: str,
    stopwords: Set[str],
) -> List[Dict]:
    if not candidatas or limite <= 0:
        return []

    selecionadas: List[Dict] = []
    pendentes = sorted(candidatas, key=lambda x: x["score"], reverse=True)

    while pendentes and len(selecionadas) < limite:
        melhor = None
        melhor_mmr = float("-inf")

        for cand in pendentes[: min(80, len(pendentes))]:
            redundancia = 0.0

            if selecionadas:
                redundancia = max(
                    jaccard_tokens(cand["texto"], s["texto"], idioma=idioma, stopwords=stopwords)
                    for s in selecionadas
                )

            mmr = (0.72 * cand["score"]) - (0.28 * redundancia)

            if mmr > melhor_mmr:
                melhor_mmr = mmr
                melhor = cand

        if melhor is None:
            break

        selecionadas.append(melhor)
        pendentes = [p for p in pendentes if p is not melhor]

    return selecionadas

def _gerar_resumo_contextual(self, doc, texto: str, nivel: int, titulo: str, idioma: str) -> str:
    from sklearn.feature_extraction.text import TfidfVectorizer

    try:
        config_resumo = {
            0: {"num_sentencas": 9, "max_chars": 1400},
            1: {"num_sentencas": 7, "max_chars": 1050},
            2: {"num_sentencas": 5, "max_chars": 780},
            3: {"num_sentencas": 4, "max_chars": 560},
            4: {"num_sentencas": 3, "max_chars": 400},
        }
        cfg = config_resumo.get(nivel, {"num_sentencas": 3, "max_chars": 380})

        sentencas = _obter_sentencas(doc)
        textos_sentencas = [s.text.strip() for s in sentencas if getattr(s, "text", "").strip()]

        if not textos_sentencas:
            return (texto or "")[: cfg["max_chars"]]

        if len(textos_sentencas) <= cfg["num_sentencas"]:
            resumo_base = " ".join(textos_sentencas)
            return resumo_base[: cfg["max_chars"]]

        idioma_base = (idioma or getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma_base, nlp=getattr(self, "nlp", None))
        titulo_tokens = set(tokenizar_significativo(titulo or "", idioma=idioma_base, stopwords=stopwords))

        tfidf_matrix = None

        try:
            vectorizer = TfidfVectorizer(
                max_features=700,
                stop_words=list(stopwords) if stopwords else None,
                ngram_range=(1, 2),
                min_df=1,
            )
            tfidf_matrix = vectorizer.fit_transform(textos_sentencas)

        except Exception:
            tfidf_matrix = None

        palavras_cue_pt = {
            "portanto", "assim", "logo", "resumindo", "conclui", "conclusao",
            "principal", "fundamental", "importante", "essencial",
        }

        palavras_cue_en = {
            "therefore", "thus", "in summary", "in conclusion", "main",
            "fundamental", "important", "essential", "overall",
        }

        palavras_cue = palavras_cue_en if idioma_base.startswith("en") else palavras_cue_pt
        candidatas = []
        total = len(textos_sentencas)

        for idx, sent in enumerate(sentencas):
            sent_texto = sent.text.strip()

            if not sent_texto:
                continue

            tokens = tokenizar_significativo(sent_texto, idioma=idioma_base, stopwords=stopwords)

            if len(tokens) < 4:
                continue

            score = 0.0
            pos_rel = idx / max(total - 1, 1)

            if idx <= 1:
                score += 0.22

            if pos_rel >= 0.85:
                score += 0.12

            score += max(0.16 - abs(0.35 - pos_rel) * 0.22, 0.02)
            tam = len(sent_texto)

            if 55 <= tam <= 240:
                score += 0.18

            elif tam < 35 or tam > 320:
                score -= 0.16

            if tfidf_matrix is not None:
                try:
                    row = tfidf_matrix[idx].toarray().ravel()

                    if row.size > 0:
                        top = np.sort(row)[-8:]
                        score += min(float(top.mean()) * 5.0, 0.33)

                except Exception:
                    pass

            tok_set = set(tokens)

            if titulo_tokens:
                overlap_titulo = len(tok_set & titulo_tokens) / max(len(titulo_tokens), 1)
                score += min(overlap_titulo * 0.42, 0.28)

            sent_lower = sent_texto.lower()

            if any(cue in sent_lower for cue in palavras_cue):
                score += 0.12

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
                score += min(densidade * 0.35, 0.24)

            except Exception:
                pass

            candidatas.append(
                {
                    "idx": idx,
                    "texto": sent_texto,
                    "score": float(score),
                }
            )

        if not candidatas:
            fallback = " ".join(textos_sentencas[: cfg["num_sentencas"]])
            return fallback[: cfg["max_chars"]]

        selecionadas = _selecionar_sentencas_mmr(
            candidatas,
            limite=cfg["num_sentencas"],
            idioma=idioma_base,
            stopwords=stopwords,
        )
        selecionadas = sorted(selecionadas, key=lambda s: s["idx"])

        partes: List[str] = []
        tamanho_atual = 0

        for sent in selecionadas:
            trecho = sent["texto"]
            novo_tamanho = tamanho_atual + len(trecho) + (1 if partes else 0)

            if novo_tamanho > cfg["max_chars"]:
                break

            partes.append(trecho)
            tamanho_atual = novo_tamanho

        resumo = " ".join(partes).strip()

        if not resumo:
            resumo = " ".join(s["texto"] for s in selecionadas[:2]).strip()

        if len(resumo) > cfg["max_chars"]:
            resumo = resumo[: cfg["max_chars"]].rstrip() + "..."

        return resumo

    except Exception as e:
        logger.error(f"Erro ao gerar resumo contextual: {e}", exc_info=True)

        try:
            sentencas = [s.text.strip() for s in getattr(doc, "sents", []) if s.text.strip()]
            if sentencas:
                return " ".join(sentencas[:3])[:500] + "..."

        except Exception:
            pass

        return (texto or "")[:500] + ("..." if len(texto or "") > 500 else "")
