"""
GKeepSync - Markdown Converter
Convert Google Keep note dict → .md file content.
"""

import re
from datetime import datetime


def sanitize_filename(title: str) -> str:
    """Convert note title to safe filename."""
    # Replace special chars with underscore
    safe = re.sub(r'[<>:"/\\|?*]', '_', title)
    # Replace multiple spaces/underscores
    safe = re.sub(r'[\s_]+', '_', safe).strip('_')
    # Limit length
    if len(safe) > 100:
        safe = safe[:100]
    # Fallback
    if not safe:
        safe = "untitled"
    return safe


def note_to_markdown(note: dict) -> str:
    """
    Convert a note dict to markdown string with YAML frontmatter.
    
    Frontmatter includes: title, tags, created, updated, pinned, color, keep_id
    Body includes: text content or checklist items
    """
    lines = []

    # --- YAML Frontmatter ---
    lines.append("---")
    lines.append(f'title: "{_escape_yaml(note["title"])}"')

    if note.get("labels"):
        tags_str = ", ".join(f'"{l}"' for l in note["labels"])
        lines.append(f"tags: [{tags_str}]")

    if note.get("created"):
        lines.append(f"created: {_format_dt(note['created'])}")
    if note.get("updated"):
        lines.append(f"updated: {_format_dt(note['updated'])}")

    if note.get("pinned"):
        lines.append("pinned: true")
    if note.get("color"):
        lines.append(f"color: {note['color']}")

    lines.append(f'keep_id: "{note["id"]}"')
    lines.append("---")
    lines.append("")

    # --- Title ---
    lines.append(f"# {note['title']}")
    lines.append("")

    # --- Body ---
    if note.get("items"):
        # Checklist note
        for item in note["items"]:
            checked = "x" if item.get("checked") else " "
            lines.append(f"- [{checked}] {item['text']}")
    elif note.get("text"):
        lines.append(note["text"])

    lines.append("")
    return "\n".join(lines)


def _escape_yaml(text: str) -> str:
    """Escape special chars for YAML string."""
    return text.replace('"', '\\"').replace("\n", " ")


def _format_dt(dt) -> str:
    """Format datetime for frontmatter."""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)
