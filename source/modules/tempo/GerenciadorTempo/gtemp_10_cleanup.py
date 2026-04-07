from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def cleanup(self):
    try:
        try:
            if hasattr(self, 'pomodoro') and self.pomodoro and hasattr(self, '_tempo_worker'):
                try:
                    self.pomodoro.ciclo_completado.disconnect(self._tempo_worker.on_pomodoro)

                except Exception:
                    pass

        except Exception:
            pass

        try:
            if hasattr(self, '_tempo_worker') and self._tempo_worker is not None:
                try:
                    self._tempo_worker.stop()

                except Exception:
                    pass

        except Exception:
            pass

        if hasattr(self, '_tempo_thread'):
            try:
                try:
                    running = False
                    try:
                        running = self._tempo_thread.isRunning()

                    except RuntimeError:
                        running = False

                    except Exception:
                        running = False

                    if running:
                        try:
                            self._tempo_thread.quit()
                            self._tempo_thread.wait(2000)

                        except RuntimeError:
                            pass

                        except Exception:
                            try:
                                self._tempo_thread.terminate()

                            except Exception:
                                pass

                except RuntimeError:
                    pass

            except Exception:
                pass

        try:
            if hasattr(self, '_tempo_worker'):
                self._tempo_worker = None

        except Exception:
            pass

        try:
            if hasattr(self, '_tempo_thread'):
                self._tempo_thread = None

        except Exception:
            pass

    except Exception as e:
        self.logger.error(f"Erro ao limpar GerenciadorTempo: {e}", exc_info=True)
