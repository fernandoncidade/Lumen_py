from source.utils.MessageBox import MessageBox
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def mudar_idioma(self, codigo_idioma):
    try:
        idioma_anterior = self.tradutor.obter_idioma_atual()

        if codigo_idioma == idioma_anterior:
            try:
                self.action_pt_br.setChecked(idioma_anterior == "pt_BR")
                self.action_en_us.setChecked(idioma_anterior == "en_US")

            except Exception:
                pass

            return

        if self.tradutor.definir_idioma(codigo_idioma):
            self.action_pt_br.setChecked(codigo_idioma == "pt_BR")
            self.action_en_us.setChecked(codigo_idioma == "en_US")

            self.atualizar_interface(codigo_idioma)
            self.atualizar_modulos()

            MessageBox.app_language_changed_success(self)

        else:
            try:
                self.action_pt_br.setChecked(idioma_anterior == "pt_BR")
                self.action_en_us.setChecked(idioma_anterior == "en_US")

            except Exception:
                pass

            MessageBox.app_language_change_error(self)

    except Exception as e:
        logger.error(f"Erro ao mudar idioma: {str(e)}", exc_info=True)
