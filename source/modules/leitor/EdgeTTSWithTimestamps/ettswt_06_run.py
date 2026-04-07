from source.utils.LogManager import LogManager
from source.modules.leitor.lt_05_WordTimestamp import WordTimestamp
import edge_tts
from edge_tts.exceptions import NoAudioReceived
import asyncio
import os
import uuid
logger = LogManager.get_logger()

def run(self):
    try:
        self._is_running = True
        chunks = self._split_text(self.texto)
        fallback_voices = ["pt-BR-AntonioNeural", "en-US-JennyNeural"]

        loop = asyncio.new_event_loop()
        self._active_loop = loop

        global_text_cursor = 0

        try:
            asyncio.set_event_loop(loop)

            async def synth_all():
                nonlocal global_text_cursor

                for idx, seg in enumerate(chunks):
                    if self._should_stop:
                        logger.debug("EdgeTTSWithTimestamps: parada solicitada.")
                        return

                    uid = uuid.uuid4().hex
                    outfile = os.path.join(self.outdir, f"tts_edge_ts_{os.getpid()}_{uid}_{idx}.mp3")
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
                    chunk_timestamps = []

                    for voice_candidate in candidates:
                        if not voice_candidate or voice_candidate in tried:
                            continue

                        tried.append(voice_candidate)
                        comm = None
                        gen = None
                        outfile_handle = None
                        chunk_timestamps = []
                        last_word_offset = 0
                        trial_text_cursor = global_text_cursor

                        try:
                            comm = edge_tts.Communicate(
                                seg, 
                                voice=voice_candidate, 
                                rate=f"{self.rate_pct:+d}%", 
                                volume=f"{self.volume_pct:+d}%",
                                boundary="WordBoundary"
                            )
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
                                        logger.debug("Parada solicitada durante stream.")
                                        break

                                    chunk_type = chunk.get("type")

                                    if chunk_type == "audio":
                                        outfile_handle.write(chunk.get("data", b""))
                                        outfile_handle.flush()

                                    elif chunk_type == "WordBoundary":
                                        try:
                                            word_text = chunk.get("text", "")
                                            offset_ticks = chunk.get("offset", 0)
                                            duration_ticks = chunk.get("duration", 0)

                                            offset_ms = offset_ticks // 10000
                                            duration_ms = duration_ticks // 10000

                                            absolute_text_pos, next_cursor, matched_len = self._find_word_in_full_text(
                                                word_text,
                                                self.texto,
                                                trial_text_cursor,
                                            )

                                            if absolute_text_pos >= 0:
                                                trial_text_cursor = next_cursor

                                                try:
                                                    if matched_len > 0:
                                                        word_text_for_ts = self.texto[absolute_text_pos:absolute_text_pos + matched_len]

                                                    else:
                                                        word_text_for_ts = word_text

                                                except Exception:
                                                    word_text_for_ts = word_text

                                            else:
                                                text_pos = self._calculate_text_offset(word_text, seg, last_word_offset)
                                                last_word_offset = text_pos + len(word_text)
                                                absolute_text_pos = max(0, global_text_cursor)
                                                word_text_for_ts = word_text

                                            wt = WordTimestamp(
                                                text=word_text_for_ts,
                                                offset_ms=offset_ms,
                                                duration_ms=duration_ms,
                                                text_offset=absolute_text_pos
                                            )
                                            chunk_timestamps.append(wt)

                                        except Exception as e:
                                            logger.debug(
                                                f"Erro ao processar WordBoundary: {e}", 
                                                exc_info=True
                                            )

                            except asyncio.CancelledError:
                                logger.debug("EdgeTTSWithTimestamps: stream cancelado.")
                                if os.path.exists(outfile_part):
                                    try:
                                        os.remove(outfile_part)

                                    except Exception:
                                        pass

                                return

                            if self._should_stop:
                                logger.debug("EdgeTTSWithTimestamps: geração interrompida.")
                                return

                            success = True
                            global_text_cursor = trial_text_cursor

                        except NoAudioReceived as nae:
                            last_err = str(nae)
                            logger.warning(f"No audio recebido com voice='{voice_candidate}': {nae}")

                        except Exception as e:
                            last_err = str(e)
                            logger.error(
                                f"Erro ao sintetizar segmento {idx} com voice '{voice_candidate}': {e}", 
                                exc_info=True
                            )

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

                            continue

                        if success:
                            try:
                                try:
                                    os.replace(outfile_part, outfile)

                                except Exception:
                                    os.rename(outfile_part, outfile)

                            except Exception:
                                logger.error(
                                    f"Falha ao renomear arquivo TTS: {outfile_part} -> {outfile}", 
                                    exc_info=True
                                )

                            logger.debug(
                                f"Síntese OK: voz={voice_candidate} segmento={idx} "
                                f"arquivo={outfile} timestamps={len(chunk_timestamps)}"
                            )

                            self._all_timestamps.extend(chunk_timestamps)
                            timestamps_dicts = [wt.to_dict() for wt in chunk_timestamps]
                            self.chunk_ready.emit(outfile, timestamps_dicts)
                            self.word_timestamps_ready.emit(timestamps_dicts)

                            break

                    if not success:
                        msg = last_err or "Falha desconhecida ao sintetizar áudio"
                        logger.error(f"Erro ao sintetizar segmento {idx}: {msg}", exc_info=True)
                        self.error.emit(msg)
                        return

            try:
                loop.run_until_complete(synth_all())

            except asyncio.CancelledError:
                logger.debug("EdgeTTSWithTimestamps: run interrupted by CancelledError.")

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
        logger.error(f"Erro ao executar Edge TTS com timestamps: {str(e)}", exc_info=True)
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
