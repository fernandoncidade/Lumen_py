from __future__ import annotations


class WordTimestamp:
    def __init__(self, text: str, offset_ms: int, duration_ms: int, text_offset: int = 0):
        self.text = text
        self.offset_ms = offset_ms
        self.duration_ms = duration_ms
        self.text_offset = text_offset

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "offset_ms": self.offset_ms,
            "duration_ms": self.duration_ms,
            "text_offset": self.text_offset,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "WordTimestamp":
        return cls(
            text=d.get("text", ""),
            offset_ms=d.get("offset_ms", 0),
            duration_ms=d.get("duration_ms", 0),
            text_offset=d.get("text_offset", 0),
        )
