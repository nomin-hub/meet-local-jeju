# Tourism

**Part of:** [JEJU-KB](../README.md)

## Purpose

Documents general points of interest and mainstream attractions. This category is retained deliberately — not to compete with existing travel guides, but to give the AI enough context on well-known attractions to contrast them against authentic local alternatives from the other nine categories, and to answer direct questions about popular sites honestly.

## Data Sources

- Jeju Tourism Organization official attraction listings
- Established travel guide content (used for factual baseline, not recommendation framing)
- Official visitor information center materials

## Example Documents

- "Seongsan Ilchulbong (Sunrise Peak): overview and visitor information"
- "Hallasan National Park: trails and practical visitor information"
- "Manjanggul Cave: overview and visitor information"
- "Jeju's major attractions: a factual baseline reference"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `tourism` |
| `source_type` | Predominantly `government`/institutional and `editorial` |
| `season` | Occasionally relevant (e.g., trail access, seasonal closures) |
| `region` | Relevant — attraction locations |
| `trust_tier` | Looser than Culture/Government, per architecture doc Section 7.2 — factual baseline, not curated for authenticity |
| `language` | Source language of the original listing |

## Future Expansion

- Explicit "mainstream vs. authentic alternative" cross-referencing with Experiences and Local Life.
- Visitor-load/crowding context to support the product's differentiation from generic tourist-attraction recommendations.
