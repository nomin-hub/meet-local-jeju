# Transportation

**Part of:** [JEJU-KB](../README.md)

## Purpose

Documents practical local mobility knowledge — public transit patterns and authentic ways of getting around the island — to support exploration beyond taxis and rental cars. This category underpins the AI's ability to make its Local Life, Experiences, and Food recommendations actually reachable.

## Data Sources

- Jeju public bus system official schedules and route information
- Local transit guides for visitors (bus, ferry to nearby islands, etc.)
- Community write-ups on practical local travel (e.g., navigating rural bus routes)
- Official Jeju transportation authority publications

## Example Documents

- "How Jeju's public bus system works: routes, apps, and payment"
- "Getting to Udo and Marado: ferry logistics for outer islands"
- "Bicycling around Jeju: routes and practical considerations"
- "Getting to mid-mountain (jungsangan) villages without a rental car"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `transportation` |
| `source_type` | Mix of `government` (official transit authority) and `community`/`editorial` (practical guides) |
| `season` | Occasionally relevant (e.g., ferry schedule changes) |
| `region` | High relevance — route and access information is inherently location-specific |
| `trust_tier` | High for schedules/logistics; must be kept current to avoid stranding travelers on outdated information |
| `language` | Source language of the original publication |

## Future Expansion

- Freshness/expiry tracking for schedule-dependent content (routes and fares change).
- Structured route data to support more precise, location-aware retrieval.
- Integration point identified for future live transit data (explicitly out of scope for MVP — see PRD Non Goals).
