# Culture

**Part of:** [JEJU-KB](../README.md)

## Purpose

Captures Jeju's distinct traditions, dialect, haenyeo (women divers) heritage, shamanic and folk practices, customs, and etiquette. This is one of the highest-trust-bar categories in JEJU-KB, since cultural claims carry real risk of misrepresentation if sourced or curated carelessly.

## Data Sources

- Academic and museum publications on Jeju culture and heritage
- UNESCO and cultural heritage documentation (haenyeo culture is UNESCO-recognized)
- Jeju dialect (Jejueo) reference materials
- Cultural center and heritage foundation materials

## Example Documents

- "Haenyeo culture: history, practice, and present-day status"
- "An introduction to Jeju dialect (Jejueo) for visitors"
- "Shamanic ritual traditions (gut) and their role in Jeju village life"
- "Etiquette guide: what visitors should know before engaging with local traditions"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `culture` |
| `source_type` | Predominantly `editorial` and `government`/institutional (museums, heritage bodies) |
| `season` | Usually not applicable, except for seasonal ritual practices |
| `region` | Often relevant — some traditions are village- or region-specific |
| `trust_tier` | Highest bar in JEJU-KB — required review before ingestion (see architecture doc, Section 7.2) |
| `language` | Source language, with attention to accurate translation of culturally specific terms |

## Future Expansion

- Partnership with Jeju cultural institutions for verified content feeds (see architecture doc, Section 13).
- Jejueo (dialect) glossary as a structured sub-resource.
- Sensitivity review workflow specific to sacred/ritual content.
