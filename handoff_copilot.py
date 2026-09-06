"""Turn an Entire Checkpoint record into a concise Markdown handoff brief."""

from __future__ import annotations

import json
from typing import Any, Mapping


SECTION_FIELDS = {
    "Intent": ("intent",),
    "What's Done": ("done", "completed", "files_changed", "reasoning"),
    "What's Unfinished": ("unfinished", "pending", "next_steps"),
    "Risks": ("risks", "blockers", "caveats"),
    "Verification Checklist": ("verification_checklist", "verification", "checks"),
}


def generate_handoff_brief(checkpoint: Mapping[str, Any] | str) -> str:
    """Read an Entire Checkpoint mapping or JSON string and format a Markdown brief."""
    if isinstance(checkpoint, str):
        checkpoint = json.loads(checkpoint)

    sections: list[str] = []
    for heading, field_names in SECTION_FIELDS.items():
        values = [checkpoint[name] for name in field_names if checkpoint.get(name)]
        sections.append(f"## {heading}\n\n{_format_values(values)}")
    return "\n\n".join(sections) + "\n"


def _format_values(values: list[Any]) -> str:
    """Render checkpoint values as readable text or Markdown bullets."""
    if not values:
        return "- Not provided"

    lines: list[str] = []
    for value in values:
        if isinstance(value, (list, tuple)):
            lines.extend(f"- {item}" for item in value)
        elif isinstance(value, Mapping):
            lines.extend(f"- {key}: {item}" for key, item in value.items())
        else:
            lines.append(f"- {value}")
    return "\n".join(lines)
