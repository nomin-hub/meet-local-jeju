"""Retriever for JEJU-KB knowledge chunks.

Provides query-time similarity search over the persisted ChromaDB vector store
built by `rag.vectordb.build_vector_store`. This module only retrieves relevant
chunks with their metadata — LLM answer generation and the Streamlit UI are not
implemented here.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python3 rag/retriever.py` to resolve `rag.vectordb` even though running
# the file directly does not put the project root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag.vectordb import load_vector_store

# Lazily-initialized, process-wide vector store, so repeated retrieval calls
# (e.g. multiple queries in one session) don't re-open the persisted ChromaDB
# collection or re-instantiate the embedding client on every call.
_VECTOR_STORE_CACHE: Chroma | None = None


def _get_vector_store() -> Chroma:
    """Return the process-wide JEJU-KB vector store, loading it on first use."""
    global _VECTOR_STORE_CACHE
    if _VECTOR_STORE_CACHE is None:
        _VECTOR_STORE_CACHE = load_vector_store()
    return _VECTOR_STORE_CACHE


def retrieve_relevant_documents(query: str, k: int = 4) -> list[Document]:
    """Retrieve the top-k JEJU-KB chunks most relevant to a natural-language query.

    Loads the persisted vector store (see `rag.vectordb.load_vector_store`) and
    runs a similarity search against it. Each returned `Document` carries its
    full chunk metadata (front matter fields plus `parent_id`, `chunk_index`,
    `chunk_id`, `file_path`), unchanged from what was stored at ingestion time.

    Args:
        query: Natural-language search query.
        k: Number of chunks to return. Defaults to 4.

    Returns:
        A list of up to `k` `Document` objects, ordered from most to least
        relevant.

    Raises:
        FileNotFoundError: if no vector store has been built yet (see
            `rag.vectordb.build_vector_store`).
    """
    vector_store = _get_vector_store()
    return vector_store.similarity_search(query, k=k)


def format_retrieval_results(documents: list[Document]) -> str:
    """Format retrieved documents into a human-readable string for debugging.

    For each document, prints its rank, title, category, parent_id, chunk_id,
    and a short single-line preview of its content.

    Args:
        documents: Documents to format, typically the output of
            `retrieve_relevant_documents`.

    Returns:
        A multi-line, human-readable string summarizing the results. Returns
        `"(no results)"` if `documents` is empty.
    """
    if not documents:
        return "(no results)"

    lines: list[str] = []
    for rank, document in enumerate(documents, start=1):
        meta = document.metadata
        preview = " ".join(document.page_content.split())
        if len(preview) > 160:
            preview = preview[:160].rstrip() + "..."

        lines.append(
            f"{rank}. title={meta.get('title')!r} | category={meta.get('category')} | "
            f"parent_id={meta.get('parent_id')} | chunk_id={meta.get('chunk_id')}\n"
            f"   preview: {preview}"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    test_queries = [
        "I want to learn about haenyeo culture",
        "What can I experience in October in Jeju?",
        "I want to meet local people at a traditional market",
        "Tell me about Jeju stone walls",
    ]

    for test_query in test_queries:
        print(f"Query: {test_query!r}")
        top_results = retrieve_relevant_documents(test_query, k=3)
        print(format_retrieval_results(top_results))
        print()
