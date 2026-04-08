from typing import Any, Dict, List
from collections import defaultdict
from source.utils.LogManager import LogManager
from .pia_32_util_texto import (
    jaccard_tokens,
    normalizar_espacos,
    normalizar_termo,
    obter_stopwords,
    termo_ruidoso,
    tokenizar_significativo,
)
logger = LogManager.get_logger()

def _sentencas_doc(doc: Any) -> List[Any]:
    try:
        sentencas = list(getattr(doc, "sents", []) or [])

        if sentencas:
            return sentencas

    except Exception:
        pass

    return [doc]

def _tem_parser(doc: Any) -> bool:
    try:
        if bool(getattr(doc, "is_parsed", False)):
            return True

        if hasattr(doc, "has_annotation"):
            return bool(doc.has_annotation("DEP"))

    except Exception:
        pass

    return False

def _extrair_conceitos_semanticos(self, doc, texto: str, nivel: int) -> List[Dict]:
    try:
        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))
        sentencas = _sentencas_doc(doc)
        candidatos: Dict[str, Dict[str, Any]] = {}

        def adicionar_candidato(
            termo_bruto: str,
            tipo: str,
            contexto: str = "",
            peso: float = 1.0,
        ) -> None:
            texto_raw = normalizar_espacos(termo_bruto or "")
            chave = normalizar_termo(texto_raw)

            if not chave:
                return

            if termo_ruidoso(chave, idioma=idioma, stopwords=stopwords):
                return

            tokens = chave.split()

            if len(tokens) > 6:
                return

            if sum(len(tok) for tok in tokens) < 4:
                return

            item = candidatos.get(chave)

            if item is None:
                texto_saida = texto_raw.strip()

                if tipo != "entidade" and texto_saida.islower():
                    texto_saida = texto_saida.capitalize()

                item = {
                    "texto": texto_saida[:90],
                    "tipo_scores": defaultdict(float),
                    "frequencia": 0.0,
                    "contextos": [],
                }
                candidatos[chave] = item

            item["tipo_scores"][tipo] += max(float(peso), 0.1)
            item["frequencia"] += max(float(peso), 0.1)

            if contexto:
                ctx = normalizar_espacos(contexto)

                if ctx and ctx not in item["contextos"] and len(item["contextos"]) < 5:
                    item["contextos"].append(ctx[:320])

        labels_entidade = {"PER", "PERSON", "ORG", "LOC", "GPE", "NORP", "MISC", "EVENT", "PRODUCT"}

        try:
            for ent in getattr(doc, "ents", []) or []:
                label = str(getattr(ent, "label_", "")).upper()

                if label not in labels_entidade:
                    continue

                sent_ent = ""

                try:
                    sent_ent = getattr(ent, "sent", None).text if hasattr(ent, "sent") else ""

                except Exception:
                    sent_ent = ""

                adicionar_candidato(ent.text, "entidade", sent_ent or ent.text, peso=2.4)

        except Exception:
            pass

        parser_disponivel = _tem_parser(doc)

        if parser_disponivel:
            try:
                for chunk in getattr(doc, "noun_chunks", []) or []:
                    tamanho = len(chunk)

                    if tamanho < 1 or tamanho > 6:
                        continue

                    adicionar_candidato(chunk.text, "termo_tecnico", getattr(chunk.sent, "text", ""), peso=1.8)

            except Exception as e:
                logger.debug(f"noun_chunks indisponivel no trecho atual: {e}")

        for sent in sentencas:
            sent_text = getattr(sent, "text", "")

            if not sent_text:
                continue

            if parser_disponivel:
                try:
                    tokens_validos = [
                        t for t in sent
                        if getattr(t, "is_alpha", False)
                        and not getattr(t, "is_stop", False)
                        and len(getattr(t, "text", "")) >= 3
                    ]

                    for tok in tokens_validos:
                        pos = getattr(tok, "pos_", "")

                        if pos not in ("NOUN", "PROPN", "ADJ"):
                            continue

                        lemma = getattr(tok, "lemma_", "") or tok.text
                        adicionar_candidato(lemma, "conceito", sent_text, peso=1.0)

                    for i in range(len(tokens_validos) - 1):
                        a = tokens_validos[i]
                        b = tokens_validos[i + 1]
                        pos_a = getattr(a, "pos_", "")
                        pos_b = getattr(b, "pos_", "")

                        if pos_b not in ("NOUN", "PROPN"):
                            continue

                        if pos_a not in ("ADJ", "NOUN", "PROPN"):
                            continue

                        la = getattr(a, "lemma_", "") or a.text
                        lb = getattr(b, "lemma_", "") or b.text
                        adicionar_candidato(f"{la} {lb}", "termo_tecnico", sent_text, peso=1.2)

                except Exception:
                    continue

            else:
                tokens = tokenizar_significativo(sent_text, idioma=idioma, stopwords=stopwords)

                for tok in tokens:
                    adicionar_candidato(tok, "conceito", sent_text, peso=0.8)

                for n in (2, 3):
                    for i in range(0, max(len(tokens) - n + 1, 0)):
                        gram = " ".join(tokens[i:i + n]).strip()
                        adicionar_candidato(gram, "termo_tecnico", sent_text, peso=0.9)

        tfidf_scores: Dict[str, float] = {}

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            corpus = [getattr(s, "text", "").strip() for s in sentencas if getattr(s, "text", "").strip()]

            if not corpus and texto:
                corpus = [texto]

            if corpus:
                vectorizer = TfidfVectorizer(
                    max_features=800,
                    stop_words=list(stopwords) if stopwords else None,
                    ngram_range=(1, 2),
                    min_df=1,
                )
                matriz = vectorizer.fit_transform(corpus)
                features = vectorizer.get_feature_names_out()
                medias = matriz.mean(axis=0).A1

                for feat, val in zip(features, medias):
                    chave_feat = normalizar_termo(feat)

                    if not chave_feat:
                        continue

                    tfidf_scores[chave_feat] = max(tfidf_scores.get(chave_feat, 0.0), float(val))

        except Exception:
            tfidf_scores = {}

        conceitos: List[Dict] = []

        for chave, item in candidatos.items():
            tipo = max(item["tipo_scores"].items(), key=lambda kv: kv[1])[0]
            palavras = chave.split()

            tfidf_local = tfidf_scores.get(chave, 0.0)

            if tfidf_local <= 0.0:
                valores = [tfidf_scores.get(tok, 0.0) for tok in palavras]
                valores = [v for v in valores if v > 0]

                if valores:
                    tfidf_local = sum(valores) / len(valores)

            freq_norm = min(item["frequencia"] / 8.0, 1.0)
            ctx_norm = min(len(item["contextos"]) / 4.0, 1.0)
            bonus_tipo = {"entidade": 0.18, "termo_tecnico": 0.12, "conceito": 0.06}.get(tipo, 0.05)
            bonus_multi = 0.12 if len(palavras) >= 2 else 0.0
            bonus_tfidf = min(tfidf_local * 3.5, 0.30)
            bonus_especificidade = min(sum(len(p) for p in palavras) / max(len(palavras) * 9.0, 1.0), 1.0) * 0.08

            importancia = 0.20
            importancia += freq_norm * 0.34
            importancia += ctx_norm * 0.16
            importancia += bonus_tipo + bonus_multi + bonus_tfidf + bonus_especificidade
            importancia = min(importancia, 1.0)

            conceitos.append(
                {
                    "texto": item["texto"],
                    "tipo": tipo,
                    "importancia": float(importancia),
                    "frequencia": int(round(item["frequencia"])),
                    "contextos": item["contextos"][:5],
                }
            )

        conceitos.sort(key=lambda c: c.get("importancia", 0.0), reverse=True)

        filtrados: List[Dict] = []

        for cand in conceitos:
            duplicado = False

            for mantido in filtrados:
                if normalizar_termo(cand["texto"]) == normalizar_termo(mantido["texto"]):
                    duplicado = True
                    break

                sim = jaccard_tokens(cand["texto"], mantido["texto"], idioma=idioma, stopwords=stopwords)

                if sim >= 0.82:
                    duplicado = True
                    break

                chave_c = normalizar_termo(cand["texto"])
                chave_m = normalizar_termo(mantido["texto"])

                if chave_c and chave_m:
                    if (chave_c in chave_m or chave_m in chave_c) and cand["importancia"] <= mantido["importancia"]:
                        duplicado = True
                        break

            if not duplicado:
                filtrados.append(cand)

        limite = {0: 16, 1: 13, 2: 10, 3: 8, 4: 6}.get(nivel, 6)
        return filtrados[:limite]

    except Exception as e:
        logger.error(f"Erro ao extrair conceitos semanticos: {e}", exc_info=True)
        return []
