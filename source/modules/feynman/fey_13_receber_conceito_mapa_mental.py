from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def receber_conceito_mapa_mental(self, dados: dict):
    try:
        titulo = dados.get('titulo', '').strip()
        notas = dados.get('notas', '').strip()

        if not titulo:
            logger.warning("Título vazio recebido do Mapa Mental, ignorando")
            return

        if not notas:
            logger.warning(f"Notas vazias para conceito '{titulo}', ignorando")
            return

        logger.info(f"Recebendo conceito do Mapa Mental para integração: '{titulo}'")

        existente = next((c for c in self.conceitos if c.get('titulo') == titulo), None)

        if existente:
            existente['revisao'] = notas

            exp = existente.get('explicacao', '') or ''
            if not exp.strip():
                existente['explicacao'] = notas

            else:
                if notas.strip() and notas.strip() not in exp:
                    existente['explicacao'] = exp + "\n\n" + notas

            logger.info(f"Conceito '{titulo}' atualizado com notas do Mapa Mental (merge/append)")

        else:
            novo = {
                'titulo': titulo,
                'explicacao': notas,
                'lacunas': '',
                'revisao': notas,
                'dominio': 0
            }
            self.conceitos.append(novo)
            logger.info(f"Novo conceito '{titulo}' criado a partir do Mapa Mental")

        self.salvar_conceitos()
        self.atualizar_lista()

        logger.info(f"Conceito '{titulo}' integrado e lista atualizada")

    except Exception as e:
        logger.error(f"Erro ao receber conceito do Mapa Mental: {str(e)}", exc_info=True)
