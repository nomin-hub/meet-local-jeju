"""Meet Local Jeju — Streamlit chat UI.

A conversational front end for the JEJU-KB RAG assistant (see `rag/chain.py`).
This module only renders the UI and calls `answer_question()`; it never builds
or rebuilds the vector store — that is a separate offline step
(`python3 rag/vectordb.py`).
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag.chain import answer_question

load_dotenv()

VECTOR_STORE_DIR = Path(__file__).resolve().parent / "vector_db" / "chroma"

EXAMPLE_QUESTIONS = [
    "I want to learn about haenyeo culture.",
    "What can I do in Jeju in October?",
    "I want to meet local people at a traditional market.",
    "Tell me about Jeju stone walls.",
]

st.set_page_config(page_title="Meet Local Jeju", page_icon="🍊", layout="centered")


def render_sources(sources: list[dict]) -> None:
    """Render a list of source dicts (id, title, category, chunk_id, file_path)."""
    if not sources:
        return
    with st.expander(f"Sources ({len(sources)})"):
        for source in sources:
            st.markdown(
                f"**{source.get('title')}** · `{source.get('id')}`\n\n"
                f"- Category: `{source.get('category')}`\n"
                f"- Chunk: `{source.get('chunk_id')}`\n"
                f"- File: `{source.get('file_path')}`"
            )
            st.divider()


# --- Sidebar: example questions ---
with st.sidebar:
    st.header("Try an example")
    for question in EXAMPLE_QUESTIONS:
        if st.button(question, use_container_width=True, key=f"example::{question}"):
            st.session_state["pending_question"] = question

    st.divider()
    st.caption(
        "Answers are grounded in JEJU-KB, a curated knowledge base of authentic "
        "Jeju culture, seasonal living, food, festivals, and local stories — not "
        "general AI knowledge."
    )

# --- Header ---
st.title("Meet Local Jeju")
st.subheader("Discover Jeju Beyond Tourism")
st.write(
    "Meet Local Jeju is an AI assistant for travelers who want more than a "
    "checklist of attractions. Ask about Jeju's local culture, seasonal life, "
    "food, festivals, and stories, and get answers grounded in a curated "
    "knowledge base of authentic local experiences."
)

if not VECTOR_STORE_DIR.exists():
    st.warning(
        "The JEJU-KB vector store hasn't been built yet, so questions will fail. "
        "Run `python3 rag/vectordb.py` once from the project root to build it, "
        "then reload this page."
    )

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_sources(message.get("sources"))

# --- Question input: chat box or a clicked sidebar example ---
question = st.chat_input("Ask about local life, culture, food, or festivals in Jeju...")
if not question and "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question is not None:
    question = question.strip()

    if not question:
        st.warning("Please enter a question.")
    else:
        st.session_state["messages"].append({"role": "user", "content": question, "sources": None})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching JEJU-KB..."):
                try:
                    result = answer_question(question)
                except RuntimeError as exc:
                    # Raised by rag.chain / rag.vectordb when OPENAI_API_KEY is missing.
                    answer_text = (
                        "**Configuration error:** the OpenAI API key is not set. "
                        f"Add `OPENAI_API_KEY` to your `.env` file and reload this page.\n\n_{exc}_"
                    )
                    st.error(answer_text)
                    sources = None
                except FileNotFoundError as exc:
                    # Raised by rag.vectordb.load_vector_store when the store doesn't exist.
                    answer_text = (
                        "**The JEJU-KB vector store hasn't been built yet.** "
                        f"Run `python3 rag/vectordb.py` from the project root first.\n\n_{exc}_"
                    )
                    st.error(answer_text)
                    sources = None
                except Exception as exc:  # noqa: BLE001 - surface any other API/runtime error to the user
                    answer_text = f"**Something went wrong while answering:** {exc}"
                    st.error(answer_text)
                    sources = None
                else:
                    answer_text = result["answer"]
                    sources = result["sources"]
                    st.markdown(answer_text)
                    render_sources(sources)

        st.session_state["messages"].append(
            {"role": "assistant", "content": answer_text, "sources": sources}
        )
