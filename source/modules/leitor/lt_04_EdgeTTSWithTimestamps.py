from PySide6.QtCore import QThread, Signal
from source.utils.LogManager import LogManager
import os
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.modules.leitor.EdgeTTSWithTimestamps import stop, _split_text, _normalize_voice, _calculate_text_offset, _find_word_in_full_text, run


class EdgeTTSWithTimestamps(QThread):
    chunk_ready = Signal(str, list)
    error = Signal(str)
    word_timestamps_ready = Signal(list)

    def __init__(self, texto: str, voz: str = "pt-BR-AntonioNeural", rate_pct: int = 0, volume_pct: int = 0, outdir: str = None):
        super().__init__()
        self.logger = LogManager.get_logger()
        self.texto = texto
        self.voz = voz
        self.rate_pct = rate_pct
        self.volume_pct = volume_pct
        self.outdir = outdir or obter_caminho_persistente()

        try:
            os.makedirs(self.outdir, exist_ok=True)

        except Exception:
            pass

        self._should_stop = False
        self._is_running = False
        self._active_loop = None
        self._current_comm = None
        self._current_gen = None
        self._tracking_comms = set()
        self._current_outfile_part = None
        self._all_timestamps = []

    def stop(self):
        stop(self)

    def _split_text(self, text: str, max_chars: int = 3500) -> list:
        return _split_text(self, text, max_chars)

    def _normalize_voice(self, voz: str) -> str:
        return _normalize_voice(self, voz)

    def _calculate_text_offset(self, word: str, segment: str, last_offset: int) -> int:
        return _calculate_text_offset(self, word, segment, last_offset)

    def _find_word_in_full_text(self, word: str, full_text: str, start: int) -> tuple[int, int, int]:
        return _find_word_in_full_text(self, word, full_text, start)

    def run(self):
        run(self)

    def get_all_timestamps(self) -> list:
        return [wt.to_dict() for wt in self._all_timestamps]
