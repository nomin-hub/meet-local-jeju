# Stories

**Part of:** [JEJU-KB](../README.md)

## Purpose

Preserves oral history, local legends, and personal/community narratives that convey the lived experience of Jeju beyond official records. This category is what gives the AI's answers texture and emotional authenticity — the difference between listing a place and explaining why it matters to the people who live there.

## Data Sources

- Oral history archives and folklore collections
- Local storyteller and elder interviews (transcribed, with consent and attribution)
- Community-submitted personal narratives (subject to review — see Future Expansion)
- Published local history and legend compilations

## Example Documents

- "The legend of Grandmother Seolmundae and the creation of Jeju"
- "A haenyeo's account of three decades diving off the same coast"
- "Village founding stories from Jeju's mid-mountain (jungsangan) region"
- "What the stone grandfathers (dol hareubang) meant to the people who carved them"

## Metadata

Inherits the shared JEJU-KB metadata schema (see [architecture doc](../../docs/product/02_ARCHITECTURE.md#71-metadata-schema)):

| Field | Notes for this category |
|---|---|
| `category` | `stories` |
| `source_type` | Primarily `oral_history` and `community`; rarely `government` |
| `season` | Usually not applicable |
| `region` | Often highly specific (village- or site-level) |
| `trust_tier` | Explicitly tagged as narrative/anecdotal — never presented as verified fact without corroboration |
| `language` | Source language of the original telling, prior to translation |

## Future Expansion

- Structured community contribution and moderation pipeline (see architecture doc, Section 9).
- Multi-generational story pairing (same site/legend, multiple tellings) to reflect how oral history varies.
- Audio/original-language preservation alongside translated text.
