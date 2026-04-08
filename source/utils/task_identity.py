from __future__ import annotations
from typing import Any
from uuid import uuid4

def _to_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()

def _read(source: Any, *keys: str) -> Any:
    if isinstance(source, dict):
        for key in keys:
            if key in source:
                return source.get(key)

        return None

    for key in keys:
        if hasattr(source, key):
            return getattr(source, key)

    return None

def normalize_priority(value: Any) -> str:
    text = _to_text(value)

    if not text:
        return "Importante e Urgente"

    try:
        if text.isdigit():
            pnum = int(text)
            mapping = {
                1: "Importante e Urgente",
                2: "Importante, mas Nao Urgente",
                3: "Nao Importante, mas Urgente",
                4: "Nao Importante e Nao Urgente",
            }
            return mapping.get(pnum, "Importante e Urgente")

    except Exception:
        pass

    lowered = text.lower()

    if "importante" in lowered and "urgente" in lowered and "nao" not in lowered and "não" not in lowered:
        return "Importante e Urgente"

    if "importante" in lowered and ("nao urgente" in lowered or "não urgente" in lowered):
        return "Importante, mas Nao Urgente"

    if ("nao importante" in lowered or "não importante" in lowered) and "urgente" in lowered:
        return "Nao Importante, mas Urgente"

    if ("nao importante" in lowered or "não importante" in lowered) and ("nao urgente" in lowered or "não urgente" in lowered):
        return "Nao Importante e Nao Urgente"

    return text

def ensure_task_id(data: dict) -> str:
    task_id = _to_text(data.get("id"))

    if not task_id:
        task_id = str(uuid4())
        data["id"] = task_id

    return task_id

def task_identity_signature(source: Any) -> tuple[str, str, str, str, str, str]:
    task_id = _to_text(_read(source, "id"))
    title = _to_text(_read(source, "titulo", "text"))
    date_value = _to_text(_read(source, "date", "date_iso"))
    time_value = _to_text(_read(source, "time"))
    description = _to_text(_read(source, "descricao", "description", "desc"))
    priority = normalize_priority(_read(source, "prioridade", "priority"))
    return (task_id, title, date_value, time_value, description, priority)

def tasks_match(source_a: Any, source_b: Any) -> bool:
    a_id, a_title, a_date, a_time, a_desc, a_prio = task_identity_signature(source_a)
    b_id, b_title, b_date, b_time, b_desc, b_prio = task_identity_signature(source_b)

    if a_id and b_id:
        return a_id == b_id

    return (
        a_title == b_title
        and a_date == b_date
        and a_time == b_time
        and a_desc == b_desc
        and a_prio == b_prio
    )
