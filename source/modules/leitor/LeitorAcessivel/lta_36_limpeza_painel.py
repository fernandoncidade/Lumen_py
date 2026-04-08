from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def limpar_painel(self):
    try:
        try:
            msg_titulo = QCoreApplication.translate("App", "Limpar conteúdo")
            msg_texto = QCoreApplication.translate(
                "App",
                "Esta ação irá limpar o conteúdo das abas \"Texto\" e \"PDF\".\n\nDeseja continuar?"
            )
            resp = QMessageBox.warning(
                self,
                msg_titulo,
                msg_texto,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if resp != QMessageBox.StandardButton.Yes:
                return

        except Exception:
            pass

        try:
            if getattr(self, "btn_stop", None) is not None and self.btn_stop.isEnabled():
                self.parar_leitura()

        except Exception:
            pass

        try:
            if getattr(self, "texto_area", None) is not None:
                self.texto_area.clear()

        except Exception as e:
            logger.debug(f"Erro ao limpar texto: {e}", exc_info=True)

        try:
            if getattr(self, "_text_find_bar", None) is not None:
                self._text_find_bar.hide_bar()

            if hasattr(self, "_text_find_clear"):
                self._text_find_clear()

        except Exception as e:
            logger.debug(f"Erro ao limpar barra de busca do texto: {e}", exc_info=True)

        try:
            if getattr(self, "pdf_view", None) is not None:
                self.pdf_view.clear()

        except Exception as e:
            logger.debug(f"Erro ao limpar visualizador de PDF: {e}", exc_info=True)

        try:
            self.pdf_doc = None

        except Exception:
            pass

        try:
            self._last_pdf_path = None

        except Exception:
            pass

        try:
            self._current_reading_pdf_path = None

        except Exception:
            pass

        try:
            self._pdf_current_page = 0

        except Exception:
            pass

        try:
            self._pdf_zoom_special = None

        except Exception:
            pass

        try:
            if getattr(self, "_pdf_mouse_handler", None) is not None:
                self._pdf_mouse_handler.set_mode("default")

        except Exception:
            pass

        try:
            if getattr(self, "_pdf_find_bar", None) is not None:
                self._pdf_find_bar.hide_bar()

            if hasattr(self, "_pdf_find_clear"):
                self._pdf_find_clear()

        except Exception as e:
            logger.debug(f"Erro ao limpar barra de busca do PDF: {e}", exc_info=True)

        try:
            if hasattr(self, "_pdf_enable_toolbar"):
                self._pdf_enable_toolbar(False)

        except Exception:
            pass

        try:
            if hasattr(self, "spin_page") and self.spin_page is not None:
                self.spin_page.blockSignals(True)
                self.spin_page.setMinimum(1)
                self.spin_page.setMaximum(1)
                self.spin_page.setValue(1)
                self.spin_page.blockSignals(False)

            if hasattr(self, "label_total_pages") and self.label_total_pages is not None:
                self.label_total_pages.setText("/ 1")

        except Exception:
            pass

        try:
            if hasattr(self, "combo_zoom") and self.combo_zoom is not None:
                self.combo_zoom.setCurrentText("100%")

            if hasattr(self, "btn_zoom_fit_width") and self.btn_zoom_fit_width is not None:
                self.btn_zoom_fit_width.setChecked(False)
                self.btn_zoom_fit_width.setStyleSheet("")

            if hasattr(self, "btn_zoom_fit_page") and self.btn_zoom_fit_page is not None:
                self.btn_zoom_fit_page.setChecked(False)
                self.btn_zoom_fit_page.setStyleSheet("")

            if hasattr(self, "btn_mode_hand") and self.btn_mode_hand is not None:
                self.btn_mode_hand.setChecked(False)
                self.btn_mode_hand.setStyleSheet("")

            if hasattr(self, "btn_mode_select") and self.btn_mode_select is not None:
                self.btn_mode_select.setChecked(False)
                self.btn_mode_select.setStyleSheet("")

        except Exception:
            pass

        try:
            if hasattr(self, "_content_stack") and self._content_stack is not None:
                self._content_stack.setCurrentIndex(0)

        except Exception:
            pass

        try:
            if hasattr(self, "_stop_speech_highlight"):
                self._stop_speech_highlight()

            if hasattr(self, "_stop_pdf_speech_highlight"):
                self._stop_pdf_speech_highlight()

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao limpar painel: {e}", exc_info=True)
