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

# Each inner tuple contains alternate field names for one required piece of context.
REQUIRED_FIELD_GROUPS = {
    "Intent": (("intent",),),
    "What's Done": (("done", "completed", "files_changed"), ("reasoning",)),
    "What's Unfinished": (("unfinished", "pending", "next_steps"),),
    "Risks": (("risks", "blockers", "caveats"),),
    "Verification Checklist": (("verification_checklist", "verification", "checks"),),
}


def generate_handoff_brief(checkpoint: Mapping[str, Any] | str) -> str:
    """Read an Entire Checkpoint mapping or JSON string and format a Markdown brief."""
    if isinstance(checkpoint, str):
        checkpoint = json.loads(checkpoint)

    sections: list[str] = []
    has_unavailable_data = False
    for heading, field_names in SECTION_FIELDS.items():
        values = [
            checkpoint[name]
            for name in field_names
            if _is_available(checkpoint.get(name))
        ]
        is_incomplete = not _has_all_required_groups(
            checkpoint, REQUIRED_FIELD_GROUPS[heading]
        )
        if is_incomplete:
            heading = f"{heading} — Incomplete — data unavailable"
            has_unavailable_data = True
        sections.append(f"## {heading}\n\n{_format_values(values)}")

    context = (
        "Context: PARTIAL — some fields redacted or missing"
        if has_unavailable_data
        else "Context: COMPLETE"
    )
    return f"{context}\n\n" + "\n\n".join(sections) + "\n"


def _has_all_required_groups(
    checkpoint: Mapping[str, Any], required_groups: tuple[tuple[str, ...], ...]
) -> bool:
    """Return whether every required context item has an available field alias."""
    return all(
        any(_is_available(checkpoint.get(field)) for field in group)
        for group in required_groups
    )


def _is_available(value: Any) -> bool:
    """Treat missing, blank, and explicitly redacted values as unavailable."""
    return not (
        value is None
        or (isinstance(value, str) and value.strip().upper() in {"", "[REDACTED]"})
    )


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
