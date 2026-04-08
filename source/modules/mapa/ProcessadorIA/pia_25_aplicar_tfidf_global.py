from typing import Dict, List
from source.utils.LogManager import LogManager
from .pia_32_util_texto import normalizar_termo, obter_stopwords
logger = LogManager.get_logger()

def _aplicar_tfidf_global(self, texto: str, arvore: Dict):
    from sklearn.feature_extraction.text import TfidfVectorizer

    try:
        def coletar_textos(no: Dict, textos_lista: List[str]):
            trecho = (no.get("texto_puro") or "").strip()

            if len(trecho) >= 40:
                textos_lista.append(trecho)

            for filho in no.get("filhos", []) or []:
                coletar_textos(filho, textos_lista)

        corpus: List[str] = []
        coletar_textos(arvore, corpus)

        if len(corpus) < 2 and texto:
            corpus = [texto]

        if not corpus:
            return

        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))

        vectorizer = TfidfVectorizer(
            max_features=1200,
            stop_words=list(stopwords) if stopwords else None,
            ngram_range=(1, 2),
            min_df=1,
        )
        tfidf = vectorizer.fit_transform(corpus)
        features = vectorizer.get_feature_names_out()

        score_termo: Dict[str, float] = {}
        medias = tfidf.mean(axis=0).A1

        for feat, val in zip(features, medias):
            chave = normalizar_termo(feat)

            if not chave:
                continue

            score_termo[chave] = max(score_termo.get(chave, 0.0), float(val))

        if not score_termo:
            return

        def score_para_conceito(texto_conceito: str) -> float:
            chave = normalizar_termo(texto_conceito)

            if not chave:
                return 0.0

            candidatos = {chave}
            tokens = chave.split()

            for tok in tokens:
                candidatos.add(tok)

            if len(tokens) >= 2:
                for i in range(0, len(tokens) - 1):
                    candidatos.add(f"{tokens[i]} {tokens[i + 1]}")

            valores = [score_termo[c] for c in candidatos if c in score_termo]

            if not valores:
                return 0.0

            return (0.65 * max(valores)) + (0.35 * (sum(valores) / len(valores)))

        def aplicar(no: Dict):
            for conceito in no.get("conceitos", []) or []:
                base = float(conceito.get("importancia", 0.0))
                freq = float(conceito.get("frequencia", 1) or 1)
                score_match = score_para_conceito(conceito.get("texto", ""))

                if score_match <= 0:
                    continue

                boost = min((score_match * 0.34) + min(freq / 60.0, 0.07), 0.25)
                conceito["importancia"] = min(base + boost, 1.0)

            for filho in no.get("filhos", []) or []:
                aplicar(filho)

        aplicar(arvore)
        logger.info("TF-IDF global aplicado para refinar importancias")

    except Exception as e:
        logger.error(f"Erro ao aplicar TF-IDF: {e}", exc_info=True)
