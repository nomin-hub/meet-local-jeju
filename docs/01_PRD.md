# Meet Local Jeju — Product Requirement Document (PRD)

**Document Owner:** Product & Engineering
**Status:** Draft v1.0
**Audience:** Investors, Engineering Team, Design Team

---

## 1. Vision

Meet Local Jeju is an AI-powered travel companion that helps international visitors experience Jeju Island the way locals do — not just the way guidebooks tell them to.

Jeju is one of the most visited islands in Asia, yet most visitors leave having seen only a narrow, repeated slice of it: the same photo spots, the same cafes, the same curated "top 10" lists. Underneath that surface is a distinct island culture — haenyeo (women divers), volcanic geography, seasonal farming rhythms, dialect, shamanic tradition, and a food culture shaped by isolation and the sea — that most travelers never encounter because it isn't packaged for them.

Our vision is to make that deeper layer of Jeju accessible to anyone, in their own language, through a conversational AI grounded in trustworthy, well-organized local knowledge. Meet Local Jeju is not a booking engine or a listicle generator — it is a knowledgeable local friend, available on demand, that helps travelers understand and engage with Jeju authentically.

## 2. Problem Statement

International travelers visiting Jeju face three compounding problems:

1. **Homogenized recommendations.** Search engines, blogs, and mainstream travel apps converge on the same handful of attractions, driven by SEO and social media virality — not by what is authentically Jeju.
2. **Fragmented, inaccessible local knowledge.** Rich information about Jeju's culture, seasonal activities, festivals, and local stories exists — scattered across Korean-language government sites, local blogs, and community sources — but it is not consolidated, not curated, and rarely available in English or other languages.
3. **No trustworthy filter for "authenticity."** Existing tools optimize for popularity or paid placement, not for cultural authenticity or seasonal relevance. Travelers have no reliable way to ask a nuanced question like *"What can I do that feels genuinely local in Jeju in November?"* and get a grounded, trustworthy answer.

The result: travelers spend significant time researching and still end up with a generic itinerary, while the authentic, seasonal, and cultural richness of Jeju remains largely invisible to outsiders.

## 3. Goals

**Product Goals**
- Provide accurate, trustworthy, and culturally authentic answers about Jeju through a conversational interface.
- Surface local experiences, seasonal activities, and cultural context that are underrepresented in mainstream travel content.
- Make Jeju's local knowledge accessible in English (and eventually other languages) for international travelers.

**Business Goals**
- Establish Meet Local Jeju as the trusted AI knowledge layer for authentic Jeju travel, positioning for future partnerships with local governments, tourism boards, and community organizations.
- Build a defensible, curated knowledge base as a long-term data moat, distinct from generic LLM knowledge.
- Validate demand for a scalable, replicable "authentic local AI guide" model that could extend to other regions post-Jeju.

**Engineering Goals**
- Ship a reliable, low-hallucination RAG system with clear source grounding.
- Build an ingestion and retrieval architecture that scales cleanly as the knowledge base grows across categories and languages.

## 4. Target Users

- **International independent travelers** visiting Jeju (leisure, first-time or repeat), who prefer self-directed exploration over packaged tours.
- **Long-stay visitors and digital nomads** spending weeks to months on Jeju, wanting deeper, non-repetitive engagement with the island over time.
- **Culturally curious travelers** specifically seeking local, non-touristic experiences (food, festivals, nature, tradition) rather than checklist sightseeing.

Out of scope for MVP: domestic (Korean) travelers, group/package tour operators, and business travelers.

## 5. User Personas

### Persona 1 — "Curious Claire"
- 29, from Canada, traveling solo for 10 days.
- Has visited generic "best of Jeju" blog posts but wants something more real.
- Speaks no Korean. Comfortable with apps and conversational AI.
- Goal: "I don't want to just see what everyone else sees — I want to understand what makes Jeju, Jeju."

### Persona 2 — "Slow-travel Sam"
- 34, from Germany, working remotely on Jeju for 6 weeks.
- Has time to explore deeply and repeatedly, but keeps running out of new, meaningful things to do.
- Wants seasonal and local-calendar awareness (e.g., what's happening this month, not evergreen lists).
- Goal: "I'm here long enough to live like a local — I just don't know how."

### Persona 3 — "Heritage-seeking Hana"
- 45, Korean-American, visiting with family to reconnect with cultural roots.
- Understands some Korean culture broadly, but not Jeju-specific traditions (haenyeo culture, dialect, shamanism, volcanic geography).
- Wants depth and credible cultural context, not superficial trivia.
- Goal: "I want to explain to my kids what makes this island's culture unique, accurately."

## 6. User Journey

1. **Entry** — User opens the Meet Local Jeju web app (Streamlit-based chat interface) with a question or general interest (e.g., "What should I do in Jeju in November that isn't touristy?").
2. **Query** — User asks a natural-language question in their own words, in English.
3. **Retrieval** — The system retrieves relevant, curated knowledge from the vector database (culture, seasonal activity, festivals, food, transportation, local stories, government/public info).
4. **Grounded response** — The AI synthesizes a conversational answer grounded in retrieved sources, including cultural context and, where relevant, seasonal timing.
5. **Exploration** — User asks follow-up questions, narrowing by interest (e.g., food, nature, tradition) or by practical constraint (e.g., transportation, season, region of the island).
6. **Discovery** — User comes away with a short list of authentic, locally-grounded experiences and enough cultural context to engage with them meaningfully and respectfully.
7. **Return use** — For long-stay users, the app becomes a recurring reference point across the duration of their stay, surfacing new seasonal/cultural content over time.

*Note: The journey intentionally ends at discovery and understanding — not at booking or transaction (see [Non Goals](#8-non-goals)).*

## 7. Core Features (MVP Only)

1. **Conversational Q&A Interface (Streamlit)**
   A simple chat interface where users ask free-form questions about Jeju and receive natural-language answers.

2. **Retrieval-Augmented Generation (RAG) Pipeline**
   All answers are grounded in a curated knowledge base (not raw LLM knowledge alone), retrieved via ChromaDB and synthesized via an LLM through LangChain.

3. **Curated Knowledge Base Ingestion**
   A structured pipeline to ingest documents across defined categories (see Section 12) into the vector store.

4. **Category-Aware Retrieval**
   Retrieval that can be informed by document category/metadata (e.g., festivals, food, culture) to improve relevance of answers.

5. **Source Transparency**
   Responses indicate what kind of source informed the answer (e.g., "based on local cultural records" vs. "based on seasonal farming information"), to build user trust without overwhelming them with citations.

6. **Seasonal Awareness**
   The system is aware of seasonality in its knowledge base (e.g., farming calendars, festival dates) and can tailor answers to the current or specified time of year.

7. **English-Language Experience**
   Full MVP experience delivered in English, targeting international travelers.

## 8. Non Goals

To keep the MVP focused, the following are explicitly **out of scope**:

- **No reservation or booking functionality** (restaurants, accommodations, tours, transportation).
- **No payment processing** of any kind.
- **No real-time itinerary planning or scheduling** (e.g., auto-generated day-by-day plans).
- **No user-generated content or social features** (reviews, posting, community forums) in MVP.
- **No native mobile app** — MVP is web-based only.
- **No multi-language support beyond English** in MVP (future roadmap item).
- **No real-time data integrations** (e.g., live weather, live transit schedules) in MVP.
- **No personalized user accounts/profiles** in MVP — sessions are stateless or lightly session-scoped.

## 9. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | The system must accept free-form natural-language questions from users via a chat interface. | Must |
| FR-2 | The system must retrieve relevant document chunks from a vector database based on the user's query. | Must |
| FR-3 | The system must generate a natural-language response grounded in retrieved content, using an LLM (OpenAI API via LangChain). | Must |
| FR-4 | The system must support ingestion of documents across all defined knowledge base categories (Section 12). | Must |
| FR-5 | The system must attach category metadata to ingested documents to support filtered/prioritized retrieval. | Must |
| FR-6 | The system must be able to indicate the general nature/category of the source behind a given answer. | Should |
| FR-7 | The system must handle queries with no strong match in the knowledge base gracefully (e.g., acknowledge limited information rather than fabricating specifics). | Must |
| FR-8 | The system must support conversational follow-up questions within a session. | Should |
| FR-9 | The system must allow the knowledge base to be updated/re-ingested without requiring application code changes. | Must |
| FR-10 | The system must be deployable as a Streamlit web application. | Must |

## 10. Non-functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | **Accuracy / Groundedness:** Responses must be grounded in retrieved knowledge base content; hallucination rate must be minimized and monitored. | Must |
| NFR-2 | **Latency:** Typical response time should be under ~5 seconds for a standard query under normal load. | Should |
| NFR-3 | **Trustworthiness:** The system must avoid fabricating specific facts (dates, prices, locations) not present in the knowledge base. | Must |
| NFR-4 | **Scalability:** The RAG architecture (ingestion, embedding, vector store, retrieval) must scale as document volume and categories grow, without architectural rework. | Must |
| NFR-5 | **Maintainability:** RAG pipeline components (loader, splitter, embeddings, vector store, retriever) must be modular and independently testable. | Must |
| NFR-6 | **Security:** API keys and credentials must be managed via environment variables and never exposed client-side or committed to source control. | Must |
| NFR-7 | **Cost efficiency:** Embedding and LLM API usage should be optimized (e.g., caching, chunking strategy) to control per-query cost. | Should |
| NFR-8 | **Content quality control:** All ingested source content must be reviewed for accuracy and cultural sensitivity before inclusion in the knowledge base. | Must |
| NFR-9 | **Availability:** The application should be reliably available during standard usage hours with graceful degradation on failure (e.g., API errors surfaced clearly, not silently). | Should |

## 11. RAG Strategy

Meet Local Jeju's core differentiator is not the LLM itself, but the **curated, trustworthy knowledge layer** it is grounded in. The RAG strategy is designed around this principle.

**Ingestion**
- Source documents are collected from Jeju public/government resources, local cultural archives, seasonal farming and festival calendars, food and culinary references, transportation information, and community/local story sources.
- Documents are organized into the category structure defined in Section 12 before ingestion, enabling category-aware retrieval.
- Raw content is cleaned and normalized before chunking (see `data/raw/` → `data/processed/` pipeline).

**Chunking**
- Documents are split into retrieval-optimized chunks, with chunking strategy adapted to content type (e.g., narrative cultural stories vs. structured festival/date data).
- Metadata (category, source, season/date relevance where applicable) is preserved at the chunk level.

**Embedding & Storage**
- Chunks are embedded using OpenAI's embedding models and stored in ChromaDB as the vector store.
- Embeddings are cached where feasible to reduce redundant API cost during re-ingestion.

**Retrieval**
- At query time, the system retrieves the most relevant chunks via similarity search, optionally informed by category metadata and, where relevant, seasonal context.
- Retrieval strategy supports future refinement (e.g., MMR for diversity, metadata filtering by category) as usage patterns emerge.

**Generation**
- Retrieved chunks are passed as grounding context to an LLM (via LangChain) to synthesize a natural-language, conversational response.
- Prompting is designed to encourage the model to answer *only* from retrieved context where specific facts are involved, and to be transparent when information is limited — prioritizing trustworthiness over completeness.

**Why RAG (not fine-tuning or raw LLM knowledge)**
- Jeju-specific, hyper-local, and seasonal knowledge is not reliably present in general-purpose LLM training data.
- RAG allows the knowledge base to be updated continuously (new festivals, seasonal changes, corrected information) without retraining a model.
- Grounding responses in retrievable sources is essential to the product's core promise: trustworthy, authentic information — not generic AI-generated travel content.

## 12. Knowledge Base Categories

The knowledge base is organized into the following top-level categories, each independently curated and ingestible:

| Category | Description |
|----------|-------------|
| **Culture** | Jeju traditions, dialect, haenyeo (women divers) heritage, shamanic and folk traditions, local customs and etiquette, local stories and oral history. |
| **Tourism** | General points of interest and geography — included for context, but framed to complement (not replace) authentic local recommendations. |
| **Festivals** | Seasonal and local festivals, community events, traditional ceremonies, and their cultural significance and timing. |
| **Food** | Local Jeju cuisine, seasonal ingredients, traditional dishes, markets, and dining customs distinct from generic restaurant recommendations. |
| **Government** | Official/public information relevant to travelers — public facilities, regulations, safety information, and other administrative context sourced from trusted public documents. |
| **Transportation** | Local transportation context (public transit patterns, practical local travel knowledge) to support authentic exploration beyond taxis/rentals. |
| **Local Stories & Community** | Community-sourced experiences, local perspectives, and stories that convey the lived experience of Jeju beyond official or commercial sources. |

Each category maps directly to a subfolder under `docs/` in the project structure, supporting clear content ownership and independent curation workflows.

## 13. Future Roadmap

**Post-MVP (Near-term)**
- Multi-language support (Korean, Japanese, Chinese, and other major visitor languages).
- Personalized recommendations based on stated interests (e.g., nature, food, tradition) within a session.
- Expanded seasonal intelligence (e.g., proactive seasonal highlights, not just query-driven).

**Mid-term**
- Community contribution pipeline for local stories, with a curation/review workflow to maintain trust and quality.
- Partnerships with Jeju local government and cultural organizations for verified, official content feeds.
- Map-based and visual exploration layer on top of the conversational interface.

**Long-term**
- Extension of the "authentic local AI guide" model to other regions/islands beyond Jeju, reusing the RAG architecture with region-specific knowledge bases.
- Optional integration layer for booking/reservation partners (kept strictly separate from the core authentic-recommendation experience, and only introduced if it does not compromise trust or neutrality).
- Offline/low-connectivity access for travelers exploring remote parts of the island.

## 14. Success Metrics

**Product / Engagement Metrics**
- **Query volume and session depth** — number of questions asked per session, indicating exploratory engagement.
- **Follow-up question rate** — proportion of sessions with multi-turn conversation, indicating perceived usefulness.
- **Category coverage of queries** — breadth of knowledge base categories being engaged with (not just "tourism").
- **Return usage rate** — for long-stay personas, frequency of return visits over the course of a trip.

**Quality Metrics**
- **Groundedness rate** — proportion of responses verifiably grounded in retrieved sources (measured via internal evaluation/spot-checking).
- **Hallucination rate** — proportion of responses containing unsupported specific claims, tracked and minimized over time.
- **User-reported helpfulness** — qualitative/quantitative feedback on whether responses felt "authentic" and useful vs. generic.

**Business / Strategic Metrics**
- **Knowledge base growth** — number of curated documents/sources per category over time, as a proxy for data moat strength.
- **Investor/partner validation** — interest and engagement from Jeju tourism-adjacent organizations as an early signal of go-to-market viability.
- **Cost per query** — LLM/embedding API cost per user query, tracked for unit economics as usage scales.

---

*This document defines the MVP scope for Meet Local Jeju. Features explicitly marked as Non Goals (Section 8) — including reservations and payments — are intentionally excluded to keep the MVP focused on establishing trust and authenticity as the product's core value proposition before layering in transactional functionality.*
