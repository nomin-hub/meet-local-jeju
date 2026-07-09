# Festivals

**Part of:** [JEJU-KB](../README.md)

## Purpose

Documents seasonal and community festivals, ceremonies, and their cultural significance and timing. Because festival relevance is time-bound, this category is a primary driver of the AI's seasonal-awareness capability described in the PRD's RAG Strategy.

## Data Sources

- Jeju provincial and municipal tourism/culture office event publications
- Village and community festival organizers
- Cultural heritage foundation event archives
- Local news coverage of festivals (for context and significance, not just schedules)

## Example Documents

- "Jeju Fire Festival (Deulbul Chukje): origins and what to expect"
- "Haenyeo Festival: honoring the women divers' tradition"
- "Village-level ancestral rites and seasonal ceremonies open to observers"
- "A month-by-month festival calendar for Jeju"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `festivals` |
| `source_type` | Predominantly `government`/institutional, supplemented by `editorial` and `community` context |
| `season` | Required — primary retrieval filter for this category |
| `region` | Relevant — many festivals are village- or town-specific |
| `trust_tier` | High for dates/logistics (must be accurate); medium for cultural-significance framing sourced informally |
| `language` | Source language of the original publication |

## Future Expansion

- Structured, date-indexed festival calendar to support proactive seasonal surfacing.
- Yearly refresh workflow, since festival dates and formats can change annually.
- Deeper linkage with Culture (significance) and Seasonal Living (agricultural-cycle timing).
