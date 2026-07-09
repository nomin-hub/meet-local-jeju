"""Meet Local Jeju — Streamlit UI (mobile app prototype).

A Streamlit-based mobile *prototype*, not a production native app: the phone
frame, header, cards, and bottom tab bar below are achieved entirely with
custom CSS constraining Streamlit's own layout (see `utils/ui_helpers.py`).

Three screens, navigated via the bottom tab bar:
  - Home: a Pinterest-style, image-first grid of local experience ideas,
    loaded from `data/experiences/` (see `utils/experience_loader.py`).
  - AI Assistant: the two functional RAG modes — "Ask a question" (see
    `rag/chain.py`) and "Get recommendations" (see `rag/recommender.py`).
  - My Page: a mock "saved ideas" screen. No login, no real saving.

This module only renders the UI and calls into `rag/`; it never builds or
rebuilds the vector store — that is a separate offline step
(`python3 rag/vectordb.py`). Nothing in this app implements or implies real
booking, payment, login, host onboarding, or marketplace functionality.
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag.chain import answer_question
from rag.recommender import TravelerPreferences, get_experience_recommendations
from utils.experience_loader import ExperienceCardError, load_experience_cards
from utils.ui_helpers import (
    inject_mobile_css,
    render_experience_grid,
    render_home_screen,
    render_honesty_badges,
    render_my_page_header,
    render_screen_title,
    render_sources,
)

load_dotenv()

VECTOR_STORE_DIR = Path(__file__).resolve().parent / "vector_db" / "chroma"

EXAMPLE_QUESTIONS = [
    "I want to learn about haenyeo culture.",
    "What can I do in Jeju in October?",
    "I want to meet local people at a traditional market.",
    "Tell me about Jeju stone walls.",
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

SCREEN_HOME = "🏠 Home"
SCREEN_ASSISTANT = "💬 AI Assistant"
SCREEN_MY_PAGE = "👤 My Page"
NAV_SCREENS = [SCREEN_HOME, SCREEN_ASSISTANT, SCREEN_MY_PAGE]

ASSISTANT_MODE_ASK = "Ask a question"
ASSISTANT_MODE_RECOMMEND = "Get recommendations"

st.set_page_config(
    page_title="Meet Local Jeju",
    page_icon="🍊",
    layout="centered",
    initial_sidebar_state="collapsed",
)


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


inject_mobile_css()

# Read the current screen/tab from session_state *before* rendering the
# bottom nav widget further down — Streamlit updates session_state as soon
# as a widget changes, before the script reruns, so this reflects the tap
# that just happened even though the nav bar itself renders later (it's
# pinned to the bottom of the phone frame via CSS, not via render order).
screen = st.session_state.get("nav_radio", SCREEN_HOME)

# ---------------------------------------------------------------------------
# Home screen
# ---------------------------------------------------------------------------
if screen == SCREEN_HOME:
    render_home_screen()

# ---------------------------------------------------------------------------
# AI Assistant screen
# ---------------------------------------------------------------------------
elif screen == SCREEN_ASSISTANT:
    render_screen_title("AI Assistant", "Ask for local recommendations grounded in JEJU-KB.")
    render_honesty_badges(["Grounded in JEJU-KB", "No booking or payment"])

    if not VECTOR_STORE_DIR.exists():
        st.warning(
            "The JEJU-KB vector store hasn't been built yet, so questions and "
            "recommendations will fail. Run `python3 rag/vectordb.py` once "
            "from the project root to build it, then reload this page."
        )

    assistant_mode = st.radio(
        "Assistant mode",
        [ASSISTANT_MODE_ASK, ASSISTANT_MODE_RECOMMEND],
        horizontal=True,
        label_visibility="collapsed",
        key="assistant_submode",
    )

    if assistant_mode == ASSISTANT_MODE_ASK:
        with st.expander("Try an example"):
            for question in EXAMPLE_QUESTIONS:
                if st.button(question, use_container_width=True, key=f"example::{question}"):
                    st.session_state["pending_question"] = question

        # --- Chat history ---
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                render_sources(message.get("sources"))

        # --- Question input: chat box or a clicked example ---
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

    else:  # ASSISTANT_MODE_RECOMMEND
        st.markdown("**Your Travel Preference Card**")
        st.caption(
            "Share your interests and travel style, and we'll recommend "
            "authentic local experiences grounded in JEJU-KB."
        )
        st.info("💡 This is a prototype recommendation feature, not a booking system.")

        if "last_recommendation" not in st.session_state:
            st.session_state["last_recommendation"] = None

        with st.form("recommendation_form"):
            interests = st.multiselect("What are you interested in?", INTEREST_OPTIONS)
            travel_style = st.multiselect("What is your travel style?", TRAVEL_STYLE_OPTIONS)
            season_or_month = st.text_input(
                "When are you visiting? (optional)", placeholder="e.g. October, winter"
            )
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
                    "Please select at least one interest or travel style, or "
                    "add a note, before submitting."
                )
            else:
                with st.spinner("Finding grounded recommendations from JEJU-KB..."):
                    try:
                        result = get_experience_recommendations(preferences)
                    except Exception as exc:  # noqa: BLE001 - surface any backend error to the user
                        st.error(
                            render_backend_error(exc, generic_context="while generating recommendations")
                        )
                    else:
                        st.session_state["last_recommendation"] = {
                            "text": result["recommendation"],
                            "sources": result["sources"],
                        }

        if st.session_state["last_recommendation"] is not None:
            st.divider()
            st.caption(
                "✨ Generated from structured local knowledge in JEJU-KB — not "
                "a generic travel search."
            )
            st.markdown(st.session_state["last_recommendation"]["text"])
            render_sources(st.session_state["last_recommendation"]["sources"])

# ---------------------------------------------------------------------------
# My Page screen (mock)
# ---------------------------------------------------------------------------
else:  # screen == SCREEN_MY_PAGE
    render_my_page_header()

    tab = st.radio(
        "My Page tabs",
        ["📌 Pins", "🗂️ Boards", "🧳 Trips"],
        horizontal=True,
        label_visibility="collapsed",
        key="mypage_tab",
    )

    if tab == "📌 Pins":
        st.caption("Ideas you've \"saved\" — prototype only, nothing is actually persisted yet.")
        try:
            cards = load_experience_cards()
        except ExperienceCardError as exc:
            st.error(f"Could not load the experience card dataset: {exc}")
        else:
            render_experience_grid(cards[:4])
    else:
        st.info(f"{tab} is coming soon — prototype only. No login or real saving in this MVP.")

# ---------------------------------------------------------------------------
# Bottom tab navigation — rendered last in the script, but pinned to the
# bottom of the phone frame via CSS (see .st-key-bottom_nav), not by order.
# ---------------------------------------------------------------------------
with st.container(key="bottom_nav"):
    st.radio(
        "Navigate",
        NAV_SCREENS,
        horizontal=True,
        label_visibility="collapsed",
        key="nav_radio",
    )
