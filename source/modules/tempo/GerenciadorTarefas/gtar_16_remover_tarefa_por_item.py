from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def remover_tarefa_por_item(self, item):
    try:
        if not item:
            return

        tarefa_id = item.data(Qt.UserRole)
        linha0 = (item.text().split('\n')[0] or '').strip()
        emoji_prefix = linha0[:2] if linha0 else ''
        titulo_item = (
            linha0
            .replace('🔴 ', '')
            .replace('🟠 ', '')
            .replace('🟡 ', '')
            .replace('🟢 ', '')
        )
        prioridade_map = {
            "🔴": "Importante e Urgente",
            "🟠": "Importante, mas Não Urgente",
            "🟡": "Não Importante, mas Urgente",
            "🟢": "Não Importante e Não Urgente",
        }
        prioridade_item = prioridade_map.get(emoji_prefix, None)

        try:
            if not MessageBox.tempo_confirm_delete_task(self, titulo_item):
                return

        except Exception:
            pass

        total_antes = len(getattr(self, 'tarefas', []))

        if tarefa_id:
            self.tarefas = [t for t in self.tarefas if getattr(t, 'id', None) != tarefa_id]

        else:
            prioridade_norm = Tarefa.normalizar_prioridade(prioridade_item) if prioridade_item else None
            novas = []

            for t in self.tarefas:
                if t.titulo != titulo_item:
                    novas.append(t)
                    continue

                if prioridade_norm is None:
                    novas.append(t)
                    continue

                if Tarefa.normalizar_prioridade(getattr(t, 'prioridade', '')) != prioridade_norm:
                    novas.append(t)

            self.tarefas = novas

        self.salvar_tarefas()
        self.atualizar_listas()

        try:
            total_depois = len(getattr(self, 'tarefas', []))

            if total_depois < total_antes:
                MessageBox.tempo_delete_task_success(self)

            else:
                MessageBox.tempo_delete_task_failure(self)

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao remover tarefa pelo menu de contexto: {str(e)}", exc_info=True)
        try:
            MessageBox.tempo_delete_task_error(self)

        except Exception:
            pass
