"""Streamlit UI rendering helpers for Meet Local Jeju.

Pure presentation helpers for the mobile app-style prototype UI: the phone
frame, headers, the Pinterest-style image-first card grid, chat-bubble/source
styling, and the "My Page" avatar block. Kept separate from `app.py` so the
three screens (Home, AI Assistant, My Page) there stay easy to read.

No RAG logic lives here — this module only calls Streamlit rendering
functions (`st.*`). "Featured Local Ideas" / "Pins" card *content* is loaded
from the structured dataset in `data/experiences/` via
`utils.experience_loader`, not hardcoded — this module only renders it.
Those cards are prototype/portfolio content only: they do not implement
saving, booking, or any real backend action.

This is a Streamlit-based mobile *prototype*, not a production native app —
the "phone frame" below is achieved entirely with CSS constraining
Streamlit's own layout, not a native mobile framework.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow this module to be imported (or, in principle, run directly) without
# the project root already being on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from utils.experience_loader import ExperienceCardError, load_experience_cards

MOBILE_CSS = """
<style>
/* ---------- Phone frame ---------- */
[data-testid="stAppViewContainer"] {
    background: #EFE6DA;
}
[data-testid="stMainBlockContainer"] {
    max-width: 430px !important;
    margin: 20px auto 0 auto !important;
    background: #FFFBF6;
    border-radius: 32px;
    box-shadow: 0 10px 40px rgba(60, 40, 20, 0.15);
    padding: 20px 18px 112px 18px !important;
    border: 1px solid #F1E1CE;
}
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}
/* Force the 2-column card grid to stay side-by-side inside the narrow phone
   frame — Streamlit's own responsive breakpoint otherwise stacks columns to
   min-width: calc(100% - 24px) below ~640px, which fights this design. */
[data-testid="stColumn"] {
    min-width: 0 !important;
}

/* ---------- Headers ---------- */
.ml-app-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}
.ml-app-header-emoji {
    font-size: 24px;
}
.ml-app-header-title {
    font-weight: 800;
    font-size: 20px;
    color: #3A2E26;
}
.ml-app-header-subtitle,
.ml-screen-subtitle {
    font-size: 12.5px;
    color: #9C8F81;
    margin: 0 0 10px 0;
}
.ml-screen-title {
    font-weight: 800;
    font-size: 19px;
    color: #3A2E26;
    margin: 2px 0 2px 0;
}

/* ---------- Honesty badges ---------- */
.ml-honesty-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 2px 0 14px 0;
}
.ml-honesty-badge {
    font-size: 10px;
    color: #A56A5A;
    background: #FBEAE5;
    border-radius: 999px;
    padding: 3px 9px;
    white-space: nowrap;
}

/* ---------- Pinterest image-first card ---------- */
.ml-pin-card {
    background: #FFFFFF;
    border: 1px solid #F1E1CE;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(60, 40, 20, 0.06);
}
.ml-pin-image {
    height: 92px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
}
.ml-pin-body {
    padding: 10px 12px 12px 12px;
}
.ml-pin-chip {
    display: inline-block;
    background: #FBE3CE;
    color: #A85A1F;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 999px;
    margin-bottom: 6px;
}
.ml-pin-title {
    font-weight: 700;
    font-size: 13.5px;
    color: #3A2E26;
    margin: 0 0 3px 0;
    line-height: 1.25;
}
.ml-pin-desc {
    font-size: 11.5px;
    color: #7A6F63;
    line-height: 1.35;
    margin-bottom: 6px;
}
.ml-pin-area {
    font-size: 10.5px;
    color: #9C8F81;
    margin-bottom: 7px;
}
.ml-pin-save {
    font-size: 10px;
    color: #9C8F81;
    border: 1px dashed #D9C8B4;
    border-radius: 999px;
    padding: 2px 8px;
    display: inline-block;
}

/* image-style gradient placeholders, cycled per card */
.ml-grad-0 { background: linear-gradient(135deg, #FBD9B4, #F4A261); }
.ml-grad-1 { background: linear-gradient(135deg, #CDEAE3, #7FC8B8); }
.ml-grad-2 { background: linear-gradient(135deg, #FFE3C2, #FDBB6D); }
.ml-grad-3 { background: linear-gradient(135deg, #E6DED3, #B9A791); }
.ml-grad-4 { background: linear-gradient(135deg, #FADCE0, #EDA0A8); }
.ml-grad-5 { background: linear-gradient(135deg, #CFE7F2, #85B7D1); }

/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 6px 8px !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #FDECD8;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #F4F1EC;
}

/* ---------- Source chips ---------- */
.ml-source-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 6px 0;
}
.ml-source-chip {
    font-size: 10.5px;
    background: #F4EDE4;
    color: #6B5B4B;
    border-radius: 999px;
    padding: 3px 9px;
}

/* ---------- My Page avatar ---------- */
.ml-avatar-circle {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: #F4A261;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
}

/* ---------- Bottom tab navigation ---------- */
.st-key-bottom_nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    background: #FFFBF6;
    border-top: 1px solid #F1E1CE;
    border-radius: 20px 20px 32px 32px;
    padding: 8px 16px 16px 16px;
    z-index: 9999;
    box-shadow: 0 -6px 20px rgba(60, 40, 20, 0.10);
}
.st-key-bottom_nav div[role="radiogroup"] {
    display: flex;
    justify-content: space-around;
}
</style>
"""

GRADIENT_CLASSES = ["ml-grad-0", "ml-grad-1", "ml-grad-2", "ml-grad-3", "ml-grad-4", "ml-grad-5"]


def inject_mobile_css() -> None:
    """Inject the phone-frame / card / chat-bubble / bottom-nav CSS once."""
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)


def render_app_header() -> None:
    """Render the Home screen's brand header (title + tagline)."""
    st.markdown(
        """<div class="ml-app-header">
<span class="ml-app-header-emoji">🍊</span>
<span class="ml-app-header-title">Meet Local Jeju</span>
</div>
<div class="ml-app-header-subtitle">Local experiences for your Jeju trip</div>""",
        unsafe_allow_html=True,
    )


def render_screen_title(title: str, subtitle: str) -> None:
    """Render a screen-specific title + subtitle (AI Assistant, My Page)."""
    st.markdown(
        f'<div class="ml-screen-title">{title}</div>'
        f'<div class="ml-screen-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def render_honesty_badges(labels: list[str]) -> None:
    """Render a row of small honesty labels, e.g. 'Prototype only'."""
    chips = "".join(f'<span class="ml-honesty-badge">{label}</span>' for label in labels)
    st.markdown(f'<div class="ml-honesty-row">{chips}</div>', unsafe_allow_html=True)


def _render_pin_card(card: dict, index: int) -> None:
    """Render a single image-first Pinterest-style card."""
    gradient_class = GRADIENT_CLASSES[index % len(GRADIENT_CLASSES)]
    best_for = card.get("best_for", [])
    best_for_text = f" · {', '.join(best_for[:2])}" if best_for else ""
    st.markdown(
        f"""<div class="ml-pin-card">
<div class="ml-pin-image {gradient_class}">{card.get('emoji', '📍')}</div>
<div class="ml-pin-body">
<span class="ml-pin-chip">{card['category']}</span>
<div class="ml-pin-title">{card['title']}</div>
<div class="ml-pin-desc">{card['description']}</div>
<div class="ml-pin-area">📍 {card['area']}{best_for_text}</div>
<span class="ml-pin-save">🔖 Save idea - prototype only</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_experience_grid(cards: list[dict]) -> None:
    """Render a 2-column Pinterest-style masonry grid of experience cards."""
    for i in range(0, len(cards), 2):
        left, right = st.columns(2)
        with left:
            _render_pin_card(cards[i], i)
        if i + 1 < len(cards):
            with right:
                _render_pin_card(cards[i + 1], i + 1)


def render_home_screen() -> None:
    """Render the full Home screen: header, honesty badges, card grid."""
    render_app_header()
    render_honesty_badges(["Prototype only", "Booking not available in MVP"])

    try:
        cards = load_experience_cards()
    except ExperienceCardError as exc:
        st.error(f"Could not load the experience card dataset: {exc}")
        return

    render_experience_grid(cards)


def render_sources(sources: list[dict]) -> None:
    """Render retrieved sources as compact chips, with a fallback expander.

    Chips give an at-a-glance view (title + id); the expander underneath
    keeps the full detail (category, chunk id, file path) available without
    cluttering the main chat/recommendation view.
    """
    if not sources:
        return

    st.caption("🔎 Sources show which JEJU-KB documents were used to ground this response.")

    seen_labels: list[str] = []
    chips_html = ""
    for source in sources:
        label = f"{source.get('title')} · {source.get('id')}"
        if label in seen_labels:
            continue
        seen_labels.append(label)
        chips_html += f'<span class="ml-source-chip">{label}</span>'
    st.markdown(f'<div class="ml-source-chip-row">{chips_html}</div>', unsafe_allow_html=True)

    with st.expander(f"Full source detail ({len(sources)})"):
        for source in sources:
            st.markdown(
                f"**{source.get('title')}** · `{source.get('id')}`\n\n"
                f"- Category: `{source.get('category')}`\n"
                f"- Chunk: `{source.get('chunk_id')}`\n"
                f"- File: `{source.get('file_path')}`"
            )
            st.divider()


def render_my_page_header() -> None:
    """Render the My Page avatar + title/subtitle honesty copy."""
    st.markdown('<div class="ml-avatar-circle">A</div>', unsafe_allow_html=True)
    render_screen_title("My Page", "Prototype only · Save feature not functional yet · No login in MVP")
