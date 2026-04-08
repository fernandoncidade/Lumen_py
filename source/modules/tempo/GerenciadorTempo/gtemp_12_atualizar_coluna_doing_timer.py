from PySide6.QtCore import QCoreApplication, QDate, QLocale, Qt
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
from source.modules.tempo.tmp_01_Tarefa import Tarefa
from source.modules.tempo.GerenciadorTarefas.gtar_25_prioridade_display import prioridade_para_texto
logger = LogManager.get_logger()

def atualizar_coluna_doing_timer(self):
    try:
        self.col_doing_timer_list.clear()

        if not hasattr(self, 'tarefas') or not self.tarefas:
            return

        prioridade_rank = {
            "Importante e Urgente": 1,
            "Importante, mas Não Urgente": 2,
            "Não Importante, mas Urgente": 3,
            "Não Importante e Não Urgente": 4,
        }

        def _parse_date(valor):
            if not valor:
                return None

            try:
                qd = QDate.fromString(str(valor), Qt.ISODate)
                if qd.isValid():
                    return qd

            except Exception:
                pass

            return None

        def _parse_time(valor):
            if not valor:
                return None

            try:
                parts = str(valor).strip().split(":")
                if len(parts) >= 2:
                    h = int(parts[0])
                    m = int(parts[1])
                    return h, m

            except Exception:
                pass

            return None

        def _sort_key(t):
            prio_norm = Tarefa.normalizar_prioridade(getattr(t, 'prioridade', 'Importante e Urgente'))
            prio_k = prioridade_rank.get(prio_norm, 1)
            date_k = _parse_date(getattr(t, 'date', None))
            time_k = _parse_time(getattr(t, 'time', None))
            return (
                prio_k,
                date_k.toJulianDay() if date_k else 99999999,
                time_k if time_k else (99, 99),
                (getattr(t, 'titulo', '') or '').lower(),
            )

        tarefas_doing = [t for t in getattr(self.tarefas, 'tarefas', []) if getattr(t, 'status', '') == "Doing"]
        tarefas_doing.sort(key=_sort_key)

        for t in tarefas_doing:
            prioridade_norm = Tarefa.normalizar_prioridade(getattr(t, 'prioridade', 'Importante e Urgente'))
            emoji = {
                "Importante e Urgente": "🔴",
                "Importante, mas Não Urgente": "🟠",
                "Não Importante, mas Urgente": "🟡",
                "Não Importante e Não Urgente": "🟢",
            }.get(prioridade_norm, "🔴")

            texto = f"{emoji} {t.titulo} — 🍅 {t.pomodoros_completados}"
            item = QListWidgetItem(texto)
            item.setData(Qt.UserRole, getattr(t, 'id', None))

            tooltip_lines = []
            date_iso = getattr(t, 'date', None)
            time_str = getattr(t, 'time', None)

            if date_iso:
                try:
                    qd = QDate.fromString(str(date_iso), Qt.ISODate)

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
                        date_human = str(date_iso)

                    tooltip_lines.append(f"{QCoreApplication.translate('App', 'Data') or 'Data'}: {date_human}")

                except Exception:
                    pass

            if time_str:
                tooltip_lines.append(f"{QCoreApplication.translate('App', 'Horário') or 'Horário'}: {time_str}")

            file_path = getattr(t, 'file_path', None)

            if file_path:
                try:
                    font = item.font() or QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setForeground(Qt.blue)

                except Exception as e:
                    logger.error(f"Erro ao destacar tarefa com arquivo vinculado na coluna lateral: {str(e)}", exc_info=True)

                tooltip_lines.append(f"{QCoreApplication.translate('App', 'Arquivo') or 'Arquivo'}: {file_path}")

            desc = getattr(t, 'descricao', None)

            if desc:
                tooltip_lines.append(f"{QCoreApplication.translate('App', 'Descrição') or 'Descrição'}: {desc}")

            prio = getattr(t, 'prioridade', None)

            if prio is not None and prio != "":
                try:
                    prio_t = prioridade_para_texto(prio, self)

                except Exception:
                    prio_t = str(prio)

                tooltip_lines.append(f"{QCoreApplication.translate('App', 'Prioridade') or 'Prioridade'}: {prio_t}")

            if tooltip_lines:
                item.setToolTip("\n".join(tooltip_lines))

            self.col_doing_timer_list.addItem(item)

    except Exception as e:
        logger.error(f"Erro ao atualizar coluna de tarefas em progresso no timer: {str(e)}", exc_info=True)
