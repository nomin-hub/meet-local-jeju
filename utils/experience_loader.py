"""Loader for Meet Local Jeju's experience card dataset.

Reads the JSON experience cards under `data/experiences/` (prototype content
for the "Featured Local Ideas" board — see `utils/ui_helpers.py`) and returns
them as validated plain dictionaries. This module has no dependency on the
RAG pipeline in `rag/`; it only loads and validates the experience-card JSON
files. Each card's `related_kb_ids` field is a pointer to real JEJU-KB
documents, but this loader does not read or validate against `knowledge/`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

EXPERIENCES_DIR = Path(__file__).resolve().parent.parent / "data" / "experiences"

REQUIRED_FIELDS = [
    "id",
    "title",
    "category",
    "area",
    "season",
    "duration",
    "best_for",
    "transportation",
    "description",
    "local_story",
    "related_kb_ids",
    "status",
    "booking_status",
    "source_note",
]


class ExperienceCardError(ValueError):
    """Raised when a file under data/experiences/ is missing or malformed."""


def _validate_card(card: dict[str, Any], file_path: Path) -> None:
    """Ensure all required experience-card fields are present and non-empty.

    Raises:
        ExperienceCardError: listing the file path and every missing field.
    """
    missing = [
        field
        for field in REQUIRED_FIELDS
        if field not in card or card[field] in (None, "", [])
    ]
    if missing:
        raise ExperienceCardError(
            f"Missing required field(s) {missing} in file: {file_path}"
        )


def load_experience_cards(experiences_dir: Path | str = EXPERIENCES_DIR) -> list[dict[str, Any]]:
    """Load and validate all experience cards from `data/experiences/`.

    Args:
        experiences_dir: Directory to scan for `*.json` experience card
            files. Defaults to the project's `data/experiences/` directory.

    Returns:
        A list of card dictionaries, sorted by `id`.

    Raises:
        ExperienceCardError: if a file is not valid JSON, is not a JSON
            object, or is missing one or more required fields. The error
            message identifies the offending file and, where applicable,
            the missing fields.
    """
    root = Path(experiences_dir)

    cards: list[dict[str, Any]] = []
    for file_path in sorted(root.glob("*.json")):
        try:
            card = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ExperienceCardError(f"Invalid JSON in file: {file_path} ({exc})") from exc

        if not isinstance(card, dict):
            raise ExperienceCardError(f"{file_path}: experience card must be a JSON object.")

        _validate_card(card, file_path)
        cards.append(card)

    cards.sort(key=lambda card: card["id"])
    return cards


if __name__ == "__main__":
    loaded_cards = load_experience_cards()

    print(f"Loaded {len(loaded_cards)} experience card(s) from {EXPERIENCES_DIR}\n")
    for card in loaded_cards:
        print(f"- {card['id']} | {card['title']}")

    print("\nExperience card dataset loaded successfully.")
