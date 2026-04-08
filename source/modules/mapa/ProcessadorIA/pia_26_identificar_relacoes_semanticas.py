from typing import Dict, List, Tuple
from itertools import combinations
from source.utils.LogManager import LogManager
from .pia_32_util_texto import normalizar_termo, obter_stopwords, tokenizar_significativo
logger = LogManager.get_logger()

def _tem_parser(doc) -> bool:
    try:
        if bool(getattr(doc, "is_parsed", False)):
            return True

        if hasattr(doc, "has_annotation"):
            return bool(doc.has_annotation("DEP"))

    except Exception:
        pass

    return False

def _identificar_relacoes_semanticas(self, arvore: Dict) -> List[Tuple[str, str, str]]:
    try:
        idioma = (getattr(self, "idioma_detectado", "pt") or "pt").lower()
        stopwords = obter_stopwords(idioma, nlp=getattr(self, "nlp", None))

        conceito_map: Dict[str, str] = {}
        sentencas_candidatas: List[str] = []

        def coletar(no: Dict):
            for conceito in no.get("conceitos", []) or []:
                texto_conceito = (conceito.get("texto") or "").strip()
                chave = normalizar_termo(texto_conceito)

                if chave:
                    conceito_map[chave] = texto_conceito.lower()

                for ctx in conceito.get("contextos", [])[:3]:
                    if ctx and len(ctx.strip()) > 20:
                        sentencas_candidatas.append(ctx.strip())

            for ideia in no.get("ideias_principais", [])[:3]:
                txt = (ideia.get("texto") or "").strip()

                if len(txt) > 20:
                    sentencas_candidatas.append(txt)

            resumo = (no.get("resumo_contextual") or "").strip()

            if resumo:
                for trecho in resumo.split(". "):
                    trecho = trecho.strip()

                    if len(trecho) > 25:
                        sentencas_candidatas.append(trecho)

                    if len(sentencas_candidatas) > 300:
                        break

            for filho in no.get("filhos", []) or []:
                coletar(filho)

        coletar(arvore)

        if not conceito_map:
            return []

        sentencas_unicas = []
        vistos = set()

        for s in sentencas_candidatas:
            chave = normalizar_termo(s)[:240]

            if not chave or chave in vistos:
                continue

            vistos.add(chave)
            sentencas_unicas.append(s)

        if not sentencas_unicas:
            return []

        def mapear_mencao_para_conceito(mencao: str) -> str | None:
            chave = normalizar_termo(mencao)

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
                    score = 0.72

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

        def adicionar_relacao(a: str, verbo: str, b: str, peso: float):
            if not a or not b or a == b:
                return

            v = (verbo or "").strip().lower()

            if not v or len(v) < 2:
                v = "relaciona"

            if v in {"ser", "estar", "be", "is", "are", "was", "were", "have", "ter"}:
                v = "relaciona"

            key = (a, v, b)
            rel_scores[key] = rel_scores.get(key, 0.0) + max(float(peso), 0.05)

        pipe = getattr(getattr(self, "nlp", None), "pipe", None)
        docs = None

        if callable(pipe):
            try:
                docs = pipe(sentencas_unicas, batch_size=16, n_process=1)

            except Exception:
                docs = None

        if docs is None:
            try:
                docs = (self.nlp(s) for s in sentencas_unicas)

            except Exception:
                docs = ()

        for doc in docs:
            try:
                sents = list(getattr(doc, "sents", []) or [doc])

            except Exception:
                sents = [doc]

            for sent in sents:
                sent_text = getattr(sent, "text", "")

                if not sent_text:
                    continue

                if _tem_parser(sent):
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

                            lemma_verbo = getattr(token, "lemma_", "") or token.text

                            for subj in sujeitos:
                                txt_s = " ".join(t.text for t in subj.subtree) if hasattr(subj, "subtree") else subj.text
                                a = mapear_mencao_para_conceito(txt_s)

                                if not a:
                                    continue

                                for obj in objetos:
                                    txt_o = " ".join(t.text for t in obj.subtree) if hasattr(obj, "subtree") else obj.text
                                    b = mapear_mencao_para_conceito(txt_o)

                                    if not b:
                                        continue

                                    adicionar_relacao(a, lemma_verbo, b, peso=1.25)

                    except Exception:
                        pass

                sent_norm = normalizar_termo(sent_text)
                presentes = []

                for ckey, valor in conceito_map.items():
                    if ckey and ckey in sent_norm:
                        presentes.append((ckey, valor))

                if len(presentes) >= 2:
                    presentes_ordenados = sorted(set(presentes), key=lambda x: len(x[0]), reverse=True)[:6]

                    for (_, a), (_, b) in combinations(presentes_ordenados, 2):
                        adicionar_relacao(a, "associa", b, peso=0.30)

        ordenadas = sorted(rel_scores.items(), key=lambda kv: kv[1], reverse=True)
        saida: List[Tuple[str, str, str]] = []

        for (a, v, b), _score in ordenadas[:60]:
            if a != b:
                saida.append((a, v, b))

        return saida[:45]

    except Exception as e:
        logger.error(f"Erro ao identificar relacoes semanticas: {e}", exc_info=True)
        return []
