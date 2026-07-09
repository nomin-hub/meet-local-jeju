# Seasonal Living

**Part of:** [JEJU-KB](../README.md)

## Purpose

Captures Jeju's seasonal farming cycles, harvest periods, and seasonal natural phenomena, along with how local life shifts across the year. This category is what lets the AI give time-aware answers — e.g., recommending canola fields in spring or mandarin harvesting in winter — instead of static, evergreen suggestions.

## Data Sources

- Jeju agricultural cooperative and farming calendar publications
- Local agricultural extension office materials
- Seasonal nature guides (bloom periods, harvest windows, migratory patterns)
- Local farmer interviews and seasonal work write-ups

## Example Documents

- "The Jeju mandarin (gamgyul) harvest calendar, month by month"
- "Canola (yuchae) bloom season: where and when"
- "What's in season: a farmer's-market guide by month"
- "Camellia bloom and winter coastal walks"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `seasonal_living` |
| `source_type` | Mix of `government` (agricultural bodies) and `editorial`/`community` |
| `season` | Required for nearly all documents in this category — primary retrieval filter |
| `region` | Relevant — growing regions and bloom locations vary across the island |
| `trust_tier` | High for agricultural/official sources; medium for informal seasonal guides |
| `language` | Source language of the original material |

## Future Expansion

- Structured seasonal calendar data to support proactive, date-aware surfacing (not just query-driven retrieval).
- Climate-shift tracking for bloom/harvest date drift over multiple years.
- Deeper linkage with Festivals (many festivals are timed to seasonal/agricultural cycles).
