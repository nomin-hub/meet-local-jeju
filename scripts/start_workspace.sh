#!/usr/bin/env bash

# Start or attach to the Meet Local Jeju tmux workspace.
#
# Usage:
#   bash scripts/start_workspace.sh
#
# The script is intentionally safe:
# - It does not kill any tmux sessions.
# - If the meet-local-jeju session already exists, it attaches to it.
# - Every pane starts in the project root.

set -euo pipefail

SESSION_NAME="meet-local-jeju"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM="xterm-256color"
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is not installed or not on PATH."
  echo "Install tmux, then run: bash scripts/start_workspace.sh"
  exit 1
fi

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Attaching to existing tmux session: $SESSION_NAME"
  exec tmux attach-session -t "$SESSION_NAME"
fi

role_message() {
  local role="$1"
  local prompt_path="$2"
  cat <<EOF
clear
cd "$PROJECT_ROOT"
printf '\\n=== %s pane ===\\n' "$role"
printf 'Project: Meet Local Jeju / Jejumate\\n'
printf 'Prompt: %s\\n\\n' "$prompt_path"
printf 'Run: codex\\n'
printf 'Then type: Read AGENTS.md and %s. Follow all constraints. No commit.\\n\\n' "$prompt_path"
EOF
}

set_pane_title() {
  local target="$1"
  local title="$2"
  # select-pane -T is available in common modern tmux versions; if unsupported,
  # the role title is still printed inside the pane by role_message.
  tmux select-pane -t "$target" -T "$title" >/dev/null 2>&1 || true
}

tmux new-session -d -s "$SESSION_NAME" -n "AI Workspace" -c "$PROJECT_ROOT"
set_pane_title "$SESSION_NAME":0.0 "PM"
tmux send-keys -t "$SESSION_NAME":0.0 "$(role_message "PM" "workspace/prompts/pm.md")" C-m

tmux split-window -h -t "$SESSION_NAME":0.0 -c "$PROJECT_ROOT"
set_pane_title "$SESSION_NAME":0.1 "Designer"
tmux send-keys -t "$SESSION_NAME":0.1 "$(role_message "Designer" "workspace/prompts/designer.md")" C-m

tmux split-window -v -t "$SESSION_NAME":0.0 -c "$PROJECT_ROOT"
set_pane_title "$SESSION_NAME":0.2 "Developer"
tmux send-keys -t "$SESSION_NAME":0.2 "$(role_message "Developer" "workspace/prompts/developer.md")" C-m

tmux split-window -v -t "$SESSION_NAME":0.1 -c "$PROJECT_ROOT"
set_pane_title "$SESSION_NAME":0.3 "QA"
tmux send-keys -t "$SESSION_NAME":0.3 "$(role_message "QA" "workspace/prompts/qa.md")" C-m

tmux split-window -v -t "$SESSION_NAME":0.3 -c "$PROJECT_ROOT"
set_pane_title "$SESSION_NAME":0.4 "Server / Git"
tmux send-keys -t "$SESSION_NAME":0.4 "clear" C-m
tmux send-keys -t "$SESSION_NAME":0.4 "cd \"$PROJECT_ROOT\"" C-m
tmux send-keys -t "$SESSION_NAME":0.4 "printf '\\n=== Server / Git pane ===\\nProject: Meet Local Jeju / Jejumate\\n\\nUseful commands:\\n  streamlit run app.py\\n  git status\\n  python3 utils/experience_loader.py\\n  python3 -m py_compile app.py utils/ui_helpers.py utils/experience_loader.py\\n\\nCommit manually only after review.\\n\\n'" C-m

tmux select-layout -t "$SESSION_NAME":0 tiled
tmux select-pane -t "$SESSION_NAME":0.0

echo "Created tmux session: $SESSION_NAME"
echo "Tip: run 'codex' in PM, Designer, Developer, and QA panes."
exec tmux attach-session -t "$SESSION_NAME"
