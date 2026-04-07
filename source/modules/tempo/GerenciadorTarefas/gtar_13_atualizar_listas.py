from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
logger = LogManager.get_logger()

try:
    from .gtar_25_prioridade_display import prioridade_para_texto

except Exception as e:
    logger.error(f"Erro ao importar prioridade_para_texto: {str(e)}", exc_info=True)
    prioridade_para_texto = None

def atualizar_listas(self):
    try:
        self.col_todo.lista.clear()
        self.col_doing.lista.clear()
        self.col_done.lista.clear()

        for tarefa in self.tarefas:
            prioridade_norm = Tarefa.normalizar_prioridade(getattr(tarefa, 'prioridade', 'Importante e Urgente'))
            emoji = {
                "Importante e Urgente": "🔴",
                "Importante, mas Não Urgente": "🟠",
                "Não Importante, mas Urgente": "🟡",
                "Não Importante e Não Urgente": "🟢",
            }.get(prioridade_norm, "🔴")

            pomodoros_texto = QCoreApplication.translate("App", "🍅 {n} pomodoros").format(n=tarefa.pomodoros_completados)
            texto = f"{emoji} {tarefa.titulo}\n{pomodoros_texto}"

            item = QListWidgetItem(texto)

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsDragEnabled
            )
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, getattr(tarefa, 'id', None))

            try:
                fp = getattr(tarefa, 'file_path', None)
                if fp:
                    font = item.font() or QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setForeground(Qt.blue)

            except Exception as e:
                logger.error(f"Erro ao destacar tarefa com arquivo vinculado: {str(e)}", exc_info=True)

            try:
                tooltip_lines = []

                fp = getattr(tarefa, 'file_path', None)
                if fp:
                    tooltip_lines.append((QCoreApplication.translate("App", "Arquivo") or "Arquivo") + f": {fp}")

                ds = getattr(tarefa, 'date', None)
                if ds:
                    try:
                        from PySide6.QtCore import QDate, QLocale
                        qd = QDate.fromString(ds, Qt.ISODate)
                        if qd.isValid():
                            try:
                                locale_name = QLocale().name() or ""

                            except Exception:
                                locale_name = ""

                            if locale_name.startswith("pt"):
                                fmt = "dd/MM/yyyy"

                            else:
                                fmt = "MM/dd/yyyy"

                            date_human = qd.toString(fmt)

                        else:
                            date_human = ds

                    except Exception as e:
                        logger.error(f"Erro ao formatar data para tooltip: {str(e)}", exc_info=True)
                        date_human = ds

                    tooltip_lines.append((QCoreApplication.translate("App", "Data") or "Data") + f": {date_human}")

                time_str = getattr(tarefa, 'time', None)
                if time_str:
                    tooltip_lines.append((QCoreApplication.translate("App", "Horário") or "Horário") + f": {time_str}")

                desc = getattr(tarefa, 'descricao', None)
                if desc:
                    tooltip_lines.append((QCoreApplication.translate("App", "Descrição") or "Descrição") + f": {desc}")

                prio = getattr(tarefa, 'prioridade', None)
                if prio is not None and prio != "":
                    try:
                        if prioridade_para_texto:
                            prio_t = prioridade_para_texto(prio, self)

                        else:
                            prio_t = str(prio)

                    except Exception as e:
                        logger.error(f"Erro ao obter texto da prioridade: {str(e)}", exc_info=True)
                        prio_t = str(prio)

                    tooltip_lines.append((QCoreApplication.translate("App", "Prioridade") or "Prioridade") + f": {prio_t}")

                if tooltip_lines:
                    try:
                        item.setToolTip("\n".join(tooltip_lines))

                    except Exception as e:
                        logger.error(f"Erro ao definir tooltip: {str(e)}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro ao construir tooltip: {str(e)}", exc_info=True)

            if tarefa.status == "Todo":
                self.col_todo.lista.addItem(item)

            elif tarefa.status == "Doing":
                self.col_doing.lista.addItem(item)

            else:
                self.col_done.lista.addItem(item)

        self.listas_atualizadas.emit()

    except Exception as e:
        logger.error(f"Erro ao atualizar listas de tarefas: {str(e)}", exc_info=True)
