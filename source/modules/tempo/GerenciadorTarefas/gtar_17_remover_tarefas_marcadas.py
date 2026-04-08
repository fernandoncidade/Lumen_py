from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

def remover_tarefas_marcadas(self):
    try:
        ids_para_remover = set()
        titulos_para_remover = set()
        titulos_prioridades_para_remover = set()

        for lista in (self.col_todo.lista, self.col_doing.lista, self.col_done.lista):
            try:
                for it in lista.selectedItems() or []:
                    tid = it.data(Qt.UserRole)

                    if tid:
                        ids_para_remover.add(tid)

                    else:
                        linha0 = (it.text().split('\n')[0] or '').strip()
                        emoji_prefix = linha0[:2] if linha0 else ''
                        titulo = (
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
                        titulos_para_remover.add(titulo)

                        if prioridade_item:
                            titulos_prioridades_para_remover.add((titulo, Tarefa.normalizar_prioridade(prioridade_item)))

            except Exception:
                pass

            for i in range(lista.count()):
                it = lista.item(i)

                if it.checkState() == Qt.Checked:
                    tid = it.data(Qt.UserRole)

                    if tid:
                        ids_para_remover.add(tid)

                    else:
                        linha0 = (it.text().split('\n')[0] or '').strip()
                        emoji_prefix = linha0[:2] if linha0 else ''
                        titulo = (
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
                        titulos_para_remover.add(titulo)

                        if prioridade_item:
                            titulos_prioridades_para_remover.add((titulo, Tarefa.normalizar_prioridade(prioridade_item)))

        if not ids_para_remover and not titulos_para_remover and not titulos_prioridades_para_remover:
            return

        total_selecionadas = len(ids_para_remover) + len(titulos_para_remover) + len(titulos_prioridades_para_remover)

        try:
            if not MessageBox.tempo_confirm_delete_tasks(self, total_selecionadas):
                return

        except Exception:
            pass

        total_antes = len(getattr(self, 'tarefas', []))
        novas = []

        for t in self.tarefas:
            if getattr(t, 'id', None) in ids_para_remover:
                continue

            if t.titulo in titulos_para_remover:
                prio_norm = Tarefa.normalizar_prioridade(getattr(t, 'prioridade', ''))

                if (t.titulo, prio_norm) in titulos_prioridades_para_remover:
                    continue

            novas.append(t)

        self.tarefas = novas
        self.salvar_tarefas()
        self.atualizar_listas()

        try:
            total_depois = len(getattr(self, 'tarefas', []))
            removidas = max(total_antes - total_depois, 0)

            if removidas > 0:
                MessageBox.tempo_delete_tasks_success(self, removidas)

            else:
                MessageBox.tempo_delete_tasks_failure(self)

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao remover tarefas marcadas: {str(e)}", exc_info=True)
        try:
            MessageBox.tempo_delete_tasks_error(self)

        except Exception:
            pass
