from source.utils.LogManager import LogManager
import asyncio, os
logger = LogManager.get_logger()

def stop(self):
    try:
        self._should_stop = True

        try:
            p = getattr(self, "_current_outfile_part", None)
            if p and os.path.exists(p):
                try:
                    os.remove(p)

                except Exception:
                    pass

        except Exception:
            pass

        try:
            loop = self._active_loop
            if loop is None:
                return

            async def _force_shutdown():
                try:
                    current = asyncio.current_task()
                    tasks = [t for t in asyncio.all_tasks() if t is not current and not t.done()]
                    for t in tasks:
                        try:
                            t.cancel()

                        except Exception:
                            pass

                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)

                except Exception:
                    pass

                try:
                    gen = getattr(self, "_current_gen", None)
                    if gen is not None:
                        aclose = getattr(gen, "aclose", None)
                        if aclose:
                            try:
                                await aclose()

                            except Exception:
                                pass

                except Exception:
                    pass

                try:
                    comm = getattr(self, "_current_comm", None)
                    comms = list(self._tracking_comms) if self._tracking_comms else []
                    if comm is not None and comm not in comms:
                        comms.append(comm)

                    for c in comms:
                        try:
                            aclose_comm = getattr(c, "aclose", None)
                            if aclose_comm:
                                try:
                                    await aclose_comm()

                                except Exception:
                                    pass

                            else:
                                sess = getattr(c, "_session", None) or getattr(c, "session", None)
                                if sess is not None:
                                    close_fn = getattr(sess, "close", None)
                                    if asyncio.iscoroutinefunction(close_fn):
                                        try:
                                            await close_fn()

                                        except Exception:
                                            pass

                                    elif callable(close_fn):
                                        try:
                                            close_fn()

                                        except Exception:
                                            pass

                        except Exception:
                            pass

                except Exception:
                    pass

            try:
                fut = asyncio.run_coroutine_threadsafe(_force_shutdown(), loop)
                try:
                    fut.result(timeout=2.0)

                except Exception:
                    pass

            except Exception:
                pass

        except Exception as e:
            logger.debug(f"Erro ao agendar fechamento de recursos assíncronos: {e}", exc_info=True)

        try:
            if loop is not None and self._tracking_comms:
                for c in list(self._tracking_comms):
                    try:
                        aclose_comm = getattr(c, "aclose", None)
                        if aclose_comm:
                            asyncio.run_coroutine_threadsafe(aclose_comm(), loop)

                        else:
                            sess = getattr(c, "_session", None) or getattr(c, "session", None)
                            if sess is not None:
                                close_fn = getattr(sess, "close", None)
                                if callable(close_fn):
                                    if asyncio.iscoroutinefunction(close_fn):
                                        asyncio.run_coroutine_threadsafe(close_fn(), loop)

                                    else:
                                        loop.call_soon_threadsafe(close_fn)

                    except Exception:
                        pass

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao solicitar parada da thread: {e}", exc_info=True)
