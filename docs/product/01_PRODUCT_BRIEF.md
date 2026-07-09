# Meet Local Jeju — Product Brief: From RAG Assistant to Local Experience Platform

**Document Owner:** Product & Engineering
**Status:** Draft v1.0
**Related:** [`README.md`](../../README.md), [`01_PRD.md`](../01_PRD.md), [`02_ARCHITECTURE.md`](02_ARCHITECTURE.md), [`05_DEMO_SCRIPT.md`](05_DEMO_SCRIPT.md)

---

## Purpose of This Document

[`docs/01_PRD.md`](../01_PRD.md) defines the requirements and scope of the **current MVP** — a RAG-powered knowledge assistant. This document extends that with the **long-term product vision**: where Meet Local Jeju is headed once the MVP has validated its core premise. Nothing described here as "future" or "planned" is implemented today. Where this document and the PRD's own brief long-term mentions overlap, this document is the fuller, authoritative statement of direction; the PRD's Non-Goals (reservation, payment, login, admin — all explicitly out of MVP scope) still stand for the current build.

## Long-Term Vision

Meet Local Jeju starts as a RAG-powered local knowledge assistant — today, that's the entire product. But the long-term goal is larger: to become a **trusted local experience and trip-planning platform** that connects international travelers with authentic Jeju local life — not just answers questions about it.

The current MVP is **Phase 1** of a multi-phase product roadmap. Phase 1 exists to answer a narrower, more fundamental question before any marketplace, booking, or host-facing feature is built: *can AI reliably understand a traveler's intent and match it to structured, trustworthy local knowledge?* Everything past Phase 1 — recommendations, trip planning, a host/experience dataset, and eventually a marketplace — depends on that foundation holding up.

## Future Platform Direction

The long-term platform direction includes, in rough order of dependency:

- **Personalized Jeju trip planner** — sequencing recommendations across days and regions based on a traveler's stated interests, time available, and season.
- **Local experience marketplace** — a searchable, filterable catalog of authentic local experiences (not generic tours), sourced from and consistent with JEJU-KB's category taxonomy.
- **Host profiles** — for the people behind local experiences: farmers, haenyeo culture guides, market guides, artisans, and local storytellers.
- **Stay + experience packages** — bundling accommodation with authentic local activities, rather than treating "where to stay" and "what to do" as separate problems.
- **Airbnb-like booking and review system** — in the long term, real booking, payment, and review infrastructure connecting travelers directly with local hosts.

**None of this exists yet.** No host onboarding, no booking flow (mock or real), no payment processing, no user accounts, and no review system are implemented in the current codebase. This section describes direction, not current capability — see [Current Reality Check](#current-reality-check) below.

## Product Evolution Roadmap

| Phase | Name | Status | What It Means |
|---|---|---|---|
| **1** | RAG-powered local knowledge assistant | ✅ **Current MVP (this repo)** | Conversational Q&A grounded in JEJU-KB, with source attribution. No personalization, no planning, no bookable inventory. |
| **2** | Personalized experience recommendation mode | 🔜 Planned, not started | Recommendations weighted by a traveler's stated interests/persona (e.g. slow-travel, heritage-seeking) within a session — still Q&A, no itinerary, no booking. |
| **3** | Multi-day trip planner | 🔭 Future | Sequencing multiple recommendations by region, season, and time available into a suggested multi-day plan — still informational, no reservations made. |
| **4** | Local host and experience dataset | 🔭 Future | Structuring real local hosts and bookable-shaped experiences as data (extending the KDS schema) — a data-modeling milestone, not user-facing host accounts yet. |
| **5** | Marketplace prototype with mock booking flow | 🔭 Future | A UI-only mock booking flow to validate the marketplace experience end-to-end — explicitly **no real payments or transactions**. |
| **6** | Real platform | 🔭 Long-term vision, not started | Host onboarding, real booking, reviews, payments, and local/tourism-board partnerships — the full Airbnb-like platform. |

Phase 1's own near-term implementation roadmap (populating remaining JEJU-KB categories, multi-language support, etc.) is tracked separately in the [README's Future Roadmap](../../README.md#future-roadmap) and [PRD Section 13](../01_PRD.md#13-future-roadmap) — those are refinements *within* Phase 1, not the same as Phases 2–6 above.

## Differentiation

Meet Local Jeju is not trying to recommend famous tourist spots. It is designed to help travelers discover local stories, seasonal living, people, food, culture, and authentic island experiences. That framing is what differentiates it from adjacent categories of product:

- **vs. General travel guide apps** — Guide apps aggregate popularity-ranked attractions (the same "top 10" everywhere). Meet Local Jeju's knowledge base is deliberately curated around authenticity and seasonality, not search-engine visibility, and every answer is source-attributed rather than presented as an anonymous listicle.
- **vs. Generic AI chatbots** — A general-purpose chatbot answers Jeju questions from broad training memory: plausible, but ungrounded, unattributed, and prone to confidently stating specifics it doesn't actually know. Meet Local Jeju retrieves from a structured, versioned knowledge base first and is explicitly prompted to say when it doesn't know something, rather than guess.
- **vs. Airbnb** — Airbnb is a booking and marketplace platform for stays (and, more recently, experiences) — its core value is transaction infrastructure. Meet Local Jeju's Phase 1–3 focus is the opposite end of the funnel: helping a traveler *understand* what's authentically worth doing before anything is booked. The long-term vision (Phase 5–6) borrows Airbnb's marketplace pattern, but only after the knowledge/recommendation layer is proven — not as a starting point.
- **vs. Traditional tour platforms** — Tour platforms sell pre-packaged, one-size-fits-all itineraries, typically commission-driven. Meet Local Jeju's recommendations are grounded in a traveler's actual question and Jeju's cultural/seasonal context, not a fixed catalog of bookable packages.

## Demo Talking Point

For portfolio presentations, this paragraph summarizes the project's current scope and rationale honestly:

> This MVP focuses on the knowledge and recommendation layer first. Before building booking, payment, or host-management features, the project validates whether AI can understand traveler intent and match it with structured local knowledge.

## Current Reality Check

To keep this vision document honest and unambiguous about what exists today:

| Capability | Status |
|---|---|
| Conversational Q&A grounded in JEJU-KB | ✅ Implemented (Phase 1) |
| Source attribution (title, category, chunk ID, file path) | ✅ Implemented (Phase 1) |
| Personalized recommendations by traveler persona | ❌ Not implemented |
| Multi-day trip planning / itineraries | ❌ Not implemented |
| Local host profiles or a host dataset | ❌ Not implemented |
| Experience marketplace / catalog browsing | ❌ Not implemented |
| Booking flow (mock or real) | ❌ Not implemented |
| Payments | ❌ Not implemented |
| User accounts, login | ❌ Not implemented |
| Reviews | ❌ Not implemented |
| Admin tooling | ❌ Not implemented |

This is still an MVP, not a real marketplace. Everything in the ❌ rows above is future-phase direction, not a current or near-term claim.

## Related Documents

- [`README.md`](../../README.md) — project overview, setup, and architecture.
- [`docs/01_PRD.md`](../01_PRD.md) — Phase 1 MVP requirements and non-goals.
- [`docs/product/02_ARCHITECTURE.md`](02_ARCHITECTURE.md) — Phase 1 system architecture.
- [`docs/product/05_DEMO_SCRIPT.md`](05_DEMO_SCRIPT.md) — live demo walkthrough, including how to talk about this vision without overclaiming.
