# Local Life

**Part of:** [JEJU-KB](../README.md)

## Purpose

Captures the everyday rhythms of living on Jeju — how residents shop, commute, socialize, and spend ordinary time. This category is the connective tissue between the other nine: it grounds culture, food, and seasonal content in the texture of daily life rather than isolated facts, and is what lets the AI answer questions like *"What's it actually like to live here for a few weeks?"*

## Data Sources

- Local resident interviews and community write-ups
- Long-stay traveler and digital-nomad journals/blogs (vetted for accuracy)
- Local neighborhood and market guides
- Jeju-based community forums and local social groups (secondary, subject to curation review)

## Example Documents

- "A typical week for a Jeju-si resident: markets, routines, and neighborhood spots"
- "Where locals actually do their grocery shopping (and when)"
- "Everyday etiquette: greetings, pace of life, and small customs visitors miss"
- "Living near the coast vs. living inland: two different daily rhythms"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `local_life` |
| `source_type` | Typically `community` or `editorial`; rarely `government` |
| `season` | Optional — most content is evergreen, but some routines shift seasonally |
| `region` | High relevance — daily life varies meaningfully by town/neighborhood |
| `trust_tier` | Medium-to-high; community sourcing requires review before ingestion |
| `language` | Source language of the original account |

## Future Expansion

- Neighborhood-level breakdowns across the island (not just Jeju-si).
- First-person contributor pipeline once community submissions are supported (see architecture doc, Section 9).
- Cross-linking with Transportation and Food categories for practical day-to-day guidance.
