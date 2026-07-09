# Experiences

**Part of:** [JEJU-KB](../README.md)

## Purpose

Documents concrete, describable activities a traveler can engage in that are locally authentic — distinct from generic "attractions" in the Tourism category. This is the category most directly responsible for the product's core promise: recommending things to *do* that feel genuinely local, not just places to *see*.

## Data Sources

- Local experience hosts and community activity write-ups
- Cultural workshops and hands-on programs (craft, farming, diving, cooking)
- Local guide and small-operator descriptions of non-commercial activities
- Traveler accounts specifically describing local-led or community-based activities

## Example Documents

- "Joining a haenyeo diving demonstration and hearing their stories firsthand"
- "Volunteering on a mandarin farm during harvest season"
- "Learning to make Jeju-style buckwheat noodles (memil guksu) in a home kitchen"
- "A morning at a local dry market before the tourist crowds arrive"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `experiences` |
| `source_type` | Mix of `community` and `editorial` |
| `season` | Often relevant — many experiences are seasonal (harvest, diving conditions, festivals) |
| `region` | High relevance — tied to specific locations/hosts |
| `trust_tier` | Medium-to-high; reviewed for authenticity and non-commercial framing |
| `language` | Source language of the original description |

## Future Expansion

- Explicit tagging to distinguish experiences from Tourism entries that merely describe a place.
- Community contribution pipeline for local hosts to describe their own activities.
- Cross-linking with Culture and Food for experiences that blend multiple categories (e.g., a cultural cooking class).
