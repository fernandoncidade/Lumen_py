import json
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox
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

def _build_json_structure(app):
    def _list_to_entries(lst, default_priority):
        entries = []

        if lst is None:
            return entries

        for i in range(lst.count()):
            item = lst.item(i)

            if not item or not (item.flags() & Qt.ItemIsSelectable):
                continue

            data = item.data(Qt.UserRole) or {}
            payload = dict(data) if isinstance(data, dict) else {}
            payload["text"] = str(payload.get("text", item.text() or "")).strip()
            payload["date"] = payload.get("date")
            payload["time"] = payload.get("time")

            if not payload["text"]:
                continue

            ensure_task_id(payload)

            entry = {
                "id": payload.get("id"),
                "text": payload.get("text"),
                "date": payload.get("date"),
                "time": payload.get("time"),
            }

            if payload.get("file_path"):
                entry["file_path"] = payload.get("file_path")

            if payload.get("description"):
                entry["description"] = payload.get("description")

            entry["priority"] = _normalize_priority(payload.get("priority"), default_priority)
            entries.append(entry)

        return entries

    return {
        "quadrant1": _list_to_entries(getattr(app, "quadrant1_list", None), 1),
        "quadrant1_completed": _list_to_entries(getattr(app, "quadrant1_completed_list", None), 1),
        "quadrant2": _list_to_entries(getattr(app, "quadrant2_list", None), 2),
        "quadrant2_completed": _list_to_entries(getattr(app, "quadrant2_completed_list", None), 2),
        "quadrant3": _list_to_entries(getattr(app, "quadrant3_list", None), 3),
        "quadrant3_completed": _list_to_entries(getattr(app, "quadrant3_completed_list", None), 3),
        "quadrant4": _list_to_entries(getattr(app, "quadrant4_list", None), 4),
        "quadrant4_completed": _list_to_entries(getattr(app, "quadrant4_completed_list", None), 4),
    }

def salvar_como(self, app=None):
    app = self._resolve_app(app)

    path, _ = QFileDialog.getSaveFileName(
        app,
        self.get_text("Salvar"),
        os.path.expanduser("~"),
        "JSON (*.json);;Excel (*.xlsx);;PDF (*.pdf)",
    )

    if not path:
        return

    ext = os.path.splitext(path)[1].lower()
    tasks = _build_json_structure(app)

    if ext == ".xlsx":
        try:
            from openpyxl import Workbook

        except Exception as e:
            logger.error(f"openpyxl não está disponível para salvar XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), self.get_text("openpyxl não está disponível para salvar XLSX."))
            return

        try:
            wb = Workbook()
            default_ws = wb.active
            wb.remove(default_ws)

            for key in _QUADRANT_KEYS:
                ws = wb.create_sheet(title=key)

                for col_index, col_name in enumerate(_XLSX_HEADERS, start=1):
                    ws.cell(row=1, column=col_index, value=col_name)

                row_index = 2

                for entry in tasks.get(key, []):
                    ws.cell(row=row_index, column=1, value=entry.get("id"))
                    ws.cell(row=row_index, column=2, value=entry.get("text"))
                    ws.cell(row=row_index, column=3, value=entry.get("date"))
                    ws.cell(row=row_index, column=4, value=entry.get("time"))
                    ws.cell(row=row_index, column=5, value=entry.get("file_path"))
                    ws.cell(row=row_index, column=6, value=entry.get("description"))
                    ws.cell(row=row_index, column=7, value=entry.get("priority"))
                    row_index += 1

            wb.save(path)
            QMessageBox.information(app, self.get_text("Salvar"), self.get_text("Arquivo salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".pdf":
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

        except Exception as e:
            logger.error(f"reportlab não está disponível para salvar PDF: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), self.get_text("reportlab não está disponível para salvar PDF."))
            return

        try:
            payload_json = json.dumps(tasks, ensure_ascii=False, indent=2)
            lines = payload_json.splitlines()

            c = canvas.Canvas(path, pagesize=A4)
            _, height = A4
            left = 36
            top = height - 36
            bottom = 36
            y = top

            c.setFont("Helvetica-Bold", 12)
            c.drawString(left, y, "Lumen Eisenhower Export")
            y -= 20
            c.setFont("Helvetica", 9)
            c.drawString(left, y, "Arquivo estrutural (JSON legivel) para importacao validada.")
            y -= 20

            for line in [_PDF_SENTINEL_BEGIN] + lines + [_PDF_SENTINEL_END]:
                if y <= bottom:
                    c.showPage()
                    y = top
                    c.setFont("Courier", 7)

                c.setFont("Courier", 7)
                c.drawString(left, y, line)
                y -= 9

            c.save()
            QMessageBox.information(app, self.get_text("Salvar"), self.get_text("PDF salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo PDF: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".json":
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)

            QMessageBox.information(app, self.get_text("Salvar"), self.get_text("Arquivo salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo JSON: {e}", exc_info=True)
            QMessageBox.critical(app, self.get_text("Erro"), f"{self.get_text('Erro') or 'Erro'}: {e}")

    else:
        QMessageBox.warning(app, self.get_text("Salvar"), self.get_text("Extensão não suportada."))
