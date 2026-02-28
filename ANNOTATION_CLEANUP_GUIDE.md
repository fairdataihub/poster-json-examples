# Annotation Cleanup Guide

Systematic procedure for auditing and correcting `_sub-json.json` and `.json` reference annotations against the source poster PDF and the poster_schema.json.

## Pre-Flight: Load Context

Before touching any annotation, do these two things every time:

1. **Read the source poster** (the `.pdf` or `.jpg` in the poster's directory). This is the single source of truth.
2. **Read the schema** at `posters-science-json-schema/poster_schema.json`. Every field name, type, constraint, and `required` array matters.

## Checklist

Work through every item below for each poster. Do not skip items — mark N/A if not applicable.

---

### 1. Content Completeness ("If it's on the poster, we keep it")

- [ ] **Every word of visible poster text** must appear somewhere in the annotation (sections, captions, descriptions, creators, etc.). Do not delete, summarize, or paraphrase. Do not add text that is not on the poster.
- [ ] **Section content** must include the full text of each section as printed, including:
  - Bullet points, numbered lists (preserve structure with `\n` and `•` or `1.`, `2.` etc.)
  - Inline data from tables (participant codes, statistical values, cost figures, etc.)
  - Footnotes, disclaimers, and fine print
  - Contact info, URLs, emails (as an untitled section or within the appropriate section)
  - Institutional logos/text (e.g., "INDIANA UNIVERSITY BLOOMINGTON")
- [ ] **References section**: All citation text exactly as printed. Page numbers, volume numbers, DOIs — these are poster data.
- [ ] **Abbreviations section**: If the poster has one, include it as a section.
- [ ] **Disclosures / Conflict of Interest**: If present, include as a section with the actual title from the poster.
- [ ] **Acknowledgements / Funding**: If present, include as a section. Do not merge with unrelated sections.

### 2. Section Structure (Match the Poster Layout)

- [ ] **Section titles must match the poster's actual headings** — do not invent titles. If a section header on the poster says "Background: Who is in and who is out?" then `sectionTitle` is exactly that.
- [ ] **No fabricated headers**: If content on the poster has no header (e.g., contact block at the bottom), either omit `sectionTitle` entirely or leave it as `""` — but note the schema requires `minLength: 1` for `sectionTitle`, so **omit the field** rather than using empty string.
- [ ] **Row-based vs. column-based organization**: Match the poster's visual grouping.
  - If a poster has 4 rows (e.g., Cells / Interconnects / Stacks / Systems), each with Targets/Methods/Results columns, the sections should be organized **by row** (one section per row containing all its columns), not by column (one section per Targets, one per Methods, etc.).
  - If a poster has 4 distinct columns each with their own header, the sections follow the column structure.
  - When in doubt, look at the poster and ask: "What does a human read as one logical unit?"
- [ ] **Consolidated sections**: Do not over-split. If the poster shows one continuous block of text under a single header, it is one section, even if it has multiple paragraphs. Conversely, do not merge visually separate sections.

### 3. Metadata Accuracy

Every metadata field must come from the poster itself or be verifiable from the poster's context.

- [ ] **`publicationYear`**: Must match the year on the poster (conference year, copyright year, or date printed). Not 2025 unless the poster says 2025.
- [ ] **`conference`**:
  - `conferenceName`: The actual conference name as printed (e.g., "DH 2023", "ISPOR Europe 2023"). Not "Unknown Conference".
  - `conferenceYear`: Must match. Required field per schema.
  - `conferenceLocation`: City and country as printed (e.g., "Graz, Austria", "Copenhagen, Denmark"). Omit if not on the poster.
- [ ] **`subjects`**: Must be specific to the poster's research topic. Not the generic "scientific poster". Extract 2-5 keywords from the poster content (e.g., "digital humanists", "cost-effectiveness", "M dwarf stars").
- [ ] **`descriptions`**:
  - If the poster has a visible abstract, include it with `descriptionType: "Abstract"`.
  - If no abstract is on the poster, use `"descriptions": []` — do NOT use placeholder text like "Scientific poster abstract."
  - The description text must be **verbatim from the poster**, not invented.
- [ ] **`creators`**:
  - Names in `"Family, Given"` format per schema.
  - `nameType: "Personal"` for people.
  - `affiliation` entries must match the poster. Use the object form `{"name": "..."}` for consistency.
- [ ] **`rightsList`**: Include if a license is shown on the poster (CC-BY-4.0, etc.). Omit if no license visible.
- [ ] **`formats`**: `["PDF"]` for PDFs, `["JPEG"]` or `["PNG"]` for images.

### 4. Captions

- [ ] **`imageCaptions`**: Every figure on the poster with a caption gets an entry. Format: `{"id": "fig1", "caption": "Figure 1: ..."}`. Auto-number `fig1`, `fig2`, etc.
- [ ] **`tableCaptions`**: Every table on the poster with a caption gets an entry. Format: `{"id": "table1", "caption": "Table 1: ..."}`. Auto-number `table1`, `table2`, etc.
- [ ] **Caption text must be verbatim** from the poster, not summarized.
- [ ] If a poster has figures/tables but no visible captions, use `[]`.
- [ ] Schema only has `id` and `caption` fields for captions — no `data` field. Table cell data goes in the relevant content section.

### 5. Schema Compliance

- [ ] **`sectionTitle`**: If present, must have `minLength: 1`. Do not use `""`. Omit the field entirely for untitled sections.
- [ ] **`sectionContent`**: Must have `minLength: 1`. Every section must have content.
- [ ] **`identifier` and `identifierType`**: Both required if `identifiers` array is present.
- [ ] **`conferenceName` and `conferenceYear`**: Both required in `conference` object.
- [ ] **`description` and `descriptionType`**: Both required for each entry in `descriptions`.
- [ ] **No `additionalProperties`** on objects that forbid them (check `"additionalProperties": false` in schema — applies to creators, identifiers, sections, captions, etc.).
- [ ] **`$schema`** field should be `"https://posters.science/schema/v0.1/poster_schema.json"`.

### 6. Text Quality

- [ ] **Unicode characters**: Use actual Unicode in JSON, not escape sequences for readability. Write files with `ensure_ascii=False`. Exception: control characters and quotes that must be escaped for valid JSON.
  - `"Jänicke"` not `"J\u00e4nicke"`
  - `"€86,407"` not `"\u20ac86,407"`
  - `"CPS 1–19"` not `"CPS 1\u201319"`
- [ ] **No trailing whitespace** in field values.
- [ ] **Consistent line breaks**: Use `\n` within section content for paragraph breaks and list items. Use `\n\n` for major paragraph breaks.
- [ ] **Trailing newline** at end of file.
- [ ] **Proper JSON escaping**: Double quotes inside string values must be escaped as `\"`.

---

## Errors Found in the First 4 Posters

These are the specific problems we caught and fixed. Use them as a pattern-matching guide for the remaining 16.

### 4448680 (SOFC Fuel Cells)
- **Wrong section organization**: Sections were grouped by cross-cutting theme (all Targets, all Methods, all Results) instead of by the poster's visual rows (Cells, Interconnects, Stacks, Systems). Each row on the poster contains its own Targets/Methods/Results — that's one logical section.
- **Missing content**: Contact information and URLs (www.qSOFC.eu, www.innosofc.eu) were either missing or truncated.
- **Bullet formatting**: Inline `• item • item` was changed to newline-separated `\n• item` to match the poster layout.

### 4560930 (RECONS M Dwarf Stars)
- **Fake description**: `"Scientific poster abstract."` was in descriptions — this text is not on the poster. Replaced with `[]`.
- **Over-split sections**: 9 sections (including separate "Abstract", "Introduction", "SURVEY", "TWINS", "Contact", "References") were consolidated to 4 sections matching the poster's actual headers: "The RECONS Program", "A Tale of Two Samples", "M Dwarf Stellar Cycles - SURVEY", "M Dwarf Twin Binaries - TWINS".
- **Missing image captions**: Two figure captions visible on the poster were not captured. Added with proper `id`/`caption` format.
- **Removed "Contact" section**: Contact info (email, URL) was given its own section with a fabricated "Contact" header — that header doesn't exist on the poster.

### 8228568 (Digital Humanists, DH 2023)
- **Wrong `publicationYear`**: Was 2025, should be 2023 (poster says "DH 2023").
- **Wrong `conference`**: Was `"Unknown Conference"` / 2025. Fixed to `"DH 2023"` / 2023 / `"Graz, Austria"`.
- **Generic subjects**: `"scientific poster"` replaced with actual topics: "digital humanists", "research identity", "digital humanities".
- **Incomplete Results section**: Only had one summary sentence. The poster's Results section contains two full tables of participant data with quotes — all added verbatim.

### isporeu2023ee359130949-pdf (ISPOR Cost-Effectiveness)
- **Fake description**: `"Scientific poster abstract."` replaced with actual abstract text from the poster.
- **Missing sections**: References (15 citations), Disclosures (full conflict-of-interest text) were not captured at all.
- **Incomplete section content**: Introduction & Objectives was missing 3 paragraphs, Methods was missing extensive detail about survival models and cost data sources, Results was missing PSA paragraph and incremental LY data, Discussion was missing limitations paragraph.
- **Missing captions**: 2 figure captions and 3 table captions on the poster were not captured.
- **Wrong conference**: `"Unknown Conference"` → `"ISPOR Europe 2023"`, added location `"Copenhagen, Denmark"`.
- **Generic subjects**: `"scientific poster"` → specific terms from the research.

---

## Common Anti-Patterns to Watch For

| Anti-Pattern | Fix |
|---|---|
| `"description": "Scientific poster abstract."` | Remove or replace with actual abstract text from poster. If no abstract visible, use `"descriptions": []` |
| `"conferenceName": "Unknown Conference"` | Look at the poster for conference name, logo, or header text |
| `"subject": "scientific poster"` | Replace with 2-5 actual research keywords from poster content |
| `"publicationYear": 2025` | Check the poster — what year does it actually say? |
| Section titled `"Contact"` | Rarely a real poster header. Merge contact info into an untitled section or the section where it appears |
| Section titled `"Abstract"` when text is also in `descriptions` | Keep both — the section captures the poster layout, the description captures metadata |
| Sections split by theme across rows (all Targets / all Methods / all Results) | Reorganize by the poster's visual grouping (usually by row or column) |
| Missing figure/table captions | Look at every figure and table on the poster. If it has a caption, add it |
| `sectionTitle: ""` | Omit `sectionTitle` entirely (schema `minLength: 1`) |
| Summarized or paraphrased content | Replace with verbatim poster text |
| Missing References / Abbreviations / Disclosures sections | If visible on poster, add as sections |

---

## Workflow Per Poster

```
1. Open the poster PDF/image and read it completely
2. Open _sub-json.json side by side
3. Walk through the checklist above, item by item
4. Fix issues in _sub-json.json
5. Validate against schema: python -c "import json, jsonschema; ..."
6. If .json (full metadata) exists, apply same fixes there
7. Move to next poster
```
