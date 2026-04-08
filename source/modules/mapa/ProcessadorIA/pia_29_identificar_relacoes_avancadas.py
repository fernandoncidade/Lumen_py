from typing import Dict, List, Tuple
from itertools import combinations
from source.utils.LogManager import LogManager
from .pia_32_util_texto import normalizar_termo, obter_stopwords, tokenizar_significativo
logger = LogManager.get_logger()

def _tem_parser(doc_) -> bool:
    try:
        if bool(getattr(doc_, "is_parsed", False)):
            return True

        if hasattr(doc_, "has_annotation"):
            return bool(doc_.has_annotation("DEP"))

    except Exception:
        pass

    return False

def _identificar_relacoes_avancadas(self, doc, conceitos: List[Dict]) -> List[Tuple[str, str, str]]:
    try:
        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))

        conceito_map: Dict[str, str] = {}

        for c in conceitos or []:
            txt = (c.get("texto") or "").strip()
            chave = normalizar_termo(txt)

            if chave:
                conceito_map[chave] = txt.lower()

        if not conceito_map:
            return []

        def mapear(texto: str) -> str | None:
            chave = normalizar_termo(texto)

            if not chave:
                return None

            if chave in conceito_map:
                return conceito_map[chave]

            tokens = set(tokenizar_significativo(chave, idioma=idioma, stopwords=stopwords))

            if not tokens:
                return None

            melhor = None
            melhor_score = 0.0

            for ckey, valor in conceito_map.items():
                if chave in ckey or ckey in chave:
                    score = 0.70

                else:
                    tok_c = set(tokenizar_significativo(ckey, idioma=idioma, stopwords=stopwords))

                    if not tok_c:
                        continue

                    inter = len(tokens & tok_c)

                    if inter <= 0:
                        continue

                    score = inter / max(len(tokens), len(tok_c), 1)

                if score > melhor_score:
                    melhor_score = score
                    melhor = valor

            return melhor if melhor_score >= 0.48 else None

        rel_scores: Dict[Tuple[str, str, str], float] = {}

        def add_rel(a: str, verbo: str, b: str, peso: float):
            if not a or not b or a == b:
                return

            v = (verbo or "").strip().lower()

            if not v or len(v) < 2:
                v = "relaciona"

            if v in {"ser", "estar", "be", "is", "are", "was", "were", "have", "ter"}:
                v = "relaciona"

            key = (a, v, b)
            rel_scores[key] = rel_scores.get(key, 0.0) + max(float(peso), 0.05)

        sents = list(getattr(doc, "sents", []) or [])

        if not sents:
            sents = [doc]

        if _tem_parser(doc):
            for sent in sents:
                try:
                    for token in sent:
                        if getattr(token, "pos_", "") != "VERB":
                            continue

                        sujeitos = []
                        objetos = []

                        for child in token.children:
                            dep = getattr(child, "dep_", "")

                            if dep in ("nsubj", "nsubjpass", "csubj"):
                                sujeitos.append(child)

                            elif dep in ("dobj", "obj", "attr", "pobj", "obl", "oprd"):
                                objetos.append(child)

                            elif dep == "prep":
                                for g in child.children:
                                    if getattr(g, "dep_", "") in ("pobj", "obj"):
                                        objetos.append(g)

                        if not sujeitos or not objetos:
                            continue

                        lemma = getattr(token, "lemma_", "") or token.text
                        for subj in sujeitos:
                            subj_txt = " ".join(t.text for t in subj.subtree) if hasattr(subj, "subtree") else subj.text
                            a = mapear(subj_txt)

                            if not a:
                                continue

                            for obj in objetos:
                                obj_txt = " ".join(t.text for t in obj.subtree) if hasattr(obj, "subtree") else obj.text
                                b = mapear(obj_txt)

                                if not b:
                                    continue

                                add_rel(a, lemma, b, peso=1.2)

                except Exception:
                    continue

        for sent in sents:
            sent_txt = getattr(sent, "text", "")
            sent_norm = normalizar_termo(sent_txt)

            if not sent_norm:
                continue

            presentes = [(k, v) for k, v in conceito_map.items() if k in sent_norm]

            if len(presentes) < 2:
                continue

            presentes = sorted(set(presentes), key=lambda x: len(x[0]), reverse=True)[:6]

            for (_, a), (_, b) in combinations(presentes, 2):
                add_rel(a, "associa", b, peso=0.28)

        ordenadas = sorted(rel_scores.items(), key=lambda kv: kv[1], reverse=True)
        relacoes = [rel for rel, _score in ordenadas[:40] if rel[0] != rel[2]]
        return relacoes

    except Exception as e:
        logger.error(f"Erro em _identificar_relacoes_avancadas: {e}", exc_info=True)
        return []
