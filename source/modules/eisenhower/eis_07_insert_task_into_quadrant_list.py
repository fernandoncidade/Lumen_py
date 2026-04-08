from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QFont
from source.modules.eisenhower.services.svc_09_prioridade_para_texto import prioridade_para_texto
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("App", text)

def insert_task_into_quadrant_list(self, lst, item):
    try:
        data = item.data(Qt.UserRole) or {}
        time_str = data.get("time")
        if not time_str:
            try:
                tooltip_lines = []
                fp = data.get("file_path")
                if fp:
                    tooltip_lines.append((get_text("Arquivo") or "Arquivo") + f": {fp}")
                    try:
                        font = item.font() or QFont()
                        font.setBold(True)
                        item.setFont(font)

                        try:
                            item.setForeground(Qt.blue)

                        except Exception as e:
                            logger.error(f"Falha ao definir cor do item: {e}", exc_info=True)

                    except Exception as e:
                        logger.error(f"Falha ao definir fonte do item: {e}", exc_info=True)

                ds = data.get("date")
                if ds:
                    try:
                        from PySide6.QtCore import QDate
                        qd = QDate.fromString(ds, Qt.ISODate)
                        if qd.isValid() and hasattr(self, "date_input"):
                            date_human = qd.toString(self.date_input.displayFormat())

                        else:
                            date_human = ds

                    except Exception as e:
                        logger.error(f"Falha ao converter data: {e}", exc_info=True)
                        date_human = ds

                    tooltip_lines.append((get_text("Data") or "Data") + f": {date_human}")

                if time_str:
                    tooltip_lines.append((get_text("Horário") or "Horário") + f": {time_str}")

                desc = data.get("description")
                if desc:
                    tooltip_lines.append((get_text("Descrição") or "Descrição") + f": {desc}")

                prio = data.get("priority")
                if prio is not None and prio != "":
                    try:
                        prio_t = prioridade_para_texto(prio, self)

                    except Exception:
                        prio_t = str(prio)

                    tooltip_lines.append((get_text("Prioridade") or "Prioridade") + f": {prio_t}")

                if tooltip_lines:
                    try:
                        item.setToolTip("\n".join(tooltip_lines))

                    except Exception as e:
                        logger.error(f"Falha ao definir tooltip do item: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"Erro ao preparar tooltip do item: {e}", exc_info=True)

            lst.addItem(item)
            return

        if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
            lst.clear()

        label = self._time_group_label(time_str)

        header_index = None
        insert_header_index = None
        existing_headers = []

        for i in range(lst.count()):
            it = lst.item(i)
            if not it:
                continue

            if self._is_group_header(it):
                existing_headers.append((i, it.text()))

        for idx, text in existing_headers:
            if text == label:
                header_index = idx
                break

        if header_index is None:
            try:
                hour = int(label.split(":")[0])

            except Exception as e:
                logger.error(f"Falha ao converter hora do rótulo do grupo: {e}", exc_info=True)
                hour = 0

            insert_header_index = lst.count()
            for idx, text in existing_headers:
                try:
                    h2 = int(text.split(":")[0])

                except Exception as e:
                    logger.error(f"Falha ao converter hora do rótulo do grupo: {e}", exc_info=True)
                    h2 = 0

                if hour < h2:
                    insert_header_index = idx
                    break

            from PySide6.QtWidgets import QListWidgetItem
            header = QListWidgetItem(label)
            from PySide6.QtCore import Qt as _Qt
            header.setFlags((header.flags() & ~_Qt.ItemIsSelectable) & ~_Qt.ItemIsEnabled)
            header.setData(_Qt.UserRole + 1, "group_header")
            lst.insertItem(insert_header_index, header)
            header_index = insert_header_index

        start = header_index + 1
        end = lst.count()
        for i in range(start, lst.count()):
            it = lst.item(i)
            if it and self._is_group_header(it):
                end = i
                break

        new_key = (self._time_key(time_str), (data.get("text") or item.text()).lower())
        pos = end
        for i in range(start, end):
            it = lst.item(i)
            idata = it.data(Qt.UserRole) or {}
            ikey = (self._time_key(idata.get("time")), (idata.get("text") or it.text()).lower())
            if new_key < ikey:
                pos = i
                break

        try:
            tooltip_lines = []
            fp = data.get("file_path")
            if fp:
                tooltip_lines.append((get_text("Arquivo") or "Arquivo") + f": {fp}")
                try:
                    font = item.font() or QFont()
                    font.setBold(True)
                    item.setFont(font)

                    try:
                        item.setForeground(Qt.blue)

                    except Exception:
                        pass

                except Exception:
                    pass

            ds = data.get("date")
            if ds:
                try:
                    from PySide6.QtCore import QDate
                    qd = QDate.fromString(ds, Qt.ISODate)
                    if qd.isValid() and hasattr(self, "date_input"):
                        date_human = qd.toString(self.date_input.displayFormat())

                    else:
                        date_human = ds

                except Exception as e:
                    logger.error(f"Falha ao converter data: {e}", exc_info=True)
                    date_human = ds

                tooltip_lines.append((get_text("Data") or "Data") + f": {date_human}")

            if time_str:
                tooltip_lines.append((get_text("Horário") or "Horário") + f": {time_str}")

            desc = data.get("description")
            if desc:
                tooltip_lines.append((get_text("Descrição") or "Descrição") + f": {desc}")

            prio = data.get("priority")
            if prio is not None and prio != "":
                    try:
                        prio_t = prioridade_para_texto(prio, self)

                    except Exception:
                        prio_t = str(prio)

                    tooltip_lines.append((get_text("Prioridade") or "Prioridade") + f": {prio_t}")

            if tooltip_lines:
                try:
                    item.setToolTip("\n".join(tooltip_lines))

                except Exception as e:
                    logger.error(f"Falha ao definir tooltip do item: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erro ao preparar tooltip do item: {e}", exc_info=True)

        lst.insertItem(pos, item)

    except Exception as e:
        logger.error(f"Erro ao inserir tarefa na lista do quadrante: {e}", exc_info=True)
