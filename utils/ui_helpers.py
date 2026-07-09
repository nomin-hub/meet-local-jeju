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

from html import escape
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
    background: linear-gradient(180deg, #EAF7F8 0%, #F7EFE4 52%, #FFF9F0 100%);
}
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display: none;
}
[data-testid="stMainBlockContainer"] {
    max-width: 430px !important;
    margin: 14px auto 0 auto !important;
    background: #FFFDF8;
    border-radius: 32px;
    box-shadow: 0 18px 54px rgba(38, 70, 83, 0.18);
    padding: 18px 16px 116px 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.78);
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
.block-container {
    padding-top: 0 !important;
}
.stButton > button,
.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] button {
    border-radius: 999px !important;
    border: 1px solid #DDECE9 !important;
    background: #FFFFFF !important;
    color: #2D4E52 !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(38, 70, 83, 0.07) !important;
}
.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    border-color: #6FB7B1 !important;
    color: #173F44 !important;
}
div[data-testid="stFormSubmitButton"] button {
    background: #F26B2D !important;
    color: #FFFFFF !important;
    border-color: #F26B2D !important;
}
[data-testid="stRadio"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    color: #3A2E26 !important;
    font-weight: 700 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 8px;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    background: #F4FAF8;
    border: 1px solid #DDECE9;
    border-radius: 999px;
    padding: 7px 10px;
}
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: #255F68;
    border-color: #255F68;
    color: #FFFFFF !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
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
    color: #243C3F;
}
.ml-app-header-subtitle,
.ml-screen-subtitle {
    font-size: 12.5px;
    color: #6D7B79;
    margin: 0 0 10px 0;
}
.ml-screen-title {
    font-weight: 800;
    font-size: 19px;
    color: #3A2E26;
    margin: 2px 0 2px 0;
}
.ml-hero {
    border-radius: 24px;
    overflow: hidden;
    min-height: 178px;
    padding: 18px 16px;
    margin: 12px 0 14px 0;
    background:
        linear-gradient(145deg, rgba(19, 76, 83, 0.92), rgba(33, 128, 132, 0.64)),
        linear-gradient(45deg, #F26B2D 0 12%, #FFD6A5 12% 28%, #7CB7A2 28% 48%, #255F68 48% 100%);
    color: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 14px 28px rgba(38, 70, 83, 0.18);
}
.ml-hero-kicker {
    width: fit-content;
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 999px;
    padding: 4px 9px;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
}
.ml-hero-title {
    font-size: 28px;
    line-height: 1.05;
    font-weight: 900;
    max-width: 270px;
    margin: 12px 0 6px 0;
}
.ml-hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
}
.ml-hero-pill {
    background: rgba(255, 255, 255, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 999px;
    color: #FFFFFF;
    font-size: 10.5px;
    padding: 4px 8px;
}
.ml-hero-copy {
    font-size: 12.5px;
    line-height: 1.45;
    max-width: 310px;
    color: rgba(255, 255, 255, 0.9);
}
.ml-section-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 12px;
    margin: 14px 0 8px 0;
}
.ml-section-title {
    color: #243C3F;
    font-weight: 850;
    font-size: 16px;
}
.ml-section-note {
    color: #7B8D8B;
    font-size: 10.5px;
    text-align: right;
}
.ml-concierge-card,
.ml-preference-card,
.ml-empty-panel {
    background: #FFFFFF;
    border: 1px solid #E5EFEC;
    border-radius: 20px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(38, 70, 83, 0.08);
    margin: 10px 0 14px 0;
}
.ml-concierge-card {
    background:
        linear-gradient(135deg, rgba(255, 255, 255, 0.88), rgba(255, 243, 231, 0.92)),
        linear-gradient(90deg, #BFE7E6, #F26B2D);
}
.ml-concierge-top {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 7px;
}
.ml-concierge-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F26B2D;
    color: #FFFFFF;
    font-size: 19px;
    flex: 0 0 auto;
}
.ml-concierge-title {
    color: #243C3F;
    font-weight: 850;
    font-size: 14.5px;
}
.ml-concierge-copy,
.ml-empty-copy {
    color: #657875;
    font-size: 12px;
    line-height: 1.45;
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
    color: #8A4B24;
    background: #FFF0E4;
    border: 1px solid #FFD8BD;
    border-radius: 999px;
    padding: 4px 9px;
    white-space: nowrap;
}

/* ---------- Pinterest image-first card ---------- */
.ml-pin-card {
    background: #FFFFFF;
    border: 1px solid #E7EFEC;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 12px;
    box-shadow: 0 8px 18px rgba(38, 70, 83, 0.08);
}
.ml-pin-image {
    height: 124px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 38px;
    position: relative;
}
.ml-pin-image::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image: linear-gradient(0deg, rgba(22, 54, 58, 0.2), rgba(255,255,255,0));
}
.ml-pin-season {
    position: absolute;
    left: 9px;
    bottom: 9px;
    z-index: 1;
    max-width: calc(100% - 18px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    background: rgba(255, 255, 255, 0.88);
    color: #245F64;
    border-radius: 999px;
    padding: 3px 8px;
    font-size: 9.5px;
    font-weight: 800;
}
.ml-pin-body {
    padding: 10px 11px 12px 11px;
}
.ml-pin-chip {
    display: inline-block;
    background: #E9F5F3;
    color: #23676C;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0;
    padding: 2px 8px;
    border-radius: 999px;
    margin-bottom: 6px;
}
.ml-pin-title {
    font-weight: 850;
    font-size: 14px;
    color: #243C3F;
    margin: 0 0 3px 0;
    line-height: 1.25;
}
.ml-pin-desc {
    font-size: 11.5px;
    color: #667674;
    line-height: 1.35;
    margin-bottom: 6px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.ml-pin-story {
    font-size: 11px;
    color: #5D5148;
    background: #FFF8EF;
    border-left: 3px solid #F7A868;
    padding: 6px 7px;
    border-radius: 8px;
    margin-bottom: 7px;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.ml-pin-area {
    font-size: 10.5px;
    color: #7A8A88;
    margin-bottom: 5px;
}
.ml-pin-meta {
    font-size: 10.5px;
    color: #7A8A88;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.ml-pin-save {
    font-size: 10px;
    color: #8A4B24;
    background: #FFF0E4;
    border: 1px dashed #F2B98B;
    border-radius: 999px;
    padding: 3px 8px;
    display: inline-block;
}
.ml-kb-chip {
    font-size: 9.5px;
    color: #5D6F6C;
    background: #F2F8F7;
    border-radius: 999px;
    padding: 2px 7px;
    display: inline-block;
    margin: 0 3px 4px 0;
}
.ml-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
}

/* image-style gradient placeholders, cycled per card */
.ml-grad-0 { background: linear-gradient(135deg, #BFE7E6, #1A7D86); }
.ml-grad-1 { background: linear-gradient(135deg, #FFE6B7, #F26B2D); }
.ml-grad-2 { background: linear-gradient(135deg, #D9EBC8, #6E9F71); }
.ml-grad-3 { background: linear-gradient(135deg, #E1DED4, #645A50); }
.ml-grad-4 { background: linear-gradient(135deg, #F5D3CB, #D96F54); }
.ml-grad-5 { background: linear-gradient(135deg, #B8DDF0, #287E9B); }

/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 6px 8px !important;
    border: 1px solid rgba(221, 236, 233, 0.75);
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
    background: #EAF5F4;
    color: #245F64;
    border-radius: 999px;
    padding: 3px 9px;
}

/* ---------- My Page avatar ---------- */
.ml-avatar-circle {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: linear-gradient(135deg, #F26B2D, #255F68);
    color: #FFFFFF;
    font-weight: 800;
    font-size: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
}
.ml-saved-summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 12px 0 12px 0;
}
.ml-saved-stat {
    background: #FFFFFF;
    border: 1px solid #E5EFEC;
    border-radius: 16px;
    padding: 10px 8px;
    box-shadow: 0 4px 12px rgba(38, 70, 83, 0.06);
}
.ml-saved-number {
    color: #243C3F;
    font-size: 17px;
    font-weight: 900;
}
.ml-saved-label {
    color: #7B8D8B;
    font-size: 10px;
    line-height: 1.25;
}

/* ---------- Bottom tab navigation ---------- */
.st-key-bottom_nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    background: rgba(255, 253, 248, 0.96);
    border-top: 1px solid #E5EFEC;
    border-radius: 20px 20px 32px 32px;
    padding: 8px 16px 16px 16px;
    z-index: 9999;
    box-shadow: 0 -8px 24px rgba(38, 70, 83, 0.12);
}
.st-key-bottom_nav div[role="radiogroup"] {
    display: flex;
    justify-content: space-around;
}
.st-key-bottom_nav div[role="radiogroup"] label {
    background: transparent;
    border: 0;
    padding: 4px 8px;
}
.st-key-bottom_nav div[role="radiogroup"] label:has(input:checked) {
    background: #E9F5F3;
    border: 1px solid #D3E8E4;
    color: #245F64 !important;
}
.st-key-bottom_nav div[role="radiogroup"] label:has(input:checked) p {
    color: #245F64 !important;
}
@media (max-width: 480px) {
    [data-testid="stMainBlockContainer"] {
        max-width: none !important;
        width: calc(100vw - 18px) !important;
        margin: 8px auto 0 auto !important;
        border-radius: 26px;
    }
    .st-key-bottom_nav {
        max-width: none;
        width: calc(100vw - 18px);
        border-radius: 18px 18px 26px 26px;
    }
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
        f'<div class="ml-screen-title">{escape(title)}</div>'
        f'<div class="ml-screen-subtitle">{escape(subtitle)}</div>',
        unsafe_allow_html=True,
    )


def render_honesty_badges(labels: list[str]) -> None:
    """Render a row of small honesty labels, e.g. 'Prototype only'."""
    chips = "".join(f'<span class="ml-honesty-badge">{escape(label)}</span>' for label in labels)
    st.markdown(f'<div class="ml-honesty-row">{chips}</div>', unsafe_allow_html=True)


def render_home_hero() -> None:
    """Render the image-like Home hero panel."""
    st.markdown(
        """<div class="ml-hero">
<div>
<div class="ml-hero-kicker">Jeju local discovery</div>
<div class="ml-hero-title">Discover Jeju beyond tourism</div>
<div class="ml-hero-copy">Browse local food, villages, seasonal farming, ocean culture, and stories grounded in JEJU-KB.</div>
<div class="ml-hero-meta">
<span class="ml-hero-pill">RAG concierge</span>
<span class="ml-hero-pill">Local stories</span>
<span class="ml-hero-pill">Mock saves</span>
</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_section_header(title: str, note: str = "") -> None:
    """Render a compact section title row."""
    st.markdown(
        f"""<div class="ml-section-row">
<div class="ml-section-title">{escape(title)}</div>
<div class="ml-section-note">{escape(note)}</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_assistant_intro() -> None:
    """Render the AI Assistant product intro panel."""
    st.markdown(
        """<div class="ml-concierge-card">
<div class="ml-concierge-top">
<div class="ml-concierge-avatar">AI</div>
<div>
<div class="ml-concierge-title">Local AI concierge</div>
<div class="ml-concierge-copy">Tell me what kind of Jeju experience you want. I will answer from JEJU-KB and show the sources.</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_preference_intro() -> None:
    """Render a small shell for the recommendation form."""
    st.markdown(
        """<div class="ml-preference-card">
<div class="ml-concierge-title">Build a travel preference card</div>
<div class="ml-concierge-copy">Pick a few signals: interests, travel style, season, and transport. Recommendations stay grounded in JEJU-KB.</div>
</div>""",
        unsafe_allow_html=True,
    )


def _render_pin_card(card: dict, index: int) -> None:
    """Render a single image-first Pinterest-style card."""
    gradient_class = GRADIENT_CLASSES[index % len(GRADIENT_CLASSES)]
    best_for = card.get("best_for", [])
    best_for_text = ", ".join(best_for[:2]) if best_for else "local travelers"
    related_kb_ids = card.get("related_kb_ids", [])
    kb_chips = "".join(f'<span class="ml-kb-chip">{escape(kb_id)}</span>' for kb_id in related_kb_ids[:3])
    story = card.get("local_story", "")
    if len(story) > 128:
        story = f"{story[:125].rstrip()}..."
    st.markdown(
        f"""<div class="ml-pin-card">
<div class="ml-pin-image {gradient_class}">{escape(card.get('emoji', '📍'))}<span class="ml-pin-season">{escape(card.get('season', 'Seasonal'))}</span></div>
<div class="ml-pin-body">
<span class="ml-pin-chip">{escape(card['category'])}</span>
<div class="ml-pin-title">{escape(card['title'])}</div>
<div class="ml-pin-desc">{escape(card['description'])}</div>
<div class="ml-pin-story">Local hook: {escape(story)}</div>
<div class="ml-pin-area">📍 {escape(card['area'])}</div>
<div class="ml-pin-meta">🕒 {escape(card['duration'])} · Best for {escape(best_for_text)}</div>
<div>{kb_chips}</div>
<div class="ml-card-footer"><span class="ml-pin-save">Save idea - mock only</span></div>
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
    render_home_hero()
    render_honesty_badges(["Prototype only", "No booking", "No payment", "No login"])
    st.button(
        "Ask AI local concierge",
        use_container_width=True,
        key="home_ai_cta",
        on_click=lambda: st.session_state.update({"nav_radio": "💬 AI Assistant"}),
    )

    try:
        cards = load_experience_cards()
    except ExperienceCardError as exc:
        st.error(f"Could not load the experience card dataset: {exc}")
        return

    render_section_header("Featured local ideas", f"{len(cards)} cards from data/experiences")
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
        chips_html += f'<span class="ml-source-chip">{escape(label)}</span>'
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
    render_honesty_badges(["Mock saved ideas", "No real account", "No persistence"])
    st.markdown(
        """<div class="ml-saved-summary">
<div class="ml-saved-stat"><div class="ml-saved-number">4</div><div class="ml-saved-label">mock pins</div></div>
<div class="ml-saved-stat"><div class="ml-saved-number">0</div><div class="ml-saved-label">real trips</div></div>
<div class="ml-saved-stat"><div class="ml-saved-number">0</div><div class="ml-saved-label">bookings</div></div>
</div>""",
        unsafe_allow_html=True,
    )
