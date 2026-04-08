import json
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox
from source.utils.LogManager import LogManager
from source.utils.task_identity import ensure_task_id
logger = LogManager.get_logger()

_QUADRANT_KEYS = (
    "quadrant1",
    "quadrant1_completed",
    "quadrant2",
    "quadrant2_completed",
    "quadrant3",
    "quadrant3_completed",
    "quadrant4",
    "quadrant4_completed",
)

_XLSX_HEADERS = ("id", "text", "date", "time", "file_path", "description", "priority")
_PDF_SENTINEL_BEGIN = "LUMEN_EISENHOWER_EXPORT_V1_BEGIN"
_PDF_SENTINEL_END = "LUMEN_EISENHOWER_EXPORT_V1_END"

def _normalize_priority(value, default_priority):
    if isinstance(value, bool):
        return default_priority

    try:
        parsed = int(value)

        if 1 <= parsed <= 4:
            return parsed

    except Exception:
        pass

    if isinstance(value, str):
        txt = value.strip().lower()

        if "importante e urgente" in txt:
            return 1

        if "importante" in txt and "nao urgente" in txt:
            return 2

        if "nao importante" in txt and "urgente" in txt:
            return 3

        if "nao importante" in txt and "nao urgente" in txt:
            return 4

    return default_priority

def _is_supported_value(value):
    return value is None or isinstance(value, (str, int, float, bool))

def _validate_tasks_structure(tasks):
    if not isinstance(tasks, dict):
        raise ValueError("Estrutura inválida: raiz deve ser objeto.")

    for key in _QUADRANT_KEYS:
        if key not in tasks or not isinstance(tasks[key], list):
            raise ValueError(f"Estrutura inválida: lista '{key}' ausente ou inválida.")

    for key in _QUADRANT_KEYS:
        for idx, entry in enumerate(tasks[key]):
            if not isinstance(entry, dict):
                raise ValueError(f"Estrutura inválida: item {idx} de '{key}' deve ser objeto.")

            if not entry.get("id"):
                raise ValueError(f"Estrutura inválida: item {idx} de '{key}' sem campo 'id'.")

            text = entry.get("text")

            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"Estrutura inválida: item {idx} de '{key}' sem 'text' válido.")

            for field in ("date", "time", "file_path", "description", "priority"):
                if field in entry and not _is_supported_value(entry.get(field)):
                    raise ValueError(f"Estrutura inválida: campo '{field}' inválido em '{key}' item {idx}.")

def _build_item(app, text, date_iso, time_str, completed, payload):
    from PySide6.QtCore import QCoreApplication, QDate

    date_format = app.date_input.displayFormat() if hasattr(app, "date_input") and app.date_input is not None else "dd/MM/yyyy"
    display_text = text
    tooltip_lines = []
    get_text = lambda s: QCoreApplication.translate("App", s)

    if date_iso:
        qd = QDate.fromString(str(date_iso), Qt.ISODate)

        if qd.isValid():
            date_human = qd.toString(date_format)
            display_text = f"{text} — {date_human} {time_str}" if time_str else f"{text} — {date_human}"
            tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

        else:
            display_text = f"{text} — {date_iso} {time_str}" if time_str else f"{text} — {date_iso}"

    if time_str:
        tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

    if payload.get("file_path"):
        tooltip_lines.append(f"{get_text('Arquivo') or 'Arquivo'}: {payload.get('file_path')}")

    if payload.get("description"):
        tooltip_lines.append(f"{get_text('Descrição') or 'Descrição'}: {payload.get('description')}")

    item = QListWidgetItem(display_text)
    item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
    item.setData(Qt.UserRole, payload)

    if tooltip_lines:
        item.setToolTip("\n".join(tooltip_lines))

    return item

def _populate_ui_from_tasks(self, app, tasks):
    list_specs = (
        ("quadrant1", app.quadrant1_list, False, 1),
        ("quadrant1_completed", app.quadrant1_completed_list, True, 1),
        ("quadrant2", app.quadrant2_list, False, 2),
        ("quadrant2_completed", app.quadrant2_completed_list, True, 2),
        ("quadrant3", app.quadrant3_list, False, 3),
        ("quadrant3_completed", app.quadrant3_completed_list, True, 3),
        ("quadrant4", app.quadrant4_list, False, 4),
        ("quadrant4_completed", app.quadrant4_completed_list, True, 4),
    )

    for _, lst, _, _ in list_specs:
        lst.clear()

    found_any = False

    for key, lst, completed, default_priority in list_specs:
        entries = tasks.get(key, [])

        if not isinstance(entries, list):
            continue

        for entry in entries:
            if not isinstance(entry, dict):
                continue

            payload = dict(entry)
            payload["text"] = str(payload.get("text", "")).strip()

            if not payload["text"]:
                continue

            payload["priority"] = _normalize_priority(payload.get("priority"), default_priority)
            ensure_task_id(payload)
            payload["date"] = payload.get("date")
            payload["time"] = payload.get("time")

            item = _build_item(app, payload["text"], payload.get("date"), payload.get("time"), completed, payload)
            found_any = True

            try:
                app.insert_task_into_quadrant_list(lst, item)

            except Exception as e:
                logger.error(f"Erro ao inserir tarefa na lista do quadrante: {e}", exc_info=True)
                lst.addItem(item)

    if not found_any:
        raise ValueError("Arquivo sem tarefas válidas.")

def abrir_arquivo(self, app=None):
    app = self._resolve_app(app)
    path, _ = QFileDialog.getOpenFileName(app, self.get_text("Abrir"), os.path.expanduser("~"), "JSON (*.json);;Excel (*.xlsx);;PDF (*.pdf)")

    if not path:
        return

    ext = os.path.splitext(path)[1].lower()

    if ext == ".xlsx":
        try:
            from openpyxl import load_workbook

        except Exception as e:
            logger.error(f"openpyxl não está disponível: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), self.get_text("openpyxl não está disponível."))
            return

        try:
            wb = load_workbook(path, read_only=True, data_only=True)
            tasks = {k: [] for k in _QUADRANT_KEYS}

            for key in _QUADRANT_KEYS:
                if key not in wb.sheetnames:
                    raise ValueError(f"Aba obrigatória ausente: {key}")

                ws = wb[key]
                header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), None)
                header = tuple((str(x).strip() if x is not None else "") for x in (header_row or ()))

                if header[:len(_XLSX_HEADERS)] != _XLSX_HEADERS:
                    raise ValueError(f"Cabeçalho inválido na aba '{key}'.")

                for row in ws.iter_rows(min_row=2, max_col=len(_XLSX_HEADERS), values_only=True):
                    if row is None or all(v is None or str(v).strip() == "" for v in row):
                        continue

                    entry = {
                        "id": str(row[0]).strip() if row[0] is not None else "",
                        "text": str(row[1]).strip() if row[1] is not None else "",
                        "date": str(row[2]).strip() if row[2] is not None and str(row[2]).strip() else None,
                        "time": str(row[3]).strip() if row[3] is not None and str(row[3]).strip() else None,
                    }

                    if row[4] is not None and str(row[4]).strip():
                        entry["file_path"] = str(row[4]).strip()

                    if row[5] is not None and str(row[5]).strip():
                        entry["description"] = str(row[5])

                    if row[6] is not None and str(row[6]).strip():
                        entry["priority"] = row[6]

                    tasks[key].append(entry)

            _validate_tasks_structure(tasks)
            _populate_ui_from_tasks(self, app, tasks)

            app.save_tasks()

            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar lista de tarefas no calendário: {e}", exc_info=True)

            QMessageBox.information(app, self.get_text("Abrir"), self.get_text("Arquivo importado com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao importar arquivo XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".pdf":
        try:
            from PyPDF2 import PdfReader

        except Exception as e:
            logger.error(f"PyPDF2 não está disponível: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), self.get_text("PyPDF2 não está disponível para ler PDF."))
            return

        try:
            reader = PdfReader(path)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"

            begin_idx = text.find(_PDF_SENTINEL_BEGIN)
            end_idx = text.find(_PDF_SENTINEL_END)

            if begin_idx == -1 or end_idx == -1 or end_idx <= begin_idx:
                QMessageBox.warning(app, self.get_text("Abrir"), self.get_text("PDF não está no formato compatível."))
                return

            payload_json = text[begin_idx + len(_PDF_SENTINEL_BEGIN):end_idx].strip()
            tasks = json.loads(payload_json)

            _validate_tasks_structure(tasks)
            _populate_ui_from_tasks(self, app, tasks)

            app.save_tasks()

            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar lista de tarefas no calendário (PDF): {e}", exc_info=True)

            QMessageBox.information(app, self.get_text("Abrir"), self.get_text("PDF importado com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao importar arquivo PDF: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".json":
        try:
            with open(path, "r", encoding="utf-8") as f:
                tasks = json.load(f)

            _populate_ui_from_tasks(self, app, tasks)

            app.save_tasks()

            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar lista de tarefas no calendário (JSON): {e}", exc_info=True)

            QMessageBox.information(app, self.get_text("Abrir"), self.get_text("Arquivo importado com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao importar arquivo JSON: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    else:
        QMessageBox.warning(app, self.get_text("Abrir"), self.get_text("Formato de arquivo não suportado."))
