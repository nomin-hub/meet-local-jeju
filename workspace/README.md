# Meet Local Jeju AI Workspace

This folder supports a tmux-based ChatGPT + Codex workflow for coordinating several Codex sessions visually, like a small AI product team.

## Start

From the repository root:

```bash
bash scripts/start_workspace.sh
```

The script creates or attaches to a tmux session named `meet-local-jeju`.

## Suggested Workflow

1. Start workspace:
   ```bash
   bash scripts/start_workspace.sh
   ```
2. PM pane:
   Ask Codex to read `AGENTS.md` and `workspace/TASK_BOARD.md`.
3. Designer pane:
   Ask for UI improvements using `workspace/prompts/designer.md`.
4. Developer pane:
   Ask for feature implementation using `workspace/prompts/developer.md`.
5. QA pane:
   Ask for review using `workspace/REVIEW_CHECKLIST.md`.
6. Server / Git pane:
   Run the app, check Git state, and commit manually only after ChatGPT review.

## Short Commands Ari Can Type

```text
Next task. Follow AGENTS.md. No commit.
```

```text
QA current changes using workspace/REVIEW_CHECKLIST.md. Do not edit files.
```

```text
Improve only the UI. Follow workspace/prompts/designer.md. Do not touch RAG files.
```

```text
Prepare a commit summary. Do not commit.
```

## Pane Roles

- PM: task breakdown, task board updates, scope control
- Designer: mobile Pinterest-style UI quality
- Developer: product implementation within allowed files
- QA: tests, behavior checks, regression review
- Server / Git: run Streamlit, run checks, inspect Git state

## Commit Policy

Codex should not commit automatically. Ari reviews changes first, then commits manually.
