from typing import Dict, List
from source.utils.LogManager import LogManager
from .pia_32_util_texto import (
    normalizar_espacos,
    normalizar_termo,
    obter_stopwords,
    termo_ruidoso,
    tokenizar_significativo,
)
logger = LogManager.get_logger()

def _extrair_conceitos_tfidf(self, doc, texto: str, max_conceitos: int = 15) -> List[Dict]:
    from sklearn.feature_extraction.text import TfidfVectorizer

    try:
        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))
        sentencas = [s.text.strip() for s in getattr(doc, "sents", []) if s.text.strip()]

        if not sentencas and texto:
            sentencas = [s.strip() for s in str(texto).split(". ") if len(s.strip()) > 10]

        if not sentencas:
            sentencas = [texto] if texto else []

        if not sentencas:
            return []

        vectorizer = TfidfVectorizer(
            max_features=1200,
            stop_words=list(stopwords) if stopwords else None,
            ngram_range=(1, 3),
            min_df=1,
        )
        tfidf = vectorizer.fit_transform(sentencas)
        features = vectorizer.get_feature_names_out()
        scores = tfidf.mean(axis=0).A1
        termos_scores = sorted(zip(features, scores), key=lambda x: x[1], reverse=True)

        noun_chunks = set()

        try:
            noun_chunks = {
                normalizar_termo(nc.text)
                for nc in getattr(doc, "noun_chunks", []) or []
                if 1 <= len(nc) <= 6
            }

        except Exception:
            noun_chunks = set()

        entidades = set()

        try:
            entidades = {
                normalizar_termo(ent.text)
                for ent in getattr(doc, "ents", []) or []
                if len(getattr(ent, "text", "")) >= 3
            }

        except Exception:
            entidades = set()

        conceitos: List[Dict] = []
        usados = set()

        def contexto_para(termo_norm: str) -> List[str]:
            ctx = []

            for s in sentencas:
                sn = normalizar_termo(s)

                if termo_norm and termo_norm in sn:
                    ctx.append(normalizar_espacos(s)[:320])

                    if len(ctx) >= 5:
                        break
            return ctx

        for termo, score in termos_scores[: max(max_conceitos * 6, 30)]:
            termo_out = normalizar_espacos(termo)
            termo_norm = normalizar_termo(termo_out)

            if not termo_norm or termo_norm in usados:
                continue

            if termo_ruidoso(termo_norm, idioma=idioma, stopwords=stopwords):
                continue

            tokens = tokenizar_significativo(termo_norm, idioma=idioma, stopwords=stopwords)

            if not tokens:
                continue

            if len(tokens) > 6:
                continue

            tipo = "conceito"

            if termo_norm in entidades:
                tipo = "entidade"

            elif termo_norm in noun_chunks or len(tokens) >= 2:
                tipo = "termo_tecnico"

            contextos = contexto_para(termo_norm)
            frequencia = max(len(contextos), 1)

            bonus_tipo = {"entidade": 0.18, "termo_tecnico": 0.10, "conceito": 0.05}.get(tipo, 0.05)
            importancia = 0.34 + min(float(score) * 4.2, 0.45) + bonus_tipo + min(frequencia * 0.03, 0.12)
            importancia = min(importancia, 1.0)

            texto_saida = termo_out.capitalize() if tipo != "entidade" and termo_out.islower() else termo_out
            conceitos.append(
                {
                    "texto": texto_saida[:90],
                    "tipo": tipo,
                    "importancia": float(importancia),
                    "frequencia": int(frequencia),
                    "contextos": contextos,
                }
            )
            usados.add(termo_norm)

            if len(conceitos) >= max_conceitos:
                break

        if not conceitos:
            conceitos = self._extrair_conceitos_semanticos(doc, texto, nivel=0)

        return conceitos[:max_conceitos]

    except Exception as e:
        logger.error(f"Erro em _extrair_conceitos_tfidf: {e}", exc_info=True)
        return []
