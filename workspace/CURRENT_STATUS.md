# Current Status

## Product State

- Streamlit mobile-style prototype exists.
- Home screen shows local experience cards from `data/experiences/`.
- AI Assistant includes RAG chat and recommendation mode.
- My Page is a mock saved ideas screen.
- RAG pipeline is a central project asset and must be preserved.

## Prototype Honesty

The app must continue to state or imply clearly:

- No real booking
- No real payment
- No login
- Save feature is mock only
- Booking is not available in MVP

## Standard Local Checks

```bash
python3 utils/experience_loader.py
python3 -m py_compile app.py utils/ui_helpers.py utils/experience_loader.py
streamlit run app.py
git status --short
```

## Coordination Notes

- Use `workspace/TASK_BOARD.md` for planned work.
- Use `workspace/REVIEW_CHECKLIST.md` for QA passes.
- Do not commit automatically.
- Report changed files and test results at the end of every task.
