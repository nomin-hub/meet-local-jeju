# Government

**Part of:** [JEJU-KB](../README.md)

## Purpose

Provides official/public information from trusted government and municipal sources — public facilities, regulations, and safety information relevant to travelers. This category exists to ground the AI's practical/administrative answers in verifiable official sources rather than informal or outdated secondhand information.

## Data Sources

- Jeju Special Self-Governing Province official publications
- Jeju Tourism Organization official materials
- Public safety and emergency information from municipal authorities
- Official visitor regulation notices (protected areas, environmental rules, etc.)

## Example Documents

- "Visitor regulations for Hallasan National Park"
- "Public safety guidance for coastal and diving areas"
- "Environmental protection rules travelers should know (e.g., Jeju's UNESCO-protected sites)"
- "Official public facility directory relevant to travelers (visitor centers, public restrooms, etc.)"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `government` |
| `source_type` | `government` exclusively — no informal/community sourcing in this category |
| `season` | Occasionally relevant (e.g., seasonal access restrictions) |
| `region` | Relevant for location-specific regulations |
| `trust_tier` | Highest — treated as authoritative fact |
| `language` | Original official-language publication, translated with care for regulatory accuracy |

## Future Expansion

- Direct feed/partnership with official Jeju government sources for freshness (see architecture doc, Section 13).
- Versioning and expiry tracking, since regulations and safety guidance can change.
- Structured fields for regulation type/severity to support clear, non-alarming presentation to travelers.
