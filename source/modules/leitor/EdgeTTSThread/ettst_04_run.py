from source.utils.LogManager import LogManager
import edge_tts
from edge_tts.exceptions import NoAudioReceived
import asyncio, os
import uuid
logger = LogManager.get_logger()

def run(self):
    try:
        self._is_running = True
        chunks = self._split_text(self.texto)
        fallback_voices = ["pt-BR-AntonioNeural", "en-US-JennyNeural"]

        loop = asyncio.new_event_loop()
        self._active_loop = loop
        try:
            asyncio.set_event_loop(loop)

            async def synth_all():
                for idx, seg in enumerate(chunks):
                    if self._should_stop:
                        logger.debug("EdgeTTSThread: parada solicitada antes de sintetizar próximo segmento.")
                        return

                    uid = uuid.uuid4().hex
                    outfile = os.path.join(self.outdir, f"tts_edge_part_{os.getpid()}_{uid}_{idx}.mp3")
                    outfile_part = outfile + ".part"
                    self._current_outfile_part = outfile_part

                    tried = []
                    candidates = []
                    if self.voz:
                        candidates.append(self.voz)
                        candidates.append(self._normalize_voice(self.voz))

                    for fv in fallback_voices:
                        if fv not in candidates:
                            candidates.append(fv)

                    success = False
                    last_err = None

                    for voice_candidate in candidates:
                        if not voice_candidate or voice_candidate in tried:
                            continue

                        tried.append(voice_candidate)

                        comm = None
                        gen = None
                        outfile_handle = None
                        try:
                            comm = edge_tts.Communicate(seg, voice=voice_candidate, rate=f"{self.rate_pct:+d}%", volume=f"{self.volume_pct:+d}%")
                            self._current_comm = comm

                            try:
                                self._tracking_comms.add(comm)

                            except Exception:
                                pass

                            gen = comm.stream()
                            self._current_gen = gen

                            outfile_handle = open(outfile_part, "wb")
                            try:
                                async for chunk in gen:
                                    if self._should_stop:
                                        logger.debug("Parada solicitada durante stream; fechando generator.")
                                        break

                                    if chunk.get("type") == "audio":
                                        outfile_handle.write(chunk.get("data", b""))
                                        outfile_handle.flush()

                            except asyncio.CancelledError:
                                logger.debug("EdgeTTSThread: stream cancelado (asyncio.CancelledError).")
                                if os.path.exists(outfile_part):
                                    try:
                                        os.remove(outfile_part)

                                    except Exception:
                                        pass

                                return

                            if self._should_stop:
                                logger.debug("EdgeTTSThread: geração interrompida (stop).")
                                return

                            success = True

                        except NoAudioReceived as nae:
                            last_err = str(nae)
                            logger.warning(f"No audio recebido com voice='{voice_candidate}': {nae}")

                        except Exception as e:
                            last_err = str(e)
                            logger.error(f"Erro ao sintetizar segmento {idx} com voice '{voice_candidate}': {e}", exc_info=True)

                        finally:
                            try:
                                if outfile_handle:
                                    outfile_handle.close()

                            except Exception:
                                pass

                            try:
                                if gen is not None:
                                    aclose = getattr(gen, "aclose", None)
                                    if aclose:
                                        await aclose()

                            except Exception:
                                pass

                            try:
                                if comm is not None:
                                    aclose_comm = getattr(comm, "aclose", None)
                                    if aclose_comm:
                                        await aclose_comm()

                                    else:
                                        close_comm = getattr(comm, "close", None)
                                        if close_comm:
                                            try:
                                                close_comm()

                                            except Exception:
                                                pass

                            except Exception:
                                pass

                            self._current_gen = None
                            self._current_comm = None
                            try:
                                if comm in self._tracking_comms:
                                    self._tracking_comms.discard(comm)

                            except Exception:
                                pass

                        if not success:
                            try:
                                if os.path.exists(outfile_part):
                                    os.remove(outfile_part)

                            except Exception:
                                pass

                            if success:
                                break

                        if success:
                            try:
                                try:
                                    os.replace(outfile_part, outfile)

                                except Exception:
                                    os.rename(outfile_part, outfile)

                            except Exception:
                                logger.error(f"Falha ao renomear arquivo TTS: {outfile_part} -> {outfile}", exc_info=True)

                            logger.debug(f"Síntese OK: voz={voice_candidate} segmento={idx} arquivo={outfile}")
                            self.chunk_ready.emit(outfile)
                            break

                        if not success:
                            continue

                    if not success:
                        msg = last_err or "Falha desconhecida ao sintetizar áudio"
                        logger.error(f"Erro ao sintetizar segmento {idx}: {msg}", exc_info=True)
                        self.error.emit(msg)
                        return

            try:
                loop.run_until_complete(synth_all())

            except asyncio.CancelledError:
                logger.debug("EdgeTTSThread: run interrupted by CancelledError (treated as stop).")

            except Exception:
                raise

        finally:
            try:
                loop.run_until_complete(loop.shutdown_asyncgens())

            except Exception:
                pass

            try:
                for c in list(self._tracking_comms):
                    try:
                        aclose_comm = getattr(c, "aclose", None)
                        if aclose_comm:
                            loop.run_until_complete(aclose_comm())

                        else:
                            sess = getattr(c, "_session", None) or getattr(c, "session", None)
                            if sess is not None:
                                close_fn = getattr(sess, "close", None)
                                if asyncio.iscoroutinefunction(close_fn):
                                    loop.run_until_complete(close_fn())

                                elif callable(close_fn):
                                    close_fn()

                    except Exception:
                        pass

            except Exception:
                pass

            try:
                asyncio.set_event_loop(None)

            except Exception:
                pass

            try:
                loop.close()

            except Exception:
                pass

            self._active_loop = None

        self._is_running = False
        return

    except Exception as e:
        logger.error(f"Erro ao executar Edge TTS: {str(e)}", exc_info=True)
        self.error.emit(str(e))

    finally:
        self._is_running = False
        try:
            if self._active_loop:
                try:
                    self._active_loop.run_until_complete(self._active_loop.shutdown_asyncgens())

                except Exception:
                    pass

                try:
                    self._active_loop.close()

                except Exception:
                    pass

        except Exception:
            pass
