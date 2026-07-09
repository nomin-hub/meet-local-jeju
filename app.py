"""Meet Local Jeju — Streamlit UI.

Two modes, both grounded in JEJU-KB:
  - "Ask Local Jeju AI": conversational Q&A (see `rag/chain.py`).
  - "Get Experience Recommendations": preference-based recommendations
    (see `rag/recommender.py`).

The visual direction is a Pinterest-style local discovery board (browse
"Featured Local Ideas") layered on top of the same two functional modes —
still a Streamlit portfolio MVP, not a production mobile app.

This module only renders the UI and calls into `rag/`; it never builds or
rebuilds the vector store — that is a separate offline step
(`python3 rag/vectordb.py`). This is a portfolio MVP: recommendation mode and
the "Featured Local Ideas" board are prototype/discovery features only — they
do not implement or imply booking, payment, host onboarding, real-time
availability, or marketplace functionality.
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag.chain import answer_question
from rag.recommender import TravelerPreferences, get_experience_recommendations
from utils.ui_helpers import (
    inject_custom_css,
    render_featured_ideas,
    render_hero,
    render_product_direction,
    render_sources,
    render_what_this_mvp_does,
)

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
MODE_CAPTIONS = [
    "Ask a free-form question about Jeju local life.",
    "Answer a short preference form for tailored suggestions.",
]

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

WHAT_IT_DOES = [
    "Ask questions about Jeju local life",
    "Get personalized local experience recommendations",
    "Explore experiences grounded in JEJU-KB sources",
    "Prototype foundation for a future trip-planning and local experience platform",
]
WHAT_IT_DOES_NOT_DO = [
    "No booking",
    "No payment",
    "No real host onboarding",
    "No real-time availability",
    "No commercial travel product sales",
]

st.set_page_config(page_title="Meet Local Jeju", page_icon="🍊", layout="wide")


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


inject_custom_css()

# --- Sidebar ---
with st.sidebar:
    st.header("Meet Local Jeju")
    st.caption("Find local Jeju experiences, ask grounded AI questions, and build future trip ideas.")
    st.divider()

    mode = st.radio("Choose a mode", [MODE_CHAT, MODE_RECOMMEND], captions=MODE_CAPTIONS, key="mode")
    st.divider()

    if mode == MODE_CHAT:
        st.caption(
            "You're in **Ask Local Jeju AI** mode — type your own question below, "
            "or click an example to get started."
        )
        st.header("Try an example")
        for question in EXAMPLE_QUESTIONS:
            if st.button(question, use_container_width=True, key=f"example::{question}"):
                st.session_state["pending_question"] = question
    else:
        st.caption(
            "You're in **Get Experience Recommendations** mode — answer a few "
            "quick questions and get grounded local experience ideas. This is "
            "a prototype recommendation feature, not a booking system."
        )

    st.divider()
    st.caption(
        "Answers are grounded in JEJU-KB, a curated knowledge base of authentic "
        "Jeju culture, seasonal living, food, festivals, and local stories — not "
        "general AI knowledge."
    )

# --- Hero ---
render_hero()

col1, col2 = st.columns([3, 2], gap="large")
with col1:
    render_product_direction()
with col2:
    render_what_this_mvp_does(WHAT_IT_DOES, WHAT_IT_DOES_NOT_DO)

st.divider()
render_featured_ideas()
st.divider()

if not VECTOR_STORE_DIR.exists():
    st.warning(
        "The JEJU-KB vector store hasn't been built yet, so questions and "
        "recommendations will fail. Run `python3 rag/vectordb.py` once from "
        "the project root to build it, then reload this page."
    )

if mode == MODE_CHAT:
    st.caption("Answers are grounded in JEJU-KB, the project's structured local knowledge base.")

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
    st.markdown("### Your Travel Preference Card")
    st.caption(
        "Share your interests and travel style, and we'll recommend authentic "
        "local experiences grounded in JEJU-KB — generated from structured "
        "local knowledge, not a generic travel search."
    )
    st.info("💡 This is a prototype recommendation feature, not a booking system.")

    if "last_recommendation" not in st.session_state:
        st.session_state["last_recommendation"] = None

    with st.form("recommendation_form"):
        interests = st.multiselect("What are you interested in?", INTEREST_OPTIONS)
        travel_style = st.multiselect("What is your travel style?", TRAVEL_STYLE_OPTIONS)
        season_or_month = st.text_input("When are you visiting? (optional)", placeholder="e.g. October, winter")
        transportation = st.selectbox("How will you move around Jeju?", TRANSPORTATION_OPTIONS)
        preferred_area = st.text_input(
            "Any specific area of Jeju in mind? (optional)", placeholder="e.g. Seogwipo, Jeju-si"
        )
        additional_notes = st.text_area("Any extra preferences? (optional)")

        submitted = st.form_submit_button("Get My Recommendations")

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
        st.caption(
            "✨ Generated from structured local knowledge in JEJU-KB — not a "
            "generic travel search."
        )
        st.markdown(st.session_state["last_recommendation"]["text"])
        render_sources(st.session_state["last_recommendation"]["sources"])
