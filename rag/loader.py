"""Loader for JEJU-KB knowledge documents.

Reads Markdown knowledge objects under `knowledge/` (see `knowledge/KDS.md` for the
Knowledge Document Standard each file must follow) and converts them into LangChain
`Document` objects: YAML front matter becomes `metadata`, the remaining Markdown
becomes `page_content`.

This module only loads and validates documents. Chunking, embedding, vector storage,
and retrieval are handled by other modules in `rag/` and are not implemented here.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

import yaml
from langchain_core.documents import Document

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

# Files that live inside knowledge/ but are not knowledge documents themselves.
IGNORED_FILENAMES = {"README.md", "KDS.md"}

# Required front matter fields, per knowledge/KDS.md, Section 3.
REQUIRED_METADATA_FIELDS = [
    "id",
    "title",
    "category",
    "subcategory",
    "island",
    "region",
    "season",
    "tags",
    "language",
    "source",
    "last_updated",
]


class KnowledgeDocumentError(ValueError):
    """Raised when a file under knowledge/ does not conform to the KDS format."""


def _iter_markdown_files(root: Path) -> list[Path]:
    """Return all KDS-eligible Markdown files under root, sorted for stable output.

    Skips README.md, KDS.md, hidden files, and any file/directory whose name starts
    with a dot (e.g. .gitkeep, .git/). Non-Markdown files are excluded by construction,
    since only *.md files are globbed.
    """
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if path.name in IGNORED_FILENAMES:
            continue
        relative_parts = path.relative_to(root).parts
        if any(part.startswith(".") for part in relative_parts):
            continue
        files.append(path)
    return sorted(files)


def _normalize_metadata_types(metadata: dict[str, Any]) -> dict[str, Any]:
    """Coerce YAML-parsed values into plain, JSON/vector-store-safe types.

    PyYAML auto-parses unquoted `YYYY-MM-DD` values (e.g. `last_updated`) into
    `datetime.date` objects. Downstream consumers (JSON serialization, ChromaDB
    metadata, which only accepts str/int/float/bool/list/None) expect plain
    strings, so date/datetime values are converted to their ISO 8601 form here,
    right after parsing, so every consumer of this metadata sees consistent types.
    """
    normalized = dict(metadata)
    for key, value in normalized.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            normalized[key] = value.isoformat()
    return normalized


def _split_front_matter(text: str, file_path: Path) -> tuple[dict[str, Any], str]:
    """Split raw Markdown text into a parsed front matter dict and the body text.

    Raises:
        KnowledgeDocumentError: if the file has no YAML front matter block, or the
            front matter is not a valid YAML mapping.
    """
    if not text.startswith("---"):
        raise KnowledgeDocumentError(
            f"{file_path}: missing YAML front matter (file must start with '---')."
        )

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise KnowledgeDocumentError(f"{file_path}: malformed front matter block.")

    _, raw_front_matter, body = parts
    metadata = yaml.safe_load(raw_front_matter) or {}
    if not isinstance(metadata, dict):
        raise KnowledgeDocumentError(f"{file_path}: front matter must be a YAML mapping.")
    metadata = _normalize_metadata_types(metadata)

    return metadata, body.strip()


def _validate_metadata(metadata: dict[str, Any], file_path: Path) -> None:
    """Ensure all required KDS fields are present and non-empty.

    Raises:
        KnowledgeDocumentError: listing the file path and every missing field.
    """
    missing = [
        field
        for field in REQUIRED_METADATA_FIELDS
        if field not in metadata or metadata[field] in (None, "", [])
    ]
    if missing:
        raise KnowledgeDocumentError(
            f"Missing required metadata field(s) {missing} in file: {file_path}"
        )


def load_knowledge_documents(knowledge_dir: Path | str = KNOWLEDGE_DIR) -> list[Document]:
    """Load all JEJU-KB knowledge documents into LangChain Document objects.

    Recursively scans `knowledge_dir` for KDS-eligible Markdown files (see
    `_iter_markdown_files`), parses each file's YAML front matter, and validates
    that all required KDS fields are present.

    Args:
        knowledge_dir: Root directory to scan. Defaults to the project's `knowledge/`
            directory.

    Returns:
        A list of `Document` objects, one per knowledge file, where `page_content`
        is the Markdown body and `metadata` is the parsed front matter plus a
        `file_path` field (path relative to the project root).

    Raises:
        KnowledgeDocumentError: if any file is missing front matter, has malformed
            front matter, or is missing one or more required metadata fields. The
            error message identifies the offending file and, where applicable, the
            missing fields.
    """
    root = Path(knowledge_dir).resolve()
    project_root = root.parent

    documents: list[Document] = []
    for file_path in _iter_markdown_files(root):
        text = file_path.read_text(encoding="utf-8")
        metadata, body = _split_front_matter(text, file_path)
        _validate_metadata(metadata, file_path)

        document_metadata = dict(metadata)
        document_metadata["file_path"] = str(file_path.relative_to(project_root))

        documents.append(Document(page_content=body, metadata=document_metadata))

    return documents


if __name__ == "__main__":
    import sys

    try:
        loaded_documents = load_knowledge_documents()
    except KnowledgeDocumentError as exc:
        print(f"JEJU-KB loading failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(loaded_documents)} knowledge document(s) from {KNOWLEDGE_DIR}\n")
    for doc in loaded_documents:
        meta = doc.metadata
        print(f"- id={meta.get('id')} | title={meta.get('title')!r} | category={meta.get('category')}")
