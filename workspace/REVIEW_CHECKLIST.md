# Review Checklist

## Scope

- Confirm requested files were changed only.
- Confirm protected RAG files were not modified unless explicitly requested.
- Confirm no real booking, payment, login, save persistence, host onboarding, or marketplace operation was added.
- Confirm no secrets or `.env` values were exposed.

## UI Checks

- Home screen renders in mobile-style frame.
- 2-column Pinterest-style cards load from `data/experiences/`.
- AI Assistant screen is readable.
- Chat mode remains grounded in JEJU-KB.
- Recommendation mode remains available.
- My Page is clearly mock-only.
- Prototype honesty copy remains visible.

## Commands

Run relevant checks:

```bash
python3 utils/experience_loader.py
python3 -m py_compile app.py utils/ui_helpers.py utils/experience_loader.py
streamlit run app.py
git status --short
```

## RAG Behavior Checks

When vector store and API key are available, test:

- `I want to learn about haenyeo culture.`
- `What can I do in Jeju in October?`
- `I want to meet local people at a traditional market.`
- `Tell me about Jeju stone walls.`

Confirm source attribution is shown.

## Required QA Report

- Changed files reviewed
- Commands run
- Pass/fail result
- Bugs or risks
- Remaining TODOs
- Safe to commit: yes/no
