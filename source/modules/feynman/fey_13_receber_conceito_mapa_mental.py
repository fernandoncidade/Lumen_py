from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def receber_conceito_mapa_mental(self, dados: dict):
    try:
        titulo = dados.get('titulo', '') or ''
        titulo = titulo.strip()

        explicacao_in = (dados.get('explicacao') or dados.get('notas') or '')
        explicacao_in = explicacao_in.strip()

        lacunas_in = (dados.get('lacunas') or '')
        lacunas_in = lacunas_in.strip()

        revisao_in = (dados.get('revisao') or explicacao_in)
        revisao_in = revisao_in.strip()

        dominio_in = int(dados.get('dominio', 0) or 0)
        arquivo_vinculado_in = (dados.get('arquivo_vinculado') or '').strip() or None

        if not titulo:
            logger.warning("Título vazio recebido do Mapa Mental, ignorando")
            return

        if not explicacao_in:
            logger.warning(f"Notas/explicacao vazias para conceito '{titulo}', ignorando")
            return

        logger.info(f"Recebendo conceito do Mapa Mental para integração: '{titulo}'")

        existente = next((c for c in self.conceitos if c.get('titulo') == titulo), None)

        if existente:
            existente['revisao'] = revisao_in

            exp = existente.get('explicacao', '') or ''
            if not exp.strip():
                existente['explicacao'] = explicacao_in

            else:
                if explicacao_in.strip() and explicacao_in.strip() not in exp:
                    existente['explicacao'] = exp + "\n\n" + explicacao_in

            if lacunas_in:
                existente['lacunas'] = lacunas_in

            try:
                existente['dominio'] = dominio_in

            except Exception:
                pass

            if arquivo_vinculado_in:
                existente['arquivo_vinculado'] = arquivo_vinculado_in

            logger.info(f"Conceito '{titulo}' atualizado com notas do Mapa Mental (merge/append)")

        else:
            novo = {
                'titulo': titulo,
                'explicacao': explicacao_in,
                'lacunas': lacunas_in,
                'revisao': revisao_in,
                'dominio': dominio_in,
                'arquivo_vinculado': arquivo_vinculado_in
            }
            self.conceitos.append(novo)
            logger.info(f"Novo conceito '{titulo}' criado a partir do Mapa Mental")

        self.salvar_conceitos()
        self.atualizar_lista()

        logger.info(f"Conceito '{titulo}' integrado e lista atualizada")

    except Exception as e:
        logger.error(f"Erro ao receber conceito do Mapa Mental: {str(e)}", exc_info=True)
