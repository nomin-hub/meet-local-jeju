# Meet Local Jeju

**Discover Jeju Beyond Tourism**

An AI travel assistant that helps international travelers experience authentic local life on Jeju Island, Korea — powered by a Retrieval-Augmented Generation (RAG) pipeline grounded in a curated, structured knowledge base rather than general model memory.

---

## Overview

Most travel AI tools answer Jeju questions from whatever a general-purpose language model happens to remember: the same handful of well-known attractions, repeated in slightly different words. Meet Local Jeju takes a different approach. Every answer is retrieved from **JEJU-KB**, a hand-curated knowledge base of Jeju's local culture, seasonal living, food, festivals, local stories, and daily life — organized, tagged, and versioned like a real data product, not scraped or hallucinated on the fly.

This project helps international travelers discover **authentic local Jeju experiences** — haenyeo diving culture, seasonal tangerine harvests, traditional five-day markets, volcanic stone walls — through **trusted, structured knowledge**, with every answer traceable back to the specific source document that grounded it.

## Problem

International travelers researching Jeju run into three compounding problems:

1. **Homogenized recommendations.** Search engines and travel apps converge on the same "top 10" attractions, driven by SEO and social virality rather than authenticity.
2. **Fragmented local knowledge.** Jeju's richest cultural and seasonal knowledge exists, but scattered across Korean-language sources, rarely consolidated or translated.
3. **No trustworthy filter for "authentic."** Existing tools optimize for popularity, not cultural depth or seasonal relevance — and general-purpose AI chatbots will confidently answer from memory even when that memory is thin, generic, or wrong.

## Solution

Meet Local Jeju is a conversational assistant that answers **only** from a curated knowledge base, not from whatever a language model happens to recall about Jeju:

1. A traveler asks a question in plain English.
2. The system retrieves the most relevant chunks from **JEJU-KB** — never the model's general training knowledge.
3. An LLM synthesizes an answer **strictly from that retrieved context**, citing the source document title and ID inline.
4. The full source list (with category, chunk ID, and file path) is shown alongside the answer, so the traveler can see exactly where the information came from.

If JEJU-KB doesn't have relevant information for a question, the assistant says so — it does not fill the gap with invented specifics.

## Long-Term Vision

Meet Local Jeju starts as a RAG-powered local knowledge assistant — that's the entire product today. But the long-term goal is bigger: to become a **trusted local experience and trip-planning platform** that connects international travelers with authentic Jeju local life, not just answers about it.

This MVP is **Phase 1** of a longer product roadmap:

| Phase | Direction | Status |
|---|---|---|
| 1 | RAG-powered local knowledge assistant | ✅ **Current MVP (this repo)** |
| 2 | Personalized experience recommendation mode | 🔜 Planned |
| 3 | Multi-day trip planner | 🔭 Future |
| 4 | Local host and experience dataset | 🔭 Future |
| 5 | Marketplace prototype with mock booking flow | 🔭 Future |
| 6 | Real platform — host onboarding, booking, reviews, payments, partnerships | 🔭 Long-term vision |

The future platform direction (Phases 2–6) includes a personalized trip planner, a local experience marketplace, host profiles for farmers, haenyeo culture guides, market guides, artisans, and local storytellers, stay + experience packages, and — long term — Airbnb-like booking and reviews. **None of that exists yet.** No host onboarding, booking flow, payments, user accounts, or reviews are implemented in this codebase.

> This MVP focuses on the knowledge and recommendation layer first. Before building booking, payment, or host-management features, the project validates whether AI can understand traveler intent and match it with structured local knowledge.

Meet Local Jeju is not trying to recommend famous tourist spots — that's what separates it from generic travel guide apps (popularity-ranked, not authenticity-ranked), generic AI chatbots (ungrounded, unattributed answers from memory), Airbnb (booking infrastructure first, discovery second), and traditional tour platforms (fixed, commission-driven packages). It's designed to help travelers discover local stories, seasonal living, people, food, culture, and authentic island experiences — with the marketplace layer only introduced later, once that foundation is proven.

Full detail on the platform direction, phase-by-phase scope, and an explicit "what exists vs. what doesn't" table: [`docs/product/01_PRODUCT_BRIEF.md`](docs/product/01_PRODUCT_BRIEF.md).

## Why RAG?

A general-purpose LLM asked "what's an authentic thing to do in Jeju in October?" will answer from broad training data — plausible-sounding, but not grounded in anything specific, current, or verifiable. Retrieval-Augmented Generation solves this differently:

- **Groundedness over fluency.** The model is instructed to answer only from retrieved JEJU-KB chunks, not its own memory of Jeju.
- **Updatable without retraining.** New knowledge documents can be added to `knowledge/` and re-embedded at any time — no model fine-tuning required.
- **Traceable answers.** Every claim can be traced back to a specific document ID and file path, which is what makes "authentic" a verifiable property instead of a marketing word.
- **Honest uncertainty.** The system prompt explicitly instructs the model to say when JEJU-KB doesn't cover something, rather than inventing prices, schedules, addresses, or named individuals to fill the gap.

## Key Features

- **Conversational chat UI** (Streamlit) with persistent session history.
- **Retrieval-grounded answers** — every response is generated from retrieved JEJU-KB chunks, never from unaided model memory.
- **Source attribution** — each answer is paired with the exact source documents (title, category, chunk ID, file path) that grounded it.
- **Structured knowledge base (JEJU-KB)** — Markdown + YAML front matter documents organized into 10 topical categories with a formal schema (see [Knowledge Document Standard](#knowledge-document-standard-kds)).
- **Seasonal and category-aware content** — knowledge documents carry `season`, `region`, and `category` metadata for more precise retrieval.
- **Guardrails against fabrication** — the prompt explicitly forbids inventing exact prices, schedules, addresses, phone numbers, or named individuals.
- **Example questions in the sidebar** for instant, one-click demoing.

## Demo Questions

Try these in the running app — all four are verified end-to-end against the current knowledge base:

- *"I want to learn about haenyeo culture."*
- *"What can I do in Jeju in October?"*
- *"I want to meet local people at a traditional market."*
- *"Tell me about Jeju stone walls."*

## Architecture

```mermaid
flowchart TD
    A["User"] --> B["Streamlit UI"]
    B --> C["RAG Chain"]
    C --> D["Retriever"]
    D --> E["ChromaDB"]
    E --> F["JEJU-KB"]
    F --> G["OpenAI"]
    G --> H["Grounded Answer + Sources"]
    H --> A
```

This diagram shows the query-time path a question takes through the system. `JEJU-KB → ChromaDB` is populated ahead of time by a separate **offline ingestion pipeline** (`rag/loader.py` → `rag/splitter.py` → `rag/vectordb.py`), not on every query — the vector store is built once via `python3 rag/vectordb.py` and simply *read* at query time. See [`docs/product/02_ARCHITECTURE.md`](docs/product/02_ARCHITECTURE.md) for the full system architecture, including the ingestion-phase diagram and the ChromaDB collection design.

## Project Structure

```
meet-local-jeju/
├── app.py                     # Streamlit chat UI (interface layer)
│
├── knowledge/                  # JEJU-KB — the AI knowledge base (RAG source of truth)
│   ├── KDS.md                    # Knowledge Document Standard
│   ├── README.md                 # What JEJU-KB is, why it's separate from docs/
│   ├── stories/                  # 2 knowledge objects (STORY-0001, STORY-0002)
│   ├── experiences/              # 3 knowledge objects (EXP-0001 – EXP-0003)
│   ├── local_life/               # 2 knowledge objects (LOCAL-0001, LOCAL-0002)
│   ├── seasonal_living/          # 1 knowledge object (SEASON-0001)
│   ├── food/                     # 1 knowledge object (FOOD-0001)
│   ├── culture/                  # 1 knowledge object (CULTURE-0001)
│   ├── festivals/                # folder + README only — not yet populated
│   ├── government/               # folder + README only — not yet populated
│   ├── transportation/           # folder + README only — not yet populated
│   └── tourism/                  # folder + README only — not yet populated
│
├── rag/                        # RAG pipeline
│   ├── loader.py                 # Parses knowledge/*.md into LangChain Documents
│   ├── splitter.py               # Chunks documents (chunk_size=800, overlap=120)
│   ├── vectordb.py               # OpenAI embeddings + ChromaDB build/load
│   ├── retriever.py              # Query-time similarity search
│   ├── chain.py                  # Grounded-answer prompt + generation
│   └── embeddings.py             # Placeholder — not yet implemented (see Limitations)
│
├── data/                       # Working storage for the ingestion pipeline (raw/processed/embeddings)
├── vector_db/chroma/            # Persisted ChromaDB collection (build artifact, gitignored)
│
├── docs/                       # Product documentation
│   ├── 01_PRD.md                 # Product Requirement Document
│   └── product/02_ARCHITECTURE.md  # System architecture
│
├── utils/                      # Placeholder — config.py / helpers.py not yet implemented
├── pages/                      # Additional Streamlit pages (none yet)
│
├── requirements.txt
├── .env.example
└── .gitignore
```

## JEJU-KB Knowledge Base

JEJU-KB is the curated knowledge base that grounds every answer — it is deliberately kept separate from `docs/` (product documentation for the team) because it has a different audience (the retrieval pipeline and, indirectly, end users), a different lifecycle (grows continuously as content is curated), and a different trust bar (every fact needs to be attributable). See [`knowledge/README.md`](knowledge/README.md) for the full rationale.

JEJU-KB is organized into **10 topical categories**:

| Category | Populated? |
|---|---|
| `stories` | ✅ 2 documents |
| `experiences` | ✅ 3 documents |
| `local_life` | ✅ 2 documents |
| `seasonal_living` | ✅ 1 document |
| `food` | ✅ 1 document |
| `culture` | ✅ 1 document |
| `festivals` | Not yet populated |
| `government` | Not yet populated |
| `transportation` | Not yet populated |
| `tourism` | Not yet populated |

**10 knowledge objects currently populated**, cross-linked by ID (e.g. the haenyeo story `STORY-0001` links to the haenyeo culture walk `EXP-0002`), forming a small but real knowledge graph rather than a flat document pile.

## Knowledge Document Standard (KDS)

Every JEJU-KB document is Markdown with YAML front matter, following the formal spec in [`knowledge/KDS.md`](knowledge/KDS.md) — not raw PDFs, because front matter can't live inside a PDF, and PDF text extraction degrades chunk quality.

**Required front matter fields:** `id`, `title`, `category`, `subcategory`, `island`, `region`, `season`, `tags`, `language`, `source`, `last_updated`.

**Optional fields:** `related_experiences`, `related_food`, `related_stories`, `transportation`, `difficulty`, `duration`, `target_user`.

**ID convention:** `{PREFIX}-{NNNN}`, one prefix per category (`STORY-0001`, `EXP-0001`, `LOCAL-0001`, `SEASON-0001`, `FOOD-0001`, `CULTURE-0001`, plus `FEST`, `GOV`, `TRANS`, `TOUR` reserved for the remaining categories). IDs are immutable once assigned and are what the loader validates against before a document can be ingested.

This schema is what makes category-aware, season-aware, metadata-filtered retrieval possible — and what lets `rag/loader.py` validate every document at load time and raise a clear error (file path + missing fields) rather than silently ingesting incomplete content.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Orchestration | LangChain (`langchain`, `langchain-community`, `langchain-openai`, `langchain-chroma`) |
| Vector store | ChromaDB (persisted locally at `vector_db/chroma/`) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Generation | OpenAI `gpt-4o-mini` |
| Config | `python-dotenv` |
| Front matter parsing | PyYAML |

## How to Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create your environment file
cp .env.example .env
# then edit .env and set OPENAI_API_KEY=...

# 3. Build the vector store (one-time, or whenever knowledge/ changes)
python3 rag/vectordb.py

# 4. Run the app
streamlit run app.py
```

Step 3 embeds every JEJU-KB document and persists them to `vector_db/chroma/`. The Streamlit app **only reads** from that persisted store — it never rebuilds the vector database itself, so step 3 must be run at least once before the app can answer questions.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key, used for both embeddings and chat generation. Set it in a local `.env` file (see `.env.example`) — never commit a real key. `.env` is gitignored. |

## Example Output

**Question:** *"Tell me about Jeju stone walls."*

> Jeju's stone walls, known as batdam, are low, dry-stacked walls made from black volcanic basalt. These walls are constructed without mortar and are designed to withstand the island's persistent coastal winds. Their unique construction allows wind to pass through the gaps, preventing the walls from being pushed over. Batdam mark the boundaries of small, irregularly shaped agricultural plots, reflecting the island's volcanic terrain rather than a grid-like layout common elsewhere.
>
> These stone walls are not merely decorative; they play a functional role in Jeju's traditional agricultural practices. The system of fields organized around batdam has been recognized as a Globally Important Agricultural Heritage System by the FAO, highlighting its significance as a long-standing and still-functioning land-management practice.
>
> Travelers can find batdam throughout Jeju's mid-mountain farmland, especially around citrus orchards and in coastal fishing villages ("Batdam: The Black Stone Walls of Jeju", CULTURE-0001).

**Sources (4):**

| ID | Title | Category | Chunk | File |
|---|---|---|---|---|
| CULTURE-0001 | Batdam: The Black Stone Walls of Jeju | culture | CULTURE-0001::chunk-0 | `knowledge/culture/CULTURE-0001-jeju-stone-walls.md` |
| CULTURE-0001 | Batdam: The Black Stone Walls of Jeju | culture | CULTURE-0001::chunk-1 | `knowledge/culture/CULTURE-0001-jeju-stone-walls.md` |
| CULTURE-0001 | Batdam: The Black Stone Walls of Jeju | culture | CULTURE-0001::chunk-2 | `knowledge/culture/CULTURE-0001-jeju-stone-walls.md` |
| CULTURE-0001 | Batdam: The Black Stone Walls of Jeju | culture | CULTURE-0001::chunk-3 | `knowledge/culture/CULTURE-0001-jeju-stone-walls.md` |

## Current Limitations

- **Knowledge coverage is partial.** 10 documents across 6 of 10 categories — `festivals`, `government`, `transportation`, and `tourism` have folder scaffolding but no content yet.
- **English only.** No multi-language ingestion or querying yet.
- **Single-turn retrieval.** Each question is answered independently; prior conversation turns are displayed in the UI but are not yet used as retrieval context for follow-up questions.
- **Full rebuild only.** `build_vector_store()` always rebuilds the entire collection from scratch — there's no incremental/partial re-ingestion yet.
- **Some source content is illustrative.** A few narrative "story" documents are composite accounts written to demonstrate the format, explicitly flagged as such in their own `Source Notes` sections, pending real attributed sourcing.
- **`rag/embeddings.py`, `utils/config.py`, and `utils/helpers.py` are still placeholders.** Embedding configuration currently lives directly in `rag/vectordb.py` rather than a shared config module.
- **No reservation, payment, login, host onboarding, or admin features.** Intentionally out of scope for Phase 1 — these belong to later phases of the platform vision (see [Long-Term Vision](#long-term-vision) and [`docs/product/01_PRODUCT_BRIEF.md`](docs/product/01_PRODUCT_BRIEF.md)), not this MVP.

## Future Roadmap

This section covers near-term improvements *within Phase 1* (the current RAG assistant). For the larger 6-phase platform vision — trip planning, a local experience marketplace, host profiles, and eventually Airbnb-like booking — see [Long-Term Vision](#long-term-vision) above and the full [Product Brief](docs/product/01_PRODUCT_BRIEF.md).

- Populate the remaining four JEJU-KB categories (`festivals`, `government`, `transportation`, `tourism`).
- Multi-language support (Korean, Japanese, Chinese).
- Multi-turn, context-aware follow-up questions.
- A community/curator content contribution pipeline with review gating.
- Partnerships with Jeju public tourism and cultural heritage sources for verified content feeds.
- An evaluation harness to systematically track groundedness and hallucination rate over time.
- Extending the same knowledge-base + RAG pattern to other regions beyond Jeju.

See [`docs/01_PRD.md`](docs/01_PRD.md) for the full Phase 1 product requirements and non-goals.

## What I Learned

Building this project end-to-end — from a bare project skeleton through a working, source-attributed RAG assistant — surfaced a few lessons worth calling out:

- **Metadata design is the real product.** The hardest and most valuable part of this project wasn't the retrieval code — it was designing a knowledge document standard (KDS) with a consistent schema, ID scheme, and category taxonomy *before* writing any content. Once that existed, loading, chunking, and retrieval all became mechanical.
- **Type mismatches hide in "boring" layers.** PyYAML silently parses unquoted `YYYY-MM-DD` front matter values into Python `date` objects instead of strings — which loaded and chunked without any error, then broke ChromaDB ingestion with a cryptic metadata-type error. The fix belonged in the loader (normalize types at the source), not patched around downstream.
- **Grounding has to be enforced at the prompt level, not assumed.** Retrieval alone doesn't stop a model from padding an answer with plausible-sounding specifics. The system prompt explicitly forbids inventing prices, schedules, addresses, and named individuals — and it's testable: every demo answer was checked against that constraint.
- **Separating "knowledge" from "docs" pays off immediately.** Keeping product documentation (`docs/`) and AI-facing knowledge (`knowledge/`) in separate trees with different quality bars made it obvious, at every step, what was safe to feed into the ingestion pipeline and what wasn't.
- **A CLI test block per module is worth the extra few lines.** Every `rag/` module (`loader.py`, `splitter.py`, `vectordb.py`, `retriever.py`, `chain.py`) is independently runnable and verifiable via `python3 rag/<module>.py`, which made debugging the pipeline stage-by-stage far faster than only testing through the UI.
