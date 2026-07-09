# Meet Local Jeju — Demo Script

**Document Owner:** Product & Engineering
**Status:** Draft v1.0
**Length:** 3–5 minute live walkthrough
**Related:** [`README.md`](../../README.md), [`01_PRD.md`](../01_PRD.md), [`02_ARCHITECTURE.md`](02_ARCHITECTURE.md)

---

## Demo Goal

Show that Meet Local Jeju answers travel questions about Jeju Island **grounded in a curated knowledge base**, not from general AI memory — and that every answer is traceable back to a specific source document. The demo should make one thing obvious: this is a real RAG system with structured, attributable knowledge behind it, not a thin wrapper around a chatbot.

## Target Audience

- Recruiters and hiring managers evaluating AI engineering portfolio work.
- Engineers assessing RAG architecture and system design decisions.
- Non-technical stakeholders interested in the product concept (authentic local travel, not generic tourism).

Calibrate depth accordingly: lead with the product experience, then go as deep into architecture as the audience wants.

## App Setup Checklist

Run through this **before** presenting, not during:

- [ ] `.env` exists locally with a valid `OPENAI_API_KEY` (never shown on screen).
- [ ] Vector store is built: `vector_db/chroma/` exists and is current — run `python3 rag/vectordb.py` if `knowledge/` has changed since the last build.
- [ ] `streamlit run app.py` starts cleanly with no errors in the terminal.
- [ ] Home screen loads with **no** "vector store hasn't been built yet" warning banner.
- [ ] Sidebar shows all 4 example question buttons.
- [ ] Do one silent test question beforehand to confirm the OpenAI API key is live and quota is available — an auth or quota error mid-demo is the single most disruptive failure mode.
- [ ] Browser window sized wide enough that the sidebar is visible without collapsing (desktop width, not a narrow/mobile viewport).

## Recommended Demo Flow

**Total: ~4 minutes**

1. **(30s) Frame the problem.** Before opening the app: most travel AI just recommends the same tourist attractions everyone already knows about. Meet Local Jeju is built to surface what's *actually* local — culture, seasonal life, food, stories — and to be honest about what it does and doesn't know.
2. **(15s) Show the home screen.** Point out the title, subtitle ("Discover Jeju Beyond Tourism"), the short product description, and the sidebar of example questions.
3. **(60s) Run one example question live.** Click a sidebar example button (don't type — it's faster and more reliable live) and narrate what's happening while it loads: "This isn't going to the model's memory — it's retrieving the most relevant chunks from a curated knowledge base first, then generating an answer grounded in only that."
4. **(45s) Open the Sources expander.** This is the proof point of the whole demo. Show the ID, title, category, chunk ID, and file path for each source. Point out that the answer's inline citation (e.g. `("Batdam: The Black Stone Walls of Jeju", CULTURE-0001)`) matches a real, traceable document.
5. **(45s) Run a second question** (pick one that shows a different category, e.g. the market question after a culture question) to show breadth across the knowledge base, not a single lucky answer.
6. **(30s) Close with architecture, if the audience is technical.** One sentence per stage: Markdown + YAML knowledge documents → chunked → embedded with OpenAI → stored in ChromaDB → retrieved at query time → answered with a grounding-only prompt.
7. **(15s) Mention scope.** Explicitly out of scope by design: reservations, payments, login, admin — this is a knowledge and recommendation layer, not a booking product.

## The 4 Verified Demo Questions

These four questions have been run end-to-end against the live app and vector store, and are the ones to rely on for a live demo:

1. *"I want to learn about haenyeo culture."*
2. *"What can I do in Jeju in October?"*
3. *"I want to meet local people at a traditional market."*
4. *"Tell me about Jeju stone walls."*

### Expected Behavior Per Question

**1. "I want to learn about haenyeo culture."**
- Retrieves chunks from `STORY-0001` (the haenyeo story) and `EXP-0002` (the haenyeo culture walk experience).
- Answer explains haenyeo diving culture and recommends the culture walk as a respectful way to engage with it.
- Inline citation references `STORY-0001` by title and ID.
- Good question to open with — culturally rich, clearly not a generic tourist-attraction answer.

**2. "What can I do in Jeju in October?"**
- Retrieves chunks from `SEASON-0001` (October tangerine season) and related experience/story documents.
- Answer correctly distinguishes **early-season** October (orchard walks, color change) from **peak harvest** in winter — this is the best question to demonstrate seasonal awareness, since it shows the system isn't just pattern-matching on "tangerine."
- Good question to highlight metadata-driven retrieval (the `season` field in front matter).

**3. "I want to meet local people at a traditional market."**
- Retrieves chunks from `EXP-0003` (guided market visit) and `LOCAL-0001` (five-day market explainer).
- Answer recommends visiting a five-day market (owe-il-jang), mentions arriving early and sampling local food like bingtteok.
- Good question to show cross-category retrieval — pulls from both `experiences` and `local_life`.

**4. "Tell me about Jeju stone walls."**
- Retrieves all chunks from `CULTURE-0001` (batdam stone walls).
- Answer explains the dry-stone construction, wind-permeability design, and GIAHS agricultural heritage recognition.
- Most reliable, focused single-document answer — good choice if you only have time for one question.

## What to Say When Explaining RAG

> "Instead of asking a language model to answer from memory, the system first retrieves the most relevant pieces of a curated knowledge base — then the model is instructed to answer *only* from what was retrieved. If the knowledge base doesn't cover something, the model is prompted to say so rather than guess. That's the difference between a chatbot that sounds confident and a system that's actually grounded."

Optional technical follow-up: "Retrieval uses OpenAI embeddings and a ChromaDB vector store — documents are chunked, embedded, and indexed once; each query embeds the question and does a similarity search against that index."

## What to Say When Explaining JEJU-KB

> "JEJU-KB is the knowledge base behind the assistant — not scraped web content, but structured Markdown documents with a formal schema: each one has an ID, category, region, season, tags, and source. It's organized into ten categories — things like local life, seasonal living, stories, food, and culture — so the system can filter and reason about content, not just pattern-match on text."

If asked about coverage honestly: "Right now six of the ten categories are populated with real content — about ten documents total. The other four have the folder structure ready but no content yet, which is the most obvious next step."

## What to Say When Explaining Source Attribution

> "Every answer comes with its sources — not just a vague 'according to my training data,' but the actual document ID, title, category, and file path that grounded the answer. That's what makes 'authentic' a checkable claim instead of a marketing word — you can go open the exact Markdown file the answer came from."

## Known Limitations

Be upfront if asked — this builds more credibility than dodging:

- Knowledge coverage is partial: 6 of 10 categories, ~10 documents total.
- English only — no multi-language support yet.
- Each question is answered independently; there's no multi-turn conversational memory feeding retrieval yet.
- The vector store is a full rebuild each time (`python3 rag/vectordb.py`) — no incremental re-ingestion yet.
- A few narrative "story" documents are explicitly composite/illustrative content, flagged as such in their own source notes, pending real attributed sourcing.
- No reservation, payment, login, or admin features — intentionally out of scope for this project.

## Future Roadmap Talking Points

- Populate the remaining four JEJU-KB categories (festivals, government, transportation, tourism).
- Multi-language support (Korean, Japanese, Chinese).
- Multi-turn, context-aware follow-up questions.
- A community/curator content pipeline with review gating, so local contributors could eventually add stories directly.
- An evaluation harness to systematically track groundedness and hallucination rate as the knowledge base grows.
- The underlying pattern (structured knowledge base + RAG) is designed to generalize beyond Jeju to other regions.

## Screenshots to Capture Later

Placeholders only — no screenshots have been captured yet. Save captured images to `assets/screenshots/` when ready:

- **Home screen** — title, subtitle, description, and sidebar with example questions visible.
- **Answer with inline citation** — a rendered answer showing an inline source citation (e.g. `("Batdam: The Black Stone Walls of Jeju", CULTURE-0001)`).
- **Sources expander** — the expanded "Sources (N)" panel showing id, title, category, chunk_id, and file_path for a result.
- **Sidebar example questions** — the sidebar panel with all 4 example question buttons visible.
