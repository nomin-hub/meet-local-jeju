# Meet Local Jeju — Demo Script

**Document Owner:** Product & Engineering
**Status:** Draft v1.0
**Length:** 1-minute, 3-minute, and full (~6-minute, both modes in depth) versions
**Related:** [`README.md`](../../README.md), [`01_PRD.md`](../01_PRD.md), [`01_PRODUCT_BRIEF.md`](01_PRODUCT_BRIEF.md), [`02_ARCHITECTURE.md`](02_ARCHITECTURE.md)

---

## Demo Goal

Show that Meet Local Jeju answers travel questions about Jeju Island **grounded in a curated knowledge base**, not from general AI memory — and that every answer is traceable back to a specific source document. The demo should make one thing obvious: this is a real RAG system with structured, attributable knowledge behind it, not a thin wrapper around a chatbot.

## Target Audience

- Recruiters and hiring managers evaluating AI engineering portfolio work.
- Engineers assessing RAG architecture and system design decisions.
- Non-technical stakeholders interested in the product concept (authentic local travel, not generic tourism).

Calibrate depth accordingly: lead with the product experience, then go as deep into architecture as the audience wants.

## 1-Minute Demo Script

Use when time is extremely tight — a recruiter screen-share, or the last minute of a longer conversation.

1. **(10s)** "Meet Local Jeju is a RAG-powered MVP that helps travelers discover authentic Jeju experiences — grounded in a curated knowledge base, not generic AI chatter."
2. **(25s)** Click a sidebar example question in Chat Mode (e.g. *"Tell me about Jeju stone walls."*) and narrate while it loads: "It retrieves from a structured knowledge base first, then answers only from what it found."
3. **(15s)** Open the Sources expander: "Every answer is traceable back to a specific document — that's the point."
4. **(10s)** "It's an MVP — no booking, no payments, no real hosts yet. The current focus is proving the knowledge and recommendation layer works before building any of that."

## 3-Minute Demo Script

Use for a standard portfolio walkthrough covering both modes.

1. **(20s) Frame it.** "Most travel AI recommends the same popular spots. Meet Local Jeju is built to surface what's actually local, grounded in a curated knowledge base called JEJU-KB."
2. **(30s) Chat Mode.** Click a sidebar example question. While it loads: "This isn't the model's memory — it retrieved relevant JEJU-KB chunks first, then answered only from that context."
3. **(30s) Sources.** Open the Sources expander: id, title, category, chunk ID, file path. "That's what makes 'authentic' a checkable claim, not a marketing word."
4. **(40s) Recommendation Mode.** Switch modes, pick 2-3 interests (e.g. *culture*, *local people*, *food*), submit. While it loads: "Same retriever, same grounding rules — just a structured recommendation instead of a free-form answer."
5. **(30s) Walk the output.** Point out the structure: Summary → Recommended Local Experiences → Suggested 1-Day Flow → Sources.
6. **(30s) Scope and vision.** "This is a recommendation feature, not a booking system — no prices, no availability, no reservations. It's Phase 1 of a longer roadmap toward a trip planner and local experience marketplace, but none of that exists yet."

## Recommended Live Demo Sequence

The canonical step-by-step order for a live walkthrough — this is the backbone both scripts above are built from:

1. Open the app.
2. Explain the problem (generic travel AI vs. grounded local knowledge).
3. Ask a haenyeo question in Chat Mode.
4. Switch to Recommendation Mode.
5. Select food / culture / local people as interests.
6. Show the recommendation results and sources.
7. Explain the long-term platform vision honestly (Phase 1 today; trip planner and marketplace are later, unbuilt phases).

For exact timing and talking points behind each step, see [Recommended Demo Flow](#recommended-demo-flow) (chat mode, ~4 min) and [Recommendation Mode Demo Flow](#recommendation-mode-demo-flow) (~2 min) below — together they form the full ~6-minute version of this sequence.

## App Setup Checklist

Run through this **before** presenting, not during:

- [ ] `.env` exists locally with a valid `OPENAI_API_KEY` (never shown on screen).
- [ ] Vector store is built: `vector_db/chroma/` exists and is current — run `python3 rag/vectordb.py` if `knowledge/` has changed since the last build.
- [ ] `streamlit run app.py` starts cleanly with no errors in the terminal.
- [ ] Home screen loads with **no** "vector store hasn't been built yet" warning banner, and the "Featured Local Ideas" board (6 cards) renders correctly.
- [ ] Sidebar shows all 4 example question buttons in "Ask Local Jeju AI" mode.
- [ ] Switch to "Get Experience Recommendations" mode and confirm the form (interests, style, season, transportation, area, notes) renders correctly.
- [ ] Do one silent test question *and* one silent test recommendation beforehand to confirm the OpenAI API key is live and quota is available — an auth or quota error mid-demo is the single most disruptive failure mode.
- [ ] Browser window sized wide enough that the sidebar is visible without collapsing (desktop width, not a narrow/mobile viewport).

## Recommended Demo Flow

**Total: ~4 minutes**

1. **(30s) Frame the problem.** Before opening the app: most travel AI just recommends the same tourist attractions everyone already knows about. Meet Local Jeju is built to surface what's *actually* local — culture, seasonal life, food, stories — and to be honest about what it does and doesn't know.
2. **(20s) Show the home screen.** Point out the title, subtitle ("Discover Jeju Beyond Tourism"), the "Where This Is Headed" cards, and scroll to the "Featured Local Ideas" board — six Pinterest-style cards browsable before typing anything. Mention it's static, developer-authored content for now, not a live catalog.
3. **(60s) Run one example question live.** Click a sidebar example button (don't type — it's faster and more reliable live) and narrate what's happening while it loads: "This isn't going to the model's memory — it's retrieving the most relevant chunks from a curated knowledge base first, then generating an answer grounded in only that."
4. **(45s) Open the Sources expander.** This is the proof point of the whole demo. Show the ID, title, category, chunk ID, and file path for each source. Point out that the answer's inline citation (e.g. `("Batdam: The Black Stone Walls of Jeju", CULTURE-0001)`) matches a real, traceable document.
5. **(45s) Run a second question** (pick one that shows a different category, e.g. the market question after a culture question) to show breadth across the knowledge base, not a single lucky answer.
6. **(30s) Close with architecture, if the audience is technical.** One sentence per stage: Markdown + YAML knowledge documents → chunked → embedded with OpenAI → stored in ChromaDB → retrieved at query time → answered with a grounding-only prompt.
7. **(15s) Mention scope.** Explicitly out of scope by design: reservations, payments, login, admin — this is a knowledge and recommendation layer, not a booking product.

## Recommendation Mode Demo Flow

**Total: ~2 minutes, run after the chat flow above (or standalone if time is short).**

1. **(10s) Switch modes.** In the sidebar, select "Get Experience Recommendations." Point out that the example-question buttons are replaced by the recommendation form — same knowledge base, different interaction style.
2. **(30s) Fill the form live.** Pick 2-3 travel interests (e.g. *culture*, *local people*, *food*), a travel style (e.g. *solo traveler*), and type a season (e.g. *October*) and preferred area (e.g. *Seogwipo*). Narrate: "This isn't a filter over a database of listings — it's converted into a natural-language query and run through the same retriever as chat mode."
3. **(30s) Submit and narrate while it loads.** "Same grounding rules as chat mode: only recommend experiences the knowledge base actually supports, and never invent a price, schedule, address, or host name."
4. **(30s) Walk through the structured output.** Point out the four sections in order: **Summary** → **Recommended Local Experiences** (each with why it fits + cultural connection) → **Suggested 1-Day Flow** → **Sources**. This structure is what separates it from a single free-form paragraph.
5. **(20s) Open the Sources expander** — same id/title/category/chunk_id/file_path format as chat mode, reinforcing that recommendations are as traceable as answers.
6. **(10s) Explicitly state scope.** "This is a recommendation feature, not a booking flow — there's no availability check, no price, no way to reserve anything here. That's intentional; see the long-term vision for where booking would eventually fit."

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

## What to Say About the Visual Design

> "The visual direction is inspired by Pinterest-style discovery, because travelers often want to browse and save local ideas before planning a trip."

Useful follow-up if asked why: chat and forms both require the traveler to already know what to ask for. A browsable board of local ideas — even a small, static one — gives them something to react to first. The "Save idea - prototype only" badge on each card is intentionally honest: it looks like a real product affordance because that's the direction this is headed, but nothing is actually saved in this MVP.

## What to Say About the Long-Term Vision

If asked "is this going to be like Airbnb?" or "where is this headed?" — answer honestly, in this order: what exists today, then the direction, without implying anything beyond Phase 1 is built.

> "Today this is a RAG-powered knowledge assistant — that's Phase 1. The long-term vision is a local experience and trip-planning platform: personalized recommendations, host profiles for people like farmers and haenyeo guides, and eventually an Airbnb-like booking and review system. But this MVP focuses on the knowledge and recommendation layer first — before building booking, payment, or host-management features, the project validates whether AI can understand traveler intent and match it with structured local knowledge. None of the marketplace or booking pieces exist yet."

Full phase-by-phase detail: [`docs/product/01_PRODUCT_BRIEF.md`](01_PRODUCT_BRIEF.md). Avoid demoing or implying any booking, payment, host, or marketplace functionality — none of it exists in the running app.

## Known Limitations

Be upfront if asked — this builds more credibility than dodging:

- Knowledge coverage is partial: 6 of 10 categories, ~10 documents total.
- English only — no multi-language support yet.
- Each question is answered independently; there's no multi-turn conversational memory feeding retrieval yet.
- The vector store is a full rebuild each time (`python3 rag/vectordb.py`) — no incremental re-ingestion yet.
- A few narrative "story" documents are explicitly composite/illustrative content, flagged as such in their own source notes, pending real attributed sourcing.
- Recommendation mode suggests at most 3 experiences and an optional 1-day sequencing — it does not build multi-day itineraries and has no concept of real-time availability.
- No reservation, payment, login, host onboarding, or admin features — intentionally out of scope for this project.

## Future Roadmap Talking Points

**Phase 1 near-term (this codebase):**
- Populate the remaining four JEJU-KB categories (festivals, government, transportation, tourism).
- Multi-language support (Korean, Japanese, Chinese).
- Multi-turn, context-aware follow-up questions.
- A community/curator content pipeline with review gating, so local contributors could eventually add stories directly.
- An evaluation harness to systematically track groundedness and hallucination rate as the knowledge base grows.
- The underlying pattern (structured knowledge base + RAG) is designed to generalize beyond Jeju to other regions.

**Beyond Phase 1 (platform vision, not built):** personalized recommendations (Phase 2) → multi-day trip planner (Phase 3) → local host/experience dataset (Phase 4) → marketplace prototype with a mock booking flow (Phase 5) → real platform with host onboarding, booking, reviews, payments, and partnerships (Phase 6). See [`01_PRODUCT_BRIEF.md`](01_PRODUCT_BRIEF.md) for the full breakdown.

## Screenshots to Capture Later

Placeholders only — no screenshots have been captured yet. Save captured images to `assets/screenshots/` when ready:

- **Home screen** — title, subtitle, description, and sidebar with example questions visible.
- **Answer with inline citation** — a rendered answer showing an inline source citation (e.g. `("Batdam: The Black Stone Walls of Jeju", CULTURE-0001)`).
- **Sources expander** — the expanded "Sources (N)" panel showing id, title, category, chunk_id, and file_path for a result.
- **Sidebar example questions** — the sidebar panel with all 4 example question buttons visible.
- **Recommendation form** — the "Get Experience Recommendations" mode with the preference form visible (interests, style, season, transportation, area, notes).
- **Structured recommendation output** — a rendered recommendation showing the Summary / Recommended Local Experiences / Suggested 1-Day Flow / Sources structure.
