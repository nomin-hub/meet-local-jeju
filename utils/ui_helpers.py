"""Streamlit UI rendering helpers for Meet Local Jeju.

Pure presentation helpers — custom card styling, the "Product Direction"
cards, the Pinterest-style "Featured Local Ideas" board, and the shared
sources renderer used by both app modes. Kept separate from `app.py` so the
two interaction modes (chat, recommendation) there stay easy to read.

No RAG logic lives here — this module only calls Streamlit rendering
functions (`st.*`) and holds static, developer-authored display data. The
"Featured Local Ideas" cards are prototype/portfolio content only: they do
not implement saving, booking, or any real backend action.
"""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
div[data-testid="stForm"] {
    background: #FFF8F1;
    border-radius: 18px;
    padding: 18px 22px 6px 22px;
    border: 1px solid #F1E1CE;
}
.ml-card {
    background: #FFF8F1;
    border: 1px solid #F1E1CE;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    height: 100%;
}
.ml-card-emoji {
    font-size: 26px;
    line-height: 1;
}
.ml-card-title {
    font-weight: 700;
    font-size: 15.5px;
    margin: 6px 0 4px 0;
    color: #3A2E26;
}
.ml-card-desc {
    font-size: 13px;
    color: #7A6F63;
    line-height: 1.4;
}
.ml-chip {
    display: inline-block;
    background: #FBE3CE;
    color: #A85A1F;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 999px;
    margin: 2px 0 8px 0;
}
.ml-save-badge {
    display: inline-block;
    margin-top: 10px;
    font-size: 11.5px;
    color: #9C8F81;
    border: 1px dashed #D9C8B4;
    border-radius: 999px;
    padding: 3px 10px;
}
.ml-kb-tag {
    display: block;
    margin-top: 6px;
    font-size: 10.5px;
    color: #B5A899;
}
</style>
"""

PRODUCT_DIRECTION_CARDS = [
    {
        "emoji": "🧭",
        "title": "Explore Local Experiences",
        "description": "Browse Pinterest-style local Jeju ideas grounded in JEJU-KB.",
    },
    {
        "emoji": "💬",
        "title": "Ask the AI Assistant",
        "description": "Ask grounded questions about Jeju culture, food, and seasonal life.",
    },
    {
        "emoji": "🗺️",
        "title": "Plan Future Jeju Trips",
        "description": "A prototype foundation for a future trip-planning experience.",
    },
]

FEATURED_IDEAS = [
    {
        "emoji": "🌊",
        "title": "Haenyeo Culture Walk",
        "category": "Culture",
        "description": "Walk the coast where Jeju's women divers still work, then visit a community museum.",
        "kb_id": "EXP-0002",
    },
    {
        "emoji": "🥬",
        "title": "Five-Day Market Visit",
        "category": "Experiences",
        "description": "Wander a rotating traditional market and meet the vendors who run it.",
        "kb_id": "EXP-0003",
    },
    {
        "emoji": "🍊",
        "title": "Tangerine Harvest",
        "category": "Experiences",
        "description": "Pick tangerines alongside a farming family during harvest season.",
        "kb_id": "EXP-0001",
    },
    {
        "emoji": "🪨",
        "title": "Jeju Stone Wall Village",
        "category": "Culture",
        "description": "See the black basalt batdam walls that shape Jeju's fields and villages.",
        "kb_id": "CULTURE-0001",
    },
    {
        "emoji": "🥟",
        "title": "Bingtteok Local Food",
        "category": "Food",
        "description": "Try Jeju's traditional buckwheat rice cake, a taste shaped by volcanic soil.",
        "kb_id": "FOOD-0001",
    },
    {
        "emoji": "🎣",
        "title": "Fishing Village Slow Walk",
        "category": "Local Life",
        "description": "Wander a coastal fishing village at the pace locals actually live it.",
        "kb_id": "LOCAL-0002",
    },
]


def inject_custom_css() -> None:
    """Inject the shared card/form styling once, near the top of the page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    """Render the title, subtitle, and one-sentence pitch."""
    st.title("Meet Local Jeju")
    st.subheader("Discover Jeju Beyond Tourism")
    st.write(
        "A RAG-powered local experience recommendation MVP for Jeju Island, "
        "designed to help international travelers discover local stories, "
        "food, culture, seasonal living, and authentic island experiences."
    )


def render_what_this_mvp_does(does: list[str], does_not: list[str]) -> None:
    """Render the two-column 'what this MVP does / does not do yet' summary."""
    what_col, not_col = st.columns(2)
    with what_col:
        st.markdown("**✅ What this MVP does**")
        st.markdown("\n".join(f"- {item}" for item in does))
    with not_col:
        st.markdown("**🚫 What this MVP does not do yet**")
        st.markdown("\n".join(f"- {item}" for item in does_not))


def render_product_direction() -> None:
    """Render the 3-card 'Product Direction' section."""
    st.markdown("#### Where This Is Headed")
    columns = st.columns(3)
    for column, card in zip(columns, PRODUCT_DIRECTION_CARDS):
        with column:
            st.markdown(
                f"""<div class="ml-card">
<div class="ml-card-emoji">{card['emoji']}</div>
<div class="ml-card-title">{card['title']}</div>
<div class="ml-card-desc">{card['description']}</div>
</div>""",
                unsafe_allow_html=True,
            )


def render_featured_ideas() -> None:
    """Render the Pinterest-style 'Featured Local Ideas' board.

    Static, developer-authored cards only — no external images, no save
    functionality, no booking. The "Save idea - prototype only" badge is
    intentionally non-interactive text, not a real action.
    """
    st.markdown("#### Featured Local Ideas")
    st.caption("A taste of what's in JEJU-KB — browse now, ask or get recommendations below for more.")

    idea_rows = [FEATURED_IDEAS[i : i + 3] for i in range(0, len(FEATURED_IDEAS), 3)]
    for row in idea_rows:
        columns = st.columns(3)
        for column, card in zip(columns, row):
            with column:
                st.markdown(
                    f"""<div class="ml-card">
<div class="ml-card-emoji">{card['emoji']}</div>
<span class="ml-chip">{card['category']}</span>
<div class="ml-card-title">{card['title']}</div>
<div class="ml-card-desc">{card['description']}</div>
<div class="ml-save-badge">💾 Save idea - prototype only</div>
<span class="ml-kb-tag">JEJU-KB: {card['kb_id']}</span>
</div>""",
                    unsafe_allow_html=True,
                )


def render_sources(sources: list[dict]) -> None:
    """Render a list of source dicts (id, title, category, chunk_id, file_path)."""
    if not sources:
        return
    st.caption("🔎 Sources show which JEJU-KB documents were used to ground this response.")
    with st.expander(f"Sources ({len(sources)})"):
        for source in sources:
            st.markdown(
                f"**{source.get('title')}** · `{source.get('id')}`\n\n"
                f"- Category: `{source.get('category')}`\n"
                f"- Chunk: `{source.get('chunk_id')}`\n"
                f"- File: `{source.get('file_path')}`"
            )
            st.divider()
