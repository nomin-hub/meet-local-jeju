# JEJU-KB Knowledge Document Standard (KDS)

**Document ID:** KDS-1.0
**Status:** Active
**Owner:** AI Engineering
**Applies to:** All documents under [`knowledge/`](README.md)
**Related:** [`knowledge/README.md`](README.md), [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md)

---

## 1. What Is KDS

The Knowledge Document Standard (KDS) is the formal specification for every document stored in JEJU-KB, the knowledge base that grounds Meet Local Jeju's RAG system.

KDS defines three things:

1. **Format** — every knowledge document is a single Markdown file with a YAML front matter block.
2. **Schema** — a fixed set of required and optional metadata fields, consistent across all ten JEJU-KB categories.
3. **Identity and placement rules** — how a document is named, numbered, and located within `knowledge/`.

KDS exists so that every knowledge document — regardless of who or what authors it, and regardless of which category it belongs to — is structurally predictable. This predictability is what allows the ingestion pipeline (`rag/loader.py`, `rag/splitter.py`) to process any document in `knowledge/` without category-specific parsing logic, and what allows the Recommendation Engine to reason over metadata (season, region, related content) instead of re-deriving it from free text at query time.

**KDS governs structure and metadata only. It does not implement ingestion, embedding, or retrieval — those remain the responsibility of `rag/` (see [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md)), which is not built yet.**

Any future task — human or AI-authored — that creates a new knowledge document in `knowledge/` must conform to this standard.

## 2. Why Structured Markdown Instead of Raw PDFs

JEJU-KB documents are authored as Markdown with YAML front matter, not as PDFs or other binary/layout formats. This is a deliberate engineering decision, not a stylistic preference:

- **Metadata cannot be embedded natively in a PDF.** A PDF is a rendering format; anything resembling metadata (category, season, region) would have to live in a separate system and be kept in sync by hand. YAML front matter keeps metadata and content in the same file, physically inseparable.
- **PDFs resist clean chunking.** Text extraction from PDFs is layout-dependent and frequently produces broken sentences, merged columns, and lost reading order — all of which degrade chunk quality and, downstream, retrieval quality. Markdown has an unambiguous linear text structure by construction.
- **Markdown is diffable and reviewable.** Every knowledge document goes through a curation review (see [`docs/product/02_ARCHITECTURE.md`, Section 7.2](../docs/product/02_ARCHITECTURE.md#72-curation-principle)). Plain-text Markdown can be reviewed and diffed like code in version control; PDFs cannot.
- **Markdown is directly and predictably parseable.** Headings, lists, and emphasis map to a small, stable set of tokens that a splitter can reason about when deciding chunk boundaries. PDF structure varies by the tool that produced it.
- **Markdown avoids unnecessary processing steps.** Ingesting a PDF requires an extraction/OCR step before any RAG-specific processing can begin — an additional point of failure and information loss. A Markdown file is ready to load as-is.

Where a source document originates as a PDF (e.g., a government publication), it must be transcribed into a KDS-compliant Markdown document during curation — the original PDF may be retained as a reference in `source`, but it is never ingested directly.

## 3. Required Front Matter Fields

Every knowledge document **must** include the following fields in its YAML front matter. Documents missing any required field are not KDS-compliant and must not be ingested.

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique document identifier, following the [ID Naming Rules](#4-id-naming-rules) (e.g. `STORY-0001`). Assigned once and never reused or changed. |
| `title` | string | Human-readable title of the document. |
| `category` | string | One of the ten top-level JEJU-KB categories, matching the folder the document lives in exactly (e.g. `stories`, `experiences`, `culture`). |
| `subcategory` | string | Finer-grained classification within the category (e.g. `haenyeo` under `culture`, `farm-experience` under `experiences`). Free-form but should be reused consistently across documents in the same category. |
| `island` | string | Island-level geographic scope. `Jeju` for all current content; reserved so JEJU-KB's schema can extend to other islands/regions without a breaking change (see [Architecture, Section 9](../docs/product/02_ARCHITECTURE.md#9-future-scalability)). |
| `region` | string | Sub-island location (e.g. `Seogwipo-si`, `Hado-ri, Jeju-si`, `Hallasan`). Should be as specific as the source material supports. |
| `season` | string | Time-of-year relevance. One of: `spring`, `summer`, `autumn`, `winter`, `year-round`. |
| `tags` | array of strings | Free-form descriptive keywords supporting fine-grained retrieval (e.g. `[haenyeo, oral-history, UNESCO]`). |
| `language` | string | ISO 639-1 code of the document's language (e.g. `en`, `ko`). Documents are authored per-language; a translation is a separate document with its own `id`. |
| `source` | string | Provenance of the content — organization, publication, named interview, or original material reference. Required for trust and attribution (see [Section 8.5](#85-source-attribution)). |
| `last_updated` | date (`YYYY-MM-DD`) | Date the document's content was last reviewed or revised. Used for freshness tracking, particularly for time-sensitive categories such as `festivals`, `transportation`, and `government`. |

## 4. Optional Front Matter Fields

The following fields may be included when relevant. They must not be fabricated — omit a field rather than guess a value.

| Field | Type | Description |
|---|---|---|
| `related_experiences` | array of strings | `id`s of related documents in `experiences/` (e.g. `[EXP-0001]`). |
| `related_food` | array of strings | `id`s of related documents in `food/` (e.g. `[FOOD-0001]`). |
| `related_stories` | array of strings | `id`s of related documents in `stories/` (e.g. `[STORY-0001]`). |
| `transportation` | string | Practical guidance on how to reach the location described, or a reference `id` in `transportation/`. |
| `difficulty` | string | Applicable to activity-oriented documents (typically `experiences`). One of: `easy`, `moderate`, `challenging`. |
| `duration` | string | Estimated time commitment (e.g. `2 hours`, `half-day`, `full-day`). |
| `target_user` | array of strings | Traveler profiles the content is best suited to (e.g. `[solo-traveler, long-stay, heritage-seeking]`), aligned with the personas defined in [`docs/01_PRD.md`](../docs/01_PRD.md#5-user-personas). |

Cross-reference fields (`related_experiences`, `related_food`, `related_stories`, `transportation`) must only reference `id`s that exist elsewhere in `knowledge/`. Dangling references are a curation defect.

## 5. ID Naming Rules

Every document `id` follows the format:

```
PREFIX-NNNN
```

- `PREFIX` identifies the document's category and is fixed per category (table below).
- `NNNN` is a zero-padded, four-digit sequence number, unique **within that prefix** (not globally). The first document in a category is `0001`.
- `id`s are immutable. Once assigned and ingested, an `id` is never reused, renumbered, or reassigned to different content — even if the original document is later retired. A retired document is marked as such in review (outside the scope of this standard's required fields) rather than having its `id` recycled.

| Category folder | Prefix | Example |
|---|---|---|
| `local_life/` | `LOCAL` | `LOCAL-0001` |
| `seasonal_living/` | `SEASON` | `SEASON-0001` |
| `stories/` | `STORY` | `STORY-0001` |
| `experiences/` | `EXP` | `EXP-0001` |
| `culture/` | `CULTURE` | `CULTURE-0001` |
| `food/` | `FOOD` | `FOOD-0001` |
| `festivals/` | `FEST` | `FEST-0001` |
| `government/` | `GOV` | `GOV-0001` |
| `transportation/` | `TRANS` | `TRANS-0001` |
| `tourism/` | `TOUR` | `TOUR-0001` |

> **Note:** `SEASON` is defined here to give `seasonal_living/` a prefix consistent with the other nine categories; without it, the standard would be unable to identify any document in that folder.

A document's `id` prefix and its `category` field must always agree with the folder it is stored in. A `STORY-*` document must have `category: stories` and live under `knowledge/stories/`.

## 6. Folder Rules

JEJU-KB has exactly ten top-level category folders. No additional top-level folders may be added without a revision to this standard.

```
knowledge/
├── local_life/
├── seasonal_living/
├── stories/
├── experiences/
├── culture/
├── food/
├── festivals/
├── government/
├── transportation/
└── tourism/
```

**Placement rules:**

- Every knowledge document lives directly inside exactly one category folder — no nested subfolders within a category (subcategorization is expressed via the `subcategory` field, not via directory structure).
- A document belongs to the category that best matches its primary subject, even when it touches multiple categories. Secondary relevance is expressed through `tags` and the `related_*` cross-reference fields, not by duplicating the document into multiple folders.
- **File naming** follows the pattern `{id}-{kebab-case-slug}.md`, where the slug is a short, human-readable version of the title. Example: `STORY-0001-haenyeo-grandmother-of-hado.md`.
- One document per file. A file must never contain multiple `id`s or multiple front matter blocks.

## 7. Example Documents

The following three documents are complete, KDS-compliant examples. They illustrate front matter usage, category placement judgment, and expected body structure for three different content types.

### 7.1 Local Story — `knowledge/stories/STORY-0001-haenyeo-grandmother-of-hado.md`

```markdown
---
id: STORY-0001
title: "The Haenyeo Grandmother of Hado"
category: stories
subcategory: haenyeo
island: Jeju
region: "Hado-ri, Jeju-si"
season: year-round
tags: [haenyeo, women-divers, oral-history, UNESCO, Hado-ri]
language: en
source: "Oral history interview, Hado-ri Haenyeo Museum community program, 2023"
last_updated: 2024-03-12
related_experiences: [EXP-0001]
related_food: [FOOD-0001]
target_user: [heritage-seeking, solo-traveler]
---

# The Haenyeo Grandmother of Hado

## Overview

In the village of Hado-ri, on Jeju's northeastern coast, Grandmother Yang has dived for abalone, conch, and sea urchin for over fifty years. She is one of the last generation of haenyeo — Jeju's traditional women divers — still diving without oxygen tanks, using only a wetsuit, a net, and decades of memorized seafloor terrain.

## The Story

Grandmother Yang began diving at fifteen, taught not in a classroom but by following her mother into the water. She describes the discipline of "sumbisori" — the distinctive whistled breath haenyeo make when surfacing, a sound that once let divers track each other's location and safety without speaking. She still dives most mornings when the sea is calm, though her daughters, unlike her, work on land.

She speaks plainly about the risk: haenyeo have historically dived without modern safety equipment in cold water, at depth, for extended periods. What outsiders often frame as tradition, she frames as work — hard, physical, and economically essential to her household for most of her life.

## Cultural Significance

Haenyeo culture was inscribed on UNESCO's Representative List of the Intangible Cultural Heritage of Humanity in 2016, recognizing both the diving practice and the distinct matrifocal community structure it created in Jeju's coastal villages. The number of active haenyeo has declined sharply over the past several decades, making firsthand accounts like Grandmother Yang's increasingly rare.

## Sources

- Oral history interview conducted through the Hado-ri Haenyeo Museum community program (2023).
- Cross-referenced with UNESCO Intangible Cultural Heritage documentation for factual accuracy regarding recognition status.
```

### 7.2 Experience — `knowledge/experiences/EXP-0001-tangerine-harvest-seogwipo.md`

```markdown
---
id: EXP-0001
title: "Tangerine Harvest in Seogwipo"
category: experiences
subcategory: farm-experience
island: Jeju
region: "Seogwipo-si"
season: winter
tags: [gamgyul, mandarin, harvest, farm-work, family-owned]
language: en
source: "Local farm operator interview, Seogwipo, 2024"
last_updated: 2024-01-20
related_food: [FOOD-0001]
related_stories: []
transportation: "Local bus routes serve most Seogwipo-area farms; several are a short taxi ride from Seogwipo bus terminal."
difficulty: easy
duration: "2-3 hours"
target_user: [family, slow-travel, solo-traveler]
---

# Tangerine Harvest in Seogwipo

## Overview

Between November and January, family-run citrus farms across Seogwipo open their groves for hands-on tangerine (gamgyul) harvesting. Visitors pick fruit directly from the trees alongside the farmers who grow it, rather than purchasing pre-packaged produce.

## What to Expect

Farmers typically walk visitors through a short orientation on how to identify ripe fruit and pick without damaging the tree, followed by open picking time in the grove. Most farms allow visitors to eat as they pick and to take home a portion of what they harvest. Sessions are informal and unhurried — there is no fixed script, and conversation with the farm family is part of the experience.

## Practical Information

- **Best timing:** Mid-November through late December, during peak harvest.
- **What to bring:** Comfortable closed-toe shoes; light rain gear, as sessions run regardless of light rain.
- **Group size:** Typically accommodates individuals and small groups without advance booking systems in place; arrangements are made directly with the farm.

## Cultural Context

Citrus farming has been central to Jeju's rural economy since the mid-20th century, and mandarin cultivation shaped the layout and rhythm of many Seogwipo-area villages. Participating in the harvest offers a direct, physical connection to the seasonal agricultural cycle described in `seasonal_living/`, rather than an observational or commercial framing of the same crop.
```

### 7.3 Local Life — `knowledge/local_life/LOCAL-0001-jeju-five-day-market.md`

```markdown
---
id: LOCAL-0001
title: "Jeju's Five-Day Markets (Owe-il-jang)"
category: local_life
subcategory: market
island: Jeju
region: "Jeju-si and Seogwipo-si (island-wide rotating schedule)"
season: year-round
tags: [owe-il-jang, market, daily-life, shopping, local-produce]
language: en
source: "Jeju Special Self-Governing Province local commerce records; community write-ups, 2023"
last_updated: 2024-02-05
related_food: [FOOD-0001]
transportation: "Most five-day markets are accessible via local bus routes; the Jeju-si market is a short walk from the intercity bus terminal."
target_user: [solo-traveler, long-stay, family]
---

# Jeju's Five-Day Markets (Owe-il-jang)

## Overview

Jeju's traditional five-day markets, or owe-il-jang, rotate through towns across the island on a fixed five-day cycle, a system that predates modern retail and still structures how many residents shop for produce, fish, and household goods.

## What You'll Find

Markets combine fresh produce and seafood vendors — many selling what they grew or caught themselves — with prepared-food stalls, household goods, and, in larger locations like Jeju-si, secondhand and craft sections. Pricing is often informal and can involve light negotiation, particularly for produce sold by local farmers directly.

## Visiting Tips

- **Confirm the local schedule.** Each town's market day follows the island-wide five-day rotation, so the same market is not open daily — check the current schedule for the town you plan to visit rather than assuming daily operation.
- **Go early.** The best selection, particularly of fresh seafood, is typically in the morning.
- **Cash is common.** Smaller vendors may not support card payment.

## Cultural Context

The five-day market system reflects an older, pre-supermarket rhythm of commerce that Jeju has retained even as convenience retail has grown. For long-stay visitors, following the market rotation is one of the most direct ways to participate in the same weekly routine many local households still follow.
```

## 8. How the RAG Pipeline Uses Metadata

KDS front matter is not incidental documentation — it is the mechanism by which the RAG pipeline described in [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md) will make retrieval precise, filtered, personalized, and trustworthy, in addition to relying on semantic similarity over document text.

### 8.1 Retrieval

The document body is embedded and indexed for semantic similarity search, as described in the architecture's [RAG Pipeline](../docs/product/02_ARCHITECTURE.md#4-rag-pipeline). `title` and `tags` are expected to be included in the text passed to the embedding model alongside the body, since they concentrate the document's topical signal and improve match quality for short, keyword-like queries (e.g., "haenyeo") that might otherwise under-match against long narrative text.

### 8.2 Filtering

`category`, `subcategory`, `island`, `region`, `season`, and `language` are structured metadata fields, not embedded text — they are intended to be used as pre-filters at the ChromaDB query level (see [ChromaDB Architecture](../docs/product/02_ARCHITECTURE.md#8-chromadb-architecture)), narrowing the candidate set before or alongside similarity ranking. This is what allows a query like "what can I do in Seogwipo in winter" to be scoped to `region: Seogwipo-si` and `season: winter` rather than relying on the LLM to infer scope from unfiltered results.

### 8.3 Recommendation

The Recommendation Engine layer (see [Architecture, Section 1](../docs/product/02_ARCHITECTURE.md#1-high-level-system-architecture)) uses `related_experiences`, `related_food`, and `related_stories` to assemble multi-category recommendation clusters — for example, surfacing a related food document alongside an experience about the farm that produces it. `target_user` supports lightweight persona-aware ranking, and `tags` supports diversity logic that avoids returning near-duplicate recommendations from the same subcategory.

### 8.4 Itinerary Planning

Structured fields — particularly `region`, `duration`, `difficulty`, `season`, and `transportation` — are what would make future itinerary-style reasoning (sequencing multiple recommendations by location, time available, and season) possible without re-deriving that information from free text at query time. **Itinerary planning is explicitly out of scope for the MVP** (see [`docs/01_PRD.md`, Section 8, Non Goals](../docs/01_PRD.md#8-non-goals)); this metadata is designed so that capability can be added later without changing the knowledge document schema.

### 8.5 Source Attribution

The `source` field is what allows the system to be transparent about provenance — supporting the product's Source Transparency feature (see [`docs/01_PRD.md`, Section 7](../docs/01_PRD.md#7-core-features-mvp-only)) without exposing raw citations that would overwhelm a conversational answer. `id` provides a stable internal reference that can be logged alongside a generated response, enabling traceability from a user-facing answer back to the specific document(s) that grounded it, independent of how the document's content or title may be revised over time (`last_updated` marks that revision history point).

---

*This standard governs the structure of individual knowledge documents. It does not define ingestion, chunking, embedding, or retrieval behavior — those are specified in [`docs/product/02_ARCHITECTURE.md`](../docs/product/02_ARCHITECTURE.md) and remain unimplemented as of this document's authoring.*
