import re
import unicodedata
from typing import List, Set

_STOPWORDS_PT = {
    "a", "ao", "aos", "as", "ate", "com", "como", "da", "das", "de", "dela", "dele",
    "deles", "delas", "do", "dos", "e", "ela", "ele", "eles", "em", "entre", "era",
    "eram", "essa", "esse", "esta", "este", "eu", "foi", "foram", "ha", "isso", "isto",
    "ja", "la", "lhe", "lhes", "mais", "mas", "me", "mesmo", "meu", "minha", "muito",
    "na", "nas", "nem", "no", "nos", "nossa", "nosso", "o", "os", "ou", "para", "pela",
    "pelas", "pelo", "pelos", "por", "qual", "que", "quem", "se", "sem", "ser", "seu",
    "sua", "suas", "tambem", "te", "tem", "tendo", "ter", "teu", "tua", "um", "uma",
    "uns", "umas", "vai", "voce", "voces",
}

_STOPWORDS_EN = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by", "for", "from",
    "had", "has", "have", "he", "her", "hers", "him", "his", "i", "in", "into", "is",
    "it", "its", "itself", "me", "my", "of", "on", "or", "our", "ours", "she", "that",
    "the", "their", "them", "there", "they", "this", "to", "was", "we", "were", "which",
    "who", "with", "you", "your", "yours",
}

_GENERIC_NOISE = {
    "capitulo", "chapter", "parte", "part", "secao", "section", "sumario", "summary",
    "indice", "index", "pagina", "page", "introducao", "introduction", "conclusao",
    "conclusion", "documento", "document",
}

def remover_acentos(texto: str) -> str:
    if not texto:
        return ""

    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))

def normalizar_espacos(texto: str) -> str:
    return re.sub(r"\s+", " ", (texto or "")).strip()

def normalizar_termo(termo: str) -> str:
    if not termo:
        return ""

    t = remover_acentos(termo.lower())
    t = re.sub(r"[^a-z0-9\s\-]", " ", t)
    t = t.replace("-", " ")
    t = normalizar_espacos(t)
    return t

def obter_stopwords(idioma: str = "pt", nlp=None) -> Set[str]:
    idioma_norm = (idioma or "pt").lower()
    stopwords = set(_STOPWORDS_EN if idioma_norm.startswith("en") else _STOPWORDS_PT)

    try:
        if nlp is not None and hasattr(nlp, "Defaults") and hasattr(nlp.Defaults, "stop_words"):
            stopwords.update(remover_acentos(w.lower()) for w in nlp.Defaults.stop_words)

    except Exception:
        pass

    return stopwords

def tokenizar_significativo(
    texto: str,
    idioma: str = "pt",
    stopwords: Set[str] | None = None,
    min_len: int = 3,
) -> List[str]:
    norm = normalizar_termo(texto)

    if not norm:
        return []

    stw = stopwords if stopwords is not None else obter_stopwords(idioma)
    tokens = []

    for tok in norm.split():
        if len(tok) < min_len:
            continue

        if tok.isdigit():
            continue

        if tok in stw:
            continue

        tokens.append(tok)

    return tokens


def termo_ruidoso(
    termo: str,
    idioma: str = "pt",
    stopwords: Set[str] | None = None,
) -> bool:
    norm = normalizar_termo(termo)

    if not norm:
        return True

    tokens = norm.split()

    if not tokens:
        return True

    stw = stopwords if stopwords is not None else obter_stopwords(idioma)

    if len(tokens) == 1:
        tok = tokens[0]

        if tok in stw or tok in _GENERIC_NOISE:
            return True

    if all(tok in stw for tok in tokens):
        return True

    if sum(ch.isdigit() for ch in norm) >= max(len(norm) // 2, 2):
        return True

    return False

def jaccard_tokens(
    texto_a: str,
    texto_b: str,
    idioma: str = "pt",
    stopwords: Set[str] | None = None,
) -> float:
    ta = set(tokenizar_significativo(texto_a, idioma=idioma, stopwords=stopwords))
    tb = set(tokenizar_significativo(texto_b, idioma=idioma, stopwords=stopwords))

    if not ta or not tb:
        return 0.0

    inter = len(ta & tb)
    uniao = len(ta | tb)
    return inter / max(uniao, 1)
