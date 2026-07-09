"""Experience recommendation mode for JEJU-KB.

Turns a traveler's stated preferences (interests, travel style, season, etc.)
into a retrieval query, then asks an OpenAI chat model to recommend authentic
local Jeju experiences grounded strictly in retrieved JEJU-KB context — the
same groundedness contract as `rag.chain.answer_question`, just structured as a
recommendation instead of a free-form Q&A answer.

This module is a recommendation feature only. It does not implement, and must
never imply, booking, payment, host onboarding, or marketplace functionality.

Reuses `rag.retriever.retrieve_relevant_documents` for retrieval and
`rag.chain.get_chat_model` / `rag.chain.format_context` / `rag.chain._document_to_source`
for model access, prompt context formatting, and source-dict construction, so
recommendation mode stays consistent with chat mode rather than duplicating logic.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Allow `python3 rag/recommender.py` to resolve `rag.retriever` / `rag.chain` even
# though running the file directly does not put the project root on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.messages import HumanMessage, SystemMessage

from rag.chain import _document_to_source, format_context, get_chat_model
from rag.retriever import retrieve_relevant_documents

DEFAULT_RECOMMENDATION_K = 6
MAX_RECOMMENDATIONS = 3

RECOMMENDATION_SYSTEM_PROMPT = """\
You are the Meet Local Jeju experience recommendation assistant. You help \
international travelers discover authentic local Jeju experiences that match \
their stated interests and travel style — not generic tourist attractions.

You must answer strictly using the JEJU-KB CONTEXT provided in the user message. \
Do not use outside knowledge about Jeju beyond that context.

This is a recommendation feature only, not a booking or marketplace feature. \
Never imply that an experience can be booked, reserved, or paid for through this \
assistant, and never mention prices, availability, or booking steps.

Rules you must always follow:
- Recommend only experiences that are clearly supported by the JEJU-KB CONTEXT — \
never invent an experience that isn't in the context.
- Recommend at most {max_recommendations} experiences. If the context only \
supports fewer good matches, recommend fewer rather than padding the list.
- Never invent exact prices, schedules, addresses, phone numbers, or named \
individuals/hosts. If the context does not include these specifics, omit them \
rather than guessing.
- If the traveler's stated preferences are not well covered by the context, say \
so plainly rather than forcing a recommendation to fit.
- Answer in clear, helpful English.

Format your response using exactly this structure:

## Summary
A short (2-3 sentence) summary of what kind of experiences fit this traveler.

## Recommended Local Experiences
For each recommended experience:
- **Experience title**
- Why it fits this traveler's stated preferences
- What local story or culture it connects to (only if the context supports it)
- Practical note (only if the context supports it — e.g. season, region, \
transportation; never invent a practical detail not present in the context)

## Suggested 1-Day Flow
If the recommended experiences can reasonably be sequenced into a single day \
(same region, compatible pacing), suggest a simple order. If they can't be \
reasonably combined in one day based on the context, say so instead of forcing \
a flow.

## Sources
List the document titles and IDs used, e.g. "Voices from the Sea: A Haenyeo's \
Daily Dive (STORY-0001)".
"""

RECOMMENDATION_USER_PROMPT_TEMPLATE = """\
TRAVELER PREFERENCES:
{preferences_text}

JEJU-KB CONTEXT:
{context}

Using only the JEJU-KB CONTEXT above, recommend authentic local Jeju \
experiences that fit these traveler preferences, following the exact \
structure in your system instructions.
"""


@dataclass
class TravelerPreferences:
    """Structured traveler preferences collected from the recommendation form.

    All fields are optional except `interests`, since the recommendation query
    needs at least some signal to retrieve against — the UI should still allow
    submitting with just travel style or a free-text note if a caller prefers.
    """

    interests: list[str] = field(default_factory=list)
    travel_style: list[str] = field(default_factory=list)
    season_or_month: str | None = None
    transportation: str | None = None
    preferred_area: str | None = None
    additional_notes: str | None = None

    def is_empty(self) -> bool:
        """Return True if no preference field carries any usable signal."""
        return not any(
            [
                self.interests,
                self.travel_style,
                self.season_or_month,
                self.transportation,
                self.preferred_area,
                self.additional_notes,
            ]
        )


def build_recommendation_query(preferences: TravelerPreferences) -> str:
    """Convert structured traveler preferences into a natural-language query.

    The resulting text is used both as the retrieval query (embedded and
    matched against JEJU-KB) and as the human-readable "TRAVELER PREFERENCES"
    block passed to the chat model, so retrieval and generation reason about
    the same description of the traveler.

    Args:
        preferences: The traveler's stated preferences.

    Returns:
        A natural-language description of the traveler's preferences. Empty or
        unset fields are omitted rather than filled with placeholder text.
    """
    lines: list[str] = []

    if preferences.interests:
        lines.append(f"Interests: {', '.join(preferences.interests)}")
    if preferences.travel_style:
        lines.append(f"Travel style: {', '.join(preferences.travel_style)}")
    if preferences.season_or_month:
        lines.append(f"Season or month: {preferences.season_or_month}")
    if preferences.transportation:
        lines.append(f"Transportation: {preferences.transportation}")
    if preferences.preferred_area:
        lines.append(f"Preferred area: {preferences.preferred_area}")
    if preferences.additional_notes:
        lines.append(f"Additional notes: {preferences.additional_notes}")

    if not lines:
        return (
            "No specific preferences given — recommend a well-rounded mix of "
            "authentic local Jeju experiences."
        )

    return "A traveler is looking for authentic local Jeju experiences with the following preferences:\n" + "\n".join(
        f"- {line}" for line in lines
    )


def get_experience_recommendations(
    preferences: TravelerPreferences, k: int = DEFAULT_RECOMMENDATION_K
) -> dict[str, Any]:
    """Recommend authentic local Jeju experiences grounded in JEJU-KB.

    Builds a retrieval query from `preferences`, retrieves the top-k most
    relevant JEJU-KB chunks, and asks the chat model to produce a structured
    recommendation (summary, recommended experiences, suggested 1-day flow,
    sources) strictly from that retrieved context. Uses the same chat model
    and groundedness rules as `rag.chain.answer_question`.

    Args:
        preferences: The traveler's stated preferences.
        k: Number of chunks to retrieve as context. Defaults to 6 (higher than
            the default Q&A retrieval count, to give the model enough spread
            across JEJU-KB categories to recommend more than one experience).

    Returns:
        A dict with:
          - `recommendation` (str): the model's structured recommendation text.
          - `sources` (list[dict]): one entry per retrieved chunk, each with
            `id`, `title`, `category`, `chunk_id`, and `file_path`.
          - `retrieved_documents` (list[Document]): the raw retrieved chunks.
          - `query` (str): the natural-language query built from `preferences`,
            for transparency/debugging.
    """
    query = build_recommendation_query(preferences)
    retrieved_documents = retrieve_relevant_documents(query, k=k)
    context = format_context(retrieved_documents)

    chat_model = get_chat_model()
    messages = [
        SystemMessage(
            content=RECOMMENDATION_SYSTEM_PROMPT.format(max_recommendations=MAX_RECOMMENDATIONS)
        ),
        HumanMessage(
            content=RECOMMENDATION_USER_PROMPT_TEMPLATE.format(
                preferences_text=query, context=context
            )
        ),
    ]
    response = chat_model.invoke(messages)

    return {
        "recommendation": response.content,
        "sources": [_document_to_source(doc) for doc in retrieved_documents],
        "retrieved_documents": retrieved_documents,
        "query": query,
    }


if __name__ == "__main__":
    sample_preferences = TravelerPreferences(
        interests=["culture", "local people", "food"],
        travel_style=["solo traveler", "cultural"],
        season_or_month="October",
        transportation="no car",
        preferred_area="Seogwipo",
        additional_notes="I want to meet local people, not just see attractions.",
    )

    result = get_experience_recommendations(sample_preferences)

    print(f"Query built from preferences:\n{result['query']}\n")
    print(f"Recommendation:\n{result['recommendation']}\n")
    print("Sources:")
    for source in result["sources"]:
        print(
            f"  - {source['id']} | {source['title']} | "
            f"{source['category']} | {source['chunk_id']} | {source['file_path']}"
        )
