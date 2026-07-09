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

1. **(10s)** "Meet Local Jeju is a RAG-powered MVP that helps travelers discover authentic Jeju experiences — grounded in a curated knowledge base, not generic AI chatter. It's styled as a mobile app prototype." Show the Home screen's 2-column card grid.
2. **(25s)** Tap the **AI Assistant** tab, open "Try an example," pick a question (e.g. *"Tell me about Jeju stone walls."*), and narrate while it loads: "It retrieves from a structured knowledge base first, then answers only from what it found."
3. **(15s)** Point at the source chips under the answer: "Every answer is traceable back to a specific document — that's the point."
4. **(10s)** "It's an MVP — no booking, no payments, no real hosts yet. The current focus is proving the knowledge and recommendation layer works before building any of that."

## 3-Minute Demo Script

Use for a standard portfolio walkthrough covering all three screens.

1. **(20s) Frame it.** "Most travel AI recommends the same popular spots. Meet Local Jeju is built to surface what's actually local, grounded in a curated knowledge base called JEJU-KB — and it's designed as a mobile app prototype, not a desktop dashboard."
2. **(20s) Home screen.** Point out the phone-frame layout and the 2-column Pinterest-style card grid — image-first cards with category chips, browsable before typing anything.
3. **(30s) AI Assistant — chat.** Tap the AI Assistant tab, ask a question. While it loads: "This isn't the model's memory — it retrieved relevant JEJU-KB chunks first, then answered only from that context."
4. **(20s) Sources.** Point out the source chips and the fallback expander: id, title, category, chunk ID, file path. "That's what makes 'authentic' a checkable claim, not a marketing word."
5. **(30s) AI Assistant — recommendations.** Toggle to "Get recommendations," pick 2-3 interests (e.g. *culture*, *local people*, *food*), submit. While it loads: "Same retriever, same grounding rules — just a structured recommendation instead of a free-form answer."
6. **(15s) Walk the output.** Point out the structure: Summary → Recommended Local Experiences → Suggested 1-Day Flow → Sources.
7. **(25s) My Page + vision.** Tap My Page: "This is mock UI — no login, nothing is actually saved. It previews where a future logged-in experience would live." Close with: "This is Phase 1 of a longer roadmap toward a trip planner and local experience marketplace, but none of that exists yet."

## Recommended Live Demo Sequence

The canonical step-by-step order for a live walkthrough:

1. Show Home screen.
2. Browse Pinterest-style local experience cards.
3. Open AI Assistant.
4. Ask a RAG question.
5. Use recommendation mode.
6. Show My Page mock saved ideas.
7. Explain future Trip Planner / marketplace direction honestly (Phase 1 today; trip planner and marketplace are later, unbuilt phases).

For exact timing and talking points behind each step, see [Full Demo Flow](#full-demo-flow) below — it's the ~6-minute expanded version of this sequence.

## App Setup Checklist

Run through this **before** presenting, not during:

- [ ] `.env` exists locally with a valid `OPENAI_API_KEY` (never shown on screen).
- [ ] Vector store is built: `vector_db/chroma/` exists and is current — run `python3 rag/vectordb.py` if `knowledge/` has changed since the last build.
- [ ] `streamlit run app.py` starts cleanly with no errors in the terminal.
- [ ] Home screen loads inside the phone-frame layout with **no** import errors, and the 2-column "Featured Local Ideas" card grid (6 cards) renders correctly.
- [ ] Bottom tab bar shows all three tabs (Home / AI Assistant / My Page) and switching between them works.
- [ ] On the AI Assistant tab, confirm both the "Ask a question" and "Get recommendations" toggle states render correctly, and there's **no** "vector store hasn't been built yet" warning.
- [ ] On My Page, confirm the avatar, Pins/Boards/Trips tabs, and saved-card grid render correctly.
- [ ] Do one silent test question *and* one silent test recommendation beforehand to confirm the OpenAI API key is live and quota is available — an auth or quota error mid-demo is the single most disruptive failure mode.
- [ ] Browser window sized to a mobile-ish width (~400-500px) or use a real mobile viewport — the phone-frame design is meant to be seen narrow, not stretched wide.

## Full Demo Flow

**Total: ~6 minutes.** Expands the [Recommended Live Demo Sequence](#recommended-live-demo-sequence) above with exact timing and talking points.

1. **(20s) Frame the problem.** Before opening the app: most travel AI just recommends the same tourist attractions everyone already knows about. Meet Local Jeju is built to surface what's *actually* local — culture, seasonal life, food, stories — and to be honest about what it does and doesn't know.
2. **(30s) Show the Home screen.** Point out the phone-frame layout (rounded card, centered, mobile-width) and the honesty badges ("Prototype only," "Booking not available in MVP") right under the header.
3. **(40s) Browse the Pinterest-style local experience cards.** Scroll the 2-column grid — image-first gradient cards, category chip, title, description, area, "Save idea - prototype only" badge. Mention cards are loaded from a structured JSON dataset, not hardcoded, and each links back to real JEJU-KB documents.
4. **(15s) Open AI Assistant.** Tap the AI Assistant tab in the bottom nav. Point out the honesty badges ("Grounded in JEJU-KB," "No booking or payment") and the "Ask a question" / "Get recommendations" toggle.
5. **(45s) Ask a RAG question.** Open "Try an example," pick one (or type your own), and narrate while it loads: "This isn't going to the model's memory — it's retrieving the most relevant chunks from a curated knowledge base first, then generating an answer grounded in only that." Point out the chat bubble styling and the source chips + fallback expander underneath the answer.
6. **(45s) Ask a second question** (a different category, e.g. the market question after a culture question) to show breadth across the knowledge base, not a single lucky answer.
7. **(60s) Use recommendation mode.** Toggle to "Get recommendations," fill the Travel Preference Card (2-3 interests, a travel style, optionally a season and area), submit. Narrate while it loads: "Same retriever, same grounding rules as chat — just a structured recommendation instead of a free-form answer." Walk through the output: Summary → Recommended Local Experiences → Suggested 1-Day Flow → Sources.
8. **(30s) Show My Page mock saved ideas.** Tap My Page. Point out the avatar, the Pins/Boards/Trips tabs, and that Pins reuses the same experience dataset as "saved" ideas. State plainly: "No login, no real saving — this previews where a future account-based experience would live."
9. **(25s) Explain the future Trip Planner / marketplace direction, honestly.** "This is Phase 1 of a longer roadmap — personalized recommendations, a trip planner, host profiles, and eventually an Airbnb-like marketplace are the direction, but none of that is built. This MVP is deliberately the knowledge and recommendation layer first."

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

> "The Pinterest-style cards are now backed by structured JSON data, which allows the prototype to evolve from static UI into a real product data layer."

If asked to go one level deeper: each card is a JSON file in `data/experiences/`, loaded and validated by `utils/experience_loader.py`, and linked back to real JEJU-KB documents via a `related_kb_ids` field — the same "separate data from rendering" pattern used for the knowledge base itself, just applied one layer up, toward a future Explore Page or Trip Planner.

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

- **Home screen** — the phone-frame layout with the 2-column Pinterest-style card grid visible.
- **AI Assistant — chat with source chips** — a rendered answer showing the chat bubble, inline citation, and source chips underneath.
- **Full source detail expander** — the expanded fallback expander showing id, title, category, chunk_id, and file_path for a result.
- **Bottom tab navigation** — the Home / AI Assistant / My Page tab bar visible at the bottom of the phone frame.
- **Recommendation form** — the "Get recommendations" toggle state with the Travel Preference Card form visible (interests, style, season, transportation, area, notes).
- **Structured recommendation output** — a rendered recommendation showing the Summary / Recommended Local Experiences / Suggested 1-Day Flow / Sources structure.
- **My Page mock saved ideas** — the avatar, Pins/Boards/Trips tabs, and saved-card grid.
