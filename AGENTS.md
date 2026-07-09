# Meet Local Jeju / Jejumate Agent Instructions

## Project Identity

- Project name: Meet Local Jeju / Jejumate
- Product type: RAG-powered mobile-style local experience discovery MVP for Jeju
- Core promise: help travelers discover Jeju beyond tourism through local culture, food, villages, nature, and stories grounded in JEJU-KB.
- Long-term vision: evolve into a trip planner and Airbnb-like local experience platform for authentic Jeju local experiences, people, stories, and potentially stays.

## Operating Principles

- Preserve the working RAG pipeline.
- Do not replace real RAG behavior with mock logic.
- Do not simplify the app into a fake demo.
- Keep the prototype honest: no real booking, payment, login, save, host onboarding, or marketplace operations.
- Do not claim unbuilt marketplace features exist.
- Do not commit automatically. The project owner commits manually after review.
- Prefer small, reviewable changes.
- Inspect existing files before editing.
- Never expose secrets or `.env` values.

## Protected RAG Files

Do not modify these files unless explicitly requested:

- `rag/loader.py`
- `rag/splitter.py`
- `rag/vectordb.py`
- `rag/retriever.py`
- `rag/chain.py`

If a task appears to require changes to these files, stop and ask for explicit confirmation.

## Product Boundaries

Do not implement or imply:

- Real booking
- Real payment
- Real login or account system
- Real save persistence
- Real host onboarding
- Real marketplace operations
- Real host names, phone numbers, prices, exact schedules, or availability

Prototype-only UI is allowed when clearly labeled as mock or MVP-only.

## Common Verification Commands

Use the relevant commands for the task:

```bash
python3 utils/experience_loader.py
python3 -m py_compile app.py utils/ui_helpers.py utils/experience_loader.py
streamlit run app.py
git status --short
```

For RAG behavior checks, confirm the vector store exists and use known demo prompts when an API key is available.

## Required Final Report

Every agent must report:

- Changed files
- Tests or checks run
- Result
- Remaining TODOs or risks
- Whether it is safe to commit

If no files were changed, say so explicitly.
