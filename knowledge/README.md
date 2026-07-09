# JEJU-KB — The Meet Local Jeju Knowledge Base

**Status:** Foundation (structure only — no content ingested yet)
**Related:** [`../docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md), [`../docs/01_PRD.md`](../docs/01_PRD.md)

---

## What is JEJU-KB

JEJU-KB is the curated knowledge base that will ground every answer Meet Local Jeju's AI gives to travelers. It is the single source of truth the RAG pipeline retrieves from — not the LLM's general training knowledge, not `docs/`, and not any other content in this repository.

Everything under `knowledge/` is intended to be authentic, verifiable, and reviewed before it is treated as retrievable ground truth. This is what allows the product to promise trustworthy, locally-grounded answers instead of generic travel-blog content.

## Why It Is Separated From `docs/`

`docs/` holds **product documentation** — the PRD, the architecture document, and other artifacts written by and for the team building Meet Local Jeju (engineers, product managers, investors).

`knowledge/` holds **AI knowledge** — the raw material the RAG pipeline ingests, embeds, and retrieves to answer end-user questions.

These two concerns are deliberately kept apart:

- **Different audiences.** `docs/` is read by humans working on the project. `knowledge/` is read by the ingestion pipeline and, indirectly, by end users through the AI's responses.
- **Different lifecycles.** Product documentation changes when the product's direction changes. Knowledge content changes continuously as new local sources, seasonal updates, and community stories are curated — independent of any product or architecture decision.
- **Different quality bars.** Product docs need to be internally accurate. Knowledge content needs to be externally trustworthy, source-attributable, and safe to surface directly to travelers.
- **Different consumers at build time.** Only `knowledge/` is intended to be loaded by the ingestion pipeline (`rag/loader.py`) and embedded into the vector store. Keeping `docs/` out of that path prevents internal product documentation from ever leaking into retrieved answers.

## How RAG Uses It

`knowledge/` is the input to the ingestion phase of the RAG pipeline described in [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md):

1. **Load** — `rag/loader.py` reads curated documents from each `knowledge/{category}/` folder.
2. **Split** — `rag/splitter.py` chunks those documents into retrieval-sized units.
3. **Embed** — `rag/embeddings.py` generates vector embeddings for each chunk via the OpenAI Embeddings API.
4. **Persist** — `rag/vectordb.py` writes chunks, embeddings, and metadata into ChromaDB (`vector_db/`).

At query time, `rag/retriever.py` searches the resulting vector store — never `knowledge/` directly — so the folder structure below only matters for curation and ingestion, not for runtime retrieval.

This document defines the **structure only**. No ingestion, chunking, embedding, or retrieval logic is implemented yet — see [Definition of Done](#definition-of-done) below.

## Folder Taxonomy

JEJU-KB is organized into ten top-level categories. Each is independently curated and has its own README describing purpose, sourcing, example documents, metadata, and expansion plans.

| Folder | Category |
|---|---|
| [`local_life/`](local_life/README.md) | Local Life |
| [`seasonal_living/`](seasonal_living/README.md) | Seasonal Living |
| [`stories/`](stories/README.md) | Stories |
| [`experiences/`](experiences/README.md) | Experiences |
| [`culture/`](culture/README.md) | Culture |
| [`food/`](food/README.md) | Food |
| [`festivals/`](festivals/README.md) | Festivals |
| [`government/`](government/README.md) | Government |
| [`transportation/`](transportation/README.md) | Transportation |
| [`tourism/`](tourism/README.md) | Tourism |

This taxonomy matches the Knowledge Base architecture defined in [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md#7-knowledge-base-architecture).

## Definition of Done (this task)

- [x] `knowledge/` folder created.
- [x] All ten category folders created.
- [x] Every category folder has a `README.md`.
- [x] No existing documents moved (`docs/` is untouched).
- [x] No code changes.
- [x] No RAG implementation.
