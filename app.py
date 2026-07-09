"""Meet Local Jeju — Streamlit UI.

Two modes, both grounded in JEJU-KB:
  - "Ask Local Jeju AI": conversational Q&A (see `rag/chain.py`).
  - "Get Experience Recommendations": preference-based recommendations
    (see `rag/recommender.py`).

This module only renders the UI and calls into `rag/`; it never builds or
rebuilds the vector store — that is a separate offline step
(`python3 rag/vectordb.py`). Recommendation mode is a recommendation feature
only — it does not implement or imply booking, payment, host onboarding, or
marketplace functionality.
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag.chain import answer_question
from rag.recommender import TravelerPreferences, get_experience_recommendations

load_dotenv()

VECTOR_STORE_DIR = Path(__file__).resolve().parent / "vector_db" / "chroma"

EXAMPLE_QUESTIONS = [
    "I want to learn about haenyeo culture.",
    "What can I do in Jeju in October?",
    "I want to meet local people at a traditional market.",
    "Tell me about Jeju stone walls.",
]

MODE_CHAT = "Ask Local Jeju AI"
MODE_RECOMMEND = "Get Experience Recommendations"

INTEREST_OPTIONS = [
    "food",
    "culture",
    "nature",
    "local people",
    "farming",
    "ocean",
    "markets",
    "slow travel",
]
TRAVEL_STYLE_OPTIONS = [
    "relaxing",
    "active",
    "cultural",
    "family-friendly",
    "solo traveler",
    "budget-friendly",
]
TRANSPORTATION_OPTIONS = ["No preference", "car", "no car", "public transportation", "taxi", "walking"]

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


def render_backend_error(exc: Exception, generic_context: str = "while answering") -> str:
    """Return a user-facing error message for known backend failure modes.

    Shared between chat mode and recommendation mode, since both call into the
    same JEJU-KB retrieval/generation stack and can fail the same ways.

    Args:
        exc: The raised exception.
        generic_context: Short phrase describing what was being done, used only
            in the fallback message for exception types other than the two
            specifically handled below (e.g. "while answering" vs.
            "while generating recommendations").
    """
    if isinstance(exc, RuntimeError):
        # Raised by rag.chain / rag.recommender / rag.vectordb when OPENAI_API_KEY is missing.
        return (
            "**Configuration error:** the OpenAI API key is not set. "
            f"Add `OPENAI_API_KEY` to your `.env` file and reload this page.\n\n_{exc}_"
        )
    if isinstance(exc, FileNotFoundError):
        # Raised by rag.vectordb.load_vector_store when the store doesn't exist.
        return (
            "**The JEJU-KB vector store hasn't been built yet.** "
            f"Run `python3 rag/vectordb.py` from the project root first.\n\n_{exc}_"
        )
    return f"**Something went wrong {generic_context}:** {exc}"


# --- Sidebar: mode selector ---
with st.sidebar:
    st.header("Mode")
    mode = st.radio("Choose a mode", [MODE_CHAT, MODE_RECOMMEND], key="mode")
    st.divider()

    if mode == MODE_CHAT:
        st.header("Try an example")
        for question in EXAMPLE_QUESTIONS:
            if st.button(question, use_container_width=True, key=f"example::{question}"):
                st.session_state["pending_question"] = question
    else:
        st.caption(
            "Fill out the form to get authentic local experience recommendations "
            "grounded in JEJU-KB — this is a recommendation feature, not a "
            "booking system."
        )

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
    "food, festivals, and stories — or get preference-based experience "
    "recommendations — grounded in a curated knowledge base of authentic "
    "local experiences."
)

if not VECTOR_STORE_DIR.exists():
    st.warning(
        "The JEJU-KB vector store hasn't been built yet, so questions and "
        "recommendations will fail. Run `python3 rag/vectordb.py` once from "
        "the project root to build it, then reload this page."
    )

if mode == MODE_CHAT:
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
                    except Exception as exc:  # noqa: BLE001 - surface any backend error to the user
                        answer_text = render_backend_error(exc)
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

else:  # mode == MODE_RECOMMEND
    st.markdown("### Get Experience Recommendations")
    st.caption(
        "This is a recommendation feature only — not a booking or marketplace "
        "feature. Nothing shown here can be reserved or paid for."
    )

    if "last_recommendation" not in st.session_state:
        st.session_state["last_recommendation"] = None

    with st.form("recommendation_form"):
        interests = st.multiselect("Travel interests", INTEREST_OPTIONS)
        travel_style = st.multiselect("Travel style", TRAVEL_STYLE_OPTIONS)
        season_or_month = st.text_input("Season or month (optional)", placeholder="e.g. October, winter")
        transportation = st.selectbox("Transportation", TRANSPORTATION_OPTIONS)
        preferred_area = st.text_input("Preferred area (optional)", placeholder="e.g. Seogwipo, Jeju-si")
        additional_notes = st.text_area("Question or additional preference (optional)")

        submitted = st.form_submit_button("Get Recommendations")

    if submitted:
        preferences = TravelerPreferences(
            interests=interests,
            travel_style=travel_style,
            season_or_month=season_or_month.strip() or None,
            transportation=None if transportation == "No preference" else transportation,
            preferred_area=preferred_area.strip() or None,
            additional_notes=additional_notes.strip() or None,
        )

        if preferences.is_empty():
            st.warning(
                "Please select at least one interest or travel style, or add a "
                "note, before submitting."
            )
        else:
            with st.spinner("Finding grounded recommendations from JEJU-KB..."):
                try:
                    result = get_experience_recommendations(preferences)
                except Exception as exc:  # noqa: BLE001 - surface any backend error to the user
                    st.error(render_backend_error(exc, generic_context="while generating recommendations"))
                else:
                    st.session_state["last_recommendation"] = {
                        "text": result["recommendation"],
                        "sources": result["sources"],
                    }

    if st.session_state["last_recommendation"] is not None:
        st.divider()
        st.markdown(st.session_state["last_recommendation"]["text"])
        render_sources(st.session_state["last_recommendation"]["sources"])
