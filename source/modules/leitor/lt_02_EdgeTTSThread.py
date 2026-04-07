from PySide6.QtCore import QThread, Signal
from source.utils.LogManager import LogManager
import os
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.modules.leitor.EdgeTTSThread import (
    stop,
    _split_text,
    _normalize_voice,
    run,
)


class EdgeTTSThread(QThread):
    chunk_ready = Signal(str)
    error = Signal(str)

    def __init__(self, texto, voz="pt-BR-AntonioNeural", rate_pct=0, volume_pct=0, outdir=None):
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

    def stop(self):
        stop(self)

    def _split_text(self, text, max_chars=3500):
        return _split_text(self, text, max_chars)

    def _normalize_voice(self, voz):
        return _normalize_voice(self, voz)

    def run(self):
        run(self)
