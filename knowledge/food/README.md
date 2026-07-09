# Food

**Part of:** [JEJU-KB](../README.md)

## Purpose

Documents local Jeju cuisine, seasonal ingredients, traditional dishes, markets, and dining customs — distinct from generic restaurant recommendations. The focus is on food as a window into local life and seasonality, not on ranking restaurants.

## Data Sources

- Local culinary guides and traditional recipe archives
- Jeju agricultural and fisheries publications (ingredient sourcing/seasonality)
- Traditional market (owe-si/five-day market) documentation
- Local food culture write-ups and community accounts

## Example Documents

- "Jeju black pork (heuk-dwaeji): tradition, preparation, and where it comes from"
- "Abalone porridge (jeonbokjuk) and the haenyeo connection to Jeju cuisine"
- "Understanding Jeju's five-day markets (owe-il-jang) and how to shop them"
- "Seasonal seafood guide: what's fresh and when"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `food` |
| `source_type` | Mix of `editorial`, `community`, and `government` (fisheries/agriculture bodies) |
| `season` | Highly relevant for ingredient-based content |
| `region` | Relevant — markets and specialties vary by town |
| `trust_tier` | High bar for factual/health-related claims (e.g., preparation, sourcing) |
| `language` | Source language of the original material |

## Future Expansion

- Structured ingredient-seasonality data shared with the Seasonal Living category.
- Market-by-market documentation across the island, not just Jeju-si.
- Dietary/allergen-aware tagging for future personalization.
