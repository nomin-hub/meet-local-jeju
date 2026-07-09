"""Text splitter for JEJU-KB knowledge documents.

Splits LangChain `Document` objects produced by `rag.loader.load_knowledge_documents`
into retrieval-sized chunks using LangChain's `RecursiveCharacterTextSplitter`. Each
resulting chunk is itself a `Document`, carrying all of its parent document's front
matter metadata plus chunk-specific identifiers.

This module only performs chunking. Embedding, vector storage, and retrieval are
handled by other modules in `rag/` and are not implemented here.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python3 rag/splitter.py` to resolve `rag.loader` even though running the
# file directly does not put the project root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loader import load_knowledge_documents

# Default chunking parameters, in characters.
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120


def split_documents(
    documents: list[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Document]:
    """Split JEJU-KB documents into retrieval-sized chunks.

    Each source document is split independently using
    `RecursiveCharacterTextSplitter`, so chunk numbering always starts at 0 for
    each document rather than continuing across documents.

    Every resulting chunk `Document` carries:
      - All metadata from its parent document (front matter fields + `file_path`).
      - `parent_id`: the parent document's KDS `id` (e.g. `STORY-0001`).
      - `chunk_index`: zero-based position of the chunk within its parent document.
      - `chunk_id`: `{parent_id}::chunk-{chunk_index}` (e.g. `STORY-0001::chunk-0`).

    Args:
        documents: Source documents to split, typically from
            `rag.loader.load_knowledge_documents`. Each document's metadata must
            include an `id` field.
        chunk_size: Maximum chunk size, in characters. Defaults to 800.
        chunk_overlap: Number of overlapping characters between consecutive
            chunks of the same document. Defaults to 120.

    Returns:
        A flat list of chunk `Document` objects, in the same document order as
        the input, with chunks in ascending `chunk_index` order within each
        document.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks: list[Document] = []
    for document in documents:
        parent_id = document.metadata["id"]
        chunk_texts = text_splitter.split_text(document.page_content)

        for chunk_index, chunk_text in enumerate(chunk_texts):
            chunk_metadata = dict(document.metadata)
            chunk_metadata["parent_id"] = parent_id
            chunk_metadata["chunk_index"] = chunk_index
            chunk_metadata["chunk_id"] = f"{parent_id}::chunk-{chunk_index}"

            chunks.append(Document(page_content=chunk_text, metadata=chunk_metadata))

    return chunks


if __name__ == "__main__":
    original_documents = load_knowledge_documents()
    document_chunks = split_documents(original_documents)

    print(f"Loaded {len(original_documents)} original document(s).")
    print(f"Produced {len(document_chunks)} chunk(s).\n")

    print("First 5 chunks:")
    for chunk in document_chunks[:5]:
        meta = chunk.metadata
        print(
            f"- chunk_id={meta.get('chunk_id')} | "
            f"title={meta.get('title')!r} | "
            f"category={meta.get('category')}"
        )
