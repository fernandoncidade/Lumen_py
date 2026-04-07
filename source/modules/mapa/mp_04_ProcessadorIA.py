from source.utils.LogManager import LogManager
from typing import List, Dict, Tuple, Any

try:
    from PySide6.QtCore import QCoreApplication

except Exception:
    QCoreApplication = None

logger = LogManager.get_logger()

from source.modules.mapa.ProcessadorIA import (
    _carregar_modelo_nlp,
    _detectar_idioma_texto,
    extrair_texto_pdf,
    extrair_texto_docx,
    extrair_texto_txt,
    extrair_texto,
    _corrigir_caracteres_extraidos,
    _corrigir_palavras_conhecidas,
    _preprocessar_linhas,
    _linha_parece_sumario,
    _proximo_titulo,
    _remover_acentos,
    _variantes_para_match,
    _detectar_secoes_avancado,
    _ajustar_niveis_relativos,
    _e_titulo_maiusculas,
    _e_titulo_isolado,
    _inferir_nivel_titulo,
    _construir_arvore_hierarquica,
    _processar_hierarquia_completa,
    analisar_estrutura,
    _gerar_resumo_contextual,
    _extrair_conceitos_semanticos,
    _extrair_ideias_principais,
    _extrair_conceitos_tfidf,
    _aplicar_tfidf_global,
    gerar_resumo_avancado,
    _load_sentence_transformer,
    get_sentence_embeddings,
    gerar_resumo_semantico,
    _identificar_relacoes_semanticas,
    _identificar_relacoes_avancadas,
    _log_estrutura_completa
)


class ProcessadorIA:
    def __init__(self):
        self._tr = lambda s: s

        try:
            if QCoreApplication and QCoreApplication.instance():
                self._tr = lambda s: QCoreApplication.translate("App", s)

            self.nlp = None
            self.idioma_detectado = 'pt'
            self._carregar_modelo_nlp()

        except Exception as e:
            logger.error(f"Erro ao inicializar ProcessadorIA: {e}", exc_info=True)

    def _carregar_modelo_nlp(self):
        _carregar_modelo_nlp(self)

    def _detectar_idioma_texto(self, texto: str) -> str:
        return _detectar_idioma_texto(self, texto)

    def extrair_texto_pdf(self, caminho: str) -> str:
        return extrair_texto_pdf(self, caminho)

    def _corrigir_caracteres_extraidos(self, texto: str) -> str:
        return _corrigir_caracteres_extraidos(self, texto)

    def _corrigir_palavras_conhecidas(self, linha: str) -> str:
        return _corrigir_palavras_conhecidas(self, linha)

    def extrair_texto_docx(self, caminho: str) -> str:
        return extrair_texto_docx(self, caminho)

    def extrair_texto_txt(self, caminho: str) -> str:
        return extrair_texto_txt(self, caminho)

    def extrair_texto(self, caminho: str) -> str:
        return extrair_texto(self, caminho)

    def analisar_estrutura(self, texto: str) -> Dict:
        return analisar_estrutura(self, texto)

    def _preprocessar_linhas(self, texto: str) -> List[str]:
        return _preprocessar_linhas(self, texto)

    def _linha_parece_sumario(self, linha: str) -> bool:
        return _linha_parece_sumario(self, linha)

    def _proximo_titulo(self, linhas: List[str], idx: int) -> str:
        return _proximo_titulo(self, linhas, idx)

    def _remover_acentos(self, s: str) -> str:
        return _remover_acentos(self, s)

    def _variantes_para_match(self, linha: str) -> Dict[str, str]:
        return _variantes_para_match(self, linha)

    def _detectar_secoes_avancado(self, texto: str, idioma: str = 'pt') -> List[Dict]:
        return _detectar_secoes_avancado(self, texto, idioma)

    def _ajustar_niveis_relativos(self, secoes: List[Dict]) -> List[Dict]:
        return _ajustar_niveis_relativos(self, secoes)

    def _e_titulo_maiusculas(self, linha: str, linhas: List[str], idx: int) -> bool:
        return _e_titulo_maiusculas(self, linha, linhas, idx)

    def _e_titulo_isolado(self, linha: str, linhas: List[str], idx: int) -> bool:
        return _e_titulo_isolado(self, linha, linhas, idx)

    def _inferir_nivel_titulo(self, titulo: str, nivel_anterior: int, tem_parte: bool) -> int:
        return _inferir_nivel_titulo(self, titulo, nivel_anterior, tem_parte)

    def _construir_arvore_hierarquica(self, texto: str, secoes_raw: List[Dict]) -> Dict:
        return _construir_arvore_hierarquica(self, texto, secoes_raw)

    def _processar_hierarquia_completa(self, texto_completo: str, no: Dict, idioma: str):
        return _processar_hierarquia_completa(self, texto_completo, no, idioma)

    def _gerar_resumo_contextual(self, doc, texto: str, nivel: int, titulo: str, idioma: str) -> str:
        return _gerar_resumo_contextual(self, doc, texto, nivel, titulo, idioma)

    def _extrair_conceitos_semanticos(self, doc, texto: str, nivel: int) -> List[Dict]:
        return _extrair_conceitos_semanticos(self, doc, texto, nivel)

    def _extrair_ideias_principais(self, doc, texto: str, nivel: int) -> List[Dict]:
        return _extrair_ideias_principais(self, doc, texto, nivel)

    def _aplicar_tfidf_global(self, texto: str, arvore: Dict):
        return _aplicar_tfidf_global(self, texto, arvore)

    def _identificar_relacoes_semanticas(self, arvore: Dict) -> List[Tuple[str, str, str]]:
        return _identificar_relacoes_semanticas(self, arvore)

    def _log_estrutura_completa(self, no: Dict, nivel: int = 0):
        return _log_estrutura_completa(self, no, nivel)

    def _extrair_conceitos_tfidf(self, doc, texto: str, max_conceitos: int = 15) -> List[Dict]:
        return _extrair_conceitos_tfidf(self, doc, texto, max_conceitos)

    def _identificar_relacoes_avancadas(self, doc, conceitos: List[Dict]) -> List[Tuple[str, str, str]]:
        return _identificar_relacoes_avancadas(self, doc, conceitos)

    def gerar_resumo_avancado(self, caminho_arquivo: str, top_n: int = 5) -> Dict[str, Any]:
        return gerar_resumo_avancado(self, caminho_arquivo, top_n)

    def _load_sentence_transformer(self, model_name: str = 'all-MiniLM-L6-v2'):
        return _load_sentence_transformer(self, model_name)

    def get_sentence_embeddings(self, texts: List[str], model_name: str = 'all-MiniLM-L6-v2'):
        return get_sentence_embeddings(self, texts, model_name)

    def gerar_resumo_semantico(self, caminho_arquivo: str, top_n: int = 5, model_name: str = 'all-MiniLM-L6-v2') -> Dict[str, Any]:
        return gerar_resumo_semantico(self, caminho_arquivo, top_n, model_name)
    