from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
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
            resp = QMessageBox.question(
                self,
                QCoreApplication.translate("App", "Confirmar Exclusão"),
                QCoreApplication.translate("App", "Deseja remover {n} tarefa(s) selecionada(s)?").format(n=total_selecionadas),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if resp != QMessageBox.Yes:
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
                QMessageBox.information(
                    self,
                    QCoreApplication.translate("App", "Sucesso"),
                    QCoreApplication.translate("App", "{n} tarefa(s) removida(s) com sucesso!").format(n=removidas)
                )

            else:
                QMessageBox.warning(
                    self,
                    QCoreApplication.translate("App", "Falha"),
                    QCoreApplication.translate("App", "Não foi possível remover as tarefas selecionadas.")
                )

        except Exception:
            pass

    except Exception as e:
        logger.error(f"Erro ao remover tarefas marcadas: {str(e)}", exc_info=True)
        try:
            QMessageBox.warning(
                self,
                QCoreApplication.translate("App", "Falha"),
                QCoreApplication.translate("App", "Ocorreu um erro ao remover as tarefas.")
            )

        except Exception:
            pass
