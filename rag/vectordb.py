"""ChromaDB vector store for JEJU-KB knowledge chunks.

Embeds JEJU-KB document chunks (produced by `rag.loader` + `rag.splitter`) using
OpenAI embeddings and persists them in a local ChromaDB collection under
`vector_db/chroma/`. This module builds and loads the vector store only — query-time
retrieval logic (top-k tuning, metadata filtering, MMR, etc.) lives in
`rag/retriever.py` and is not implemented here.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Allow `python3 rag/vectordb.py` to resolve `rag.loader` / `rag.splitter` even
# though running the file directly does not put the project root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from rag.loader import load_knowledge_documents
from rag.splitter import split_documents

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERSIST_DIRECTORY = PROJECT_ROOT / "vector_db" / "chroma"

COLLECTION_NAME = "meet_local_jeju_knowledge"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding_model(model: str = DEFAULT_EMBEDDING_MODEL) -> OpenAIEmbeddings:
    """Return the OpenAI embedding model shared by ingestion and querying.

    Loads environment variables via python-dotenv (so a project-root `.env` file
    is picked up) and reads the API key from `OPENAI_API_KEY`.

    Args:
        model: OpenAI embedding model name. Defaults to `text-embedding-3-small`.

    Returns:
        A configured `OpenAIEmbeddings` instance.

    Raises:
        RuntimeError: if `OPENAI_API_KEY` is not set in the environment or `.env`.
    """
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to a .env file at the project root "
            "(see .env.example) or export it in your environment before running "
            "this module."
        )
    return OpenAIEmbeddings(model=model, api_key=api_key)


def build_vector_store(
    persist_directory: Path | str = PERSIST_DIRECTORY,
    collection_name: str = COLLECTION_NAME,
) -> Chroma:
    """Build the JEJU-KB vector store from scratch and persist it to disk.

    Loads all JEJU-KB knowledge documents (`rag.loader.load_knowledge_documents`),
    splits them into chunks (`rag.splitter.split_documents`), embeds every chunk
    via OpenAI embeddings, and stores the results in a persistent ChromaDB
    collection. Any existing data at `persist_directory` is removed first, so this
    always produces a full, consistent rebuild rather than an incremental update.

    Each chunk is stored using its `chunk_id` (e.g. `STORY-0001::chunk-0`) as the
    ChromaDB document/vector ID, and its full metadata (front matter fields plus
    `parent_id`, `chunk_index`, `chunk_id`, `file_path`) is preserved alongside
    the embedding.

    Args:
        persist_directory: Directory to persist the ChromaDB collection to.
            Defaults to `vector_db/chroma/` at the project root.
        collection_name: Name of the ChromaDB collection to create.

    Returns:
        The resulting `Chroma` vector store, ready for similarity search.
    """
    persist_path = Path(persist_directory)
    if persist_path.exists():
        shutil.rmtree(persist_path)
    persist_path.mkdir(parents=True, exist_ok=True)

    documents = load_knowledge_documents()
    chunks = split_documents(documents)
    chunk_ids = [chunk.metadata["chunk_id"] for chunk in chunks]

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        ids=chunk_ids,
        collection_name=collection_name,
        persist_directory=str(persist_path),
    )
    return vector_store


def load_vector_store(
    persist_directory: Path | str = PERSIST_DIRECTORY,
    collection_name: str = COLLECTION_NAME,
) -> Chroma:
    """Load a previously persisted JEJU-KB vector store without rebuilding it.

    Args:
        persist_directory: Directory the ChromaDB collection was persisted to by
            `build_vector_store`. Defaults to `vector_db/chroma/` at the project
            root.
        collection_name: Name of the ChromaDB collection to load.

    Returns:
        A `Chroma` vector store backed by the persisted collection, ready for
        similarity search.

    Raises:
        FileNotFoundError: if `persist_directory` does not exist, meaning
            `build_vector_store` has not been run yet.
    """
    persist_path = Path(persist_directory)
    if not persist_path.exists():
        raise FileNotFoundError(
            f"No persisted vector store found at {persist_path}. "
            "Run build_vector_store() first."
        )

    embedding_model = get_embedding_model()
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=str(persist_path),
    )


if __name__ == "__main__":
    documents = load_knowledge_documents()
    chunks = split_documents(documents)

    print(f"Source documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Persist path: {PERSIST_DIRECTORY}\n")

    print("Building vector store (embedding all chunks via OpenAI)...")
    vector_store = build_vector_store()
    print("Vector store built.\n")

    query = "I want to learn about haenyeo culture"
    print(f"Test similarity search: {query!r}\n")
    results = vector_store.similarity_search(query, k=3)

    for rank, result in enumerate(results, start=1):
        meta = result.metadata
        print(
            f"{rank}. title={meta.get('title')!r} | "
            f"category={meta.get('category')} | "
            f"parent_id={meta.get('parent_id')} | "
            f"chunk_id={meta.get('chunk_id')}"
        )
