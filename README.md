# Manual Poster Annotation Ground Truth Dataset

This directory contains manually annotated scientific posters that serve as ground truth for machine-actionable poster metadata extraction.

## Purpose

These annotations provide:
- **Training data** for automated poster extraction models
- **Validation benchmarks** for AI extraction quality assessment
- **Examples** of complete, machine-actionable poster metadata

## Directory Structure

Each poster is contained in its own folder named by a unique identifier (e.g., `42/`, `10890106/`). Within each folder, there are **four files** representing different aspects of the poster annotation:

```
{poster_id}/
├── {poster_id}.pdf          # Original poster file
├── {poster_id}_raw.md       # Extracted text in structured markdown
├── {poster_id}.json         # Full metadata JSON (complete schema)
├── {poster_id}_sub-json.json # Poster content subset (AI-ready)
```

---

## File Descriptions

### 1. Original Poster File (`{poster_id}.pdf` or `{poster_id}.jpg`)

The source poster file in its original format. This is the visual artifact from which all metadata is extracted.

**Accepted File Formats:**

#### Primary Formats (Recommended)
| Format | Extension | Notes |
|--------|-----------|-------|
| **PDF** | `.pdf` | Most common poster format. Must be single-page. |
| **PNG** | `.png` | Lossless image format. |
| **JPEG** | `.jpg`, `.jpeg` | Widely used image format. |
| **TIFF** | `.tiff`, `.tif` | High-quality, print-ready. |
| **PowerPoint** | `.pptx` | Must be single-slide. |
| **SVG** | `.svg` | Vector format from Figma/Illustrator. |

#### Additional Supported Formats
| Format | Extension | Notes |
|--------|-----------|-------|
| PowerPoint Legacy | `.ppt` | Older PowerPoint format. |
| OpenDocument | `.odp` | LibreOffice/OpenOffice presentations. |
| Keynote | `.key` | Apple Keynote (macOS). |
| EPS | `.eps` | Encapsulated PostScript vector. |
| WebP | `.webp` | Modern web image format. |
| GIF | `.gif` | Limited colors, rare for posters. |
| BMP | `.bmp` | Uncompressed bitmap. |
| HEIF | `.heic`, `.heif` | Apple high-efficiency format. |

#### Page/Slide Requirements

For multi-page formats (PDF, PPTX, PPT, ODP, KEY), only **single-page/single-slide documents** are accepted as valid posters. Multi-page documents are automatically flagged for review.

#### Design Tool Exports

If you created your poster in design software like Figma, Adobe Illustrator, or Canva, we recommend exporting as:
1. **PDF** (preferred) - maintains quality and is widely compatible
2. **SVG** - preserves vector quality
3. **PNG** - high-resolution raster fallback

---

### 2. Structured Markdown (`{poster_id}_raw.md`)

Human-readable text extracted from the poster, organized into logical sections. This file preserves the poster's textual content with semantic structure using markdown formatting.

**Characteristics:**
- Title and author information at the top
- Section headers matching poster sections (Abstract, Introduction, Methods, Results, etc.)
- Preserved figure/table references
- Citation and reference formatting
- Contact information

**Example structure:**
```markdown
# Poster Title

Author Name¹, Co-Author Name²

¹Institution 1; ²Institution 2

**Poster ID:** #XXX

## Abstract
[Abstract text...]

## Introduction
[Introduction text...]

## Methodology
[Methods text...]

## Results
[Results text with figure references...]

## Discussion/Conclusions
[Conclusions text...]

## References
[Formatted citations...]
```

---

### 3. Full Metadata JSON (`{poster_id}.json`)

Complete poster metadata including all available information:

- **Identifiers**: DOIs, poster numbers, file names
- **Creators**: Author names, ORCIDs, affiliations with ROR identifiers
- **Titles**: Main and alternative titles
- **Publisher**: Conference organizer or hosting institution
- **Publication Year**: Year of presentation
- **Subjects**: Keywords and classification terms
- **Dates**: Presentation dates, conference dates
- **Language**: Primary language (ISO 639)
- **Types**: Resource type (Conference Poster)
- **Related Identifiers**: DOIs to papers, datasets, software
- **Rights**: License information
- **Descriptions**: Abstract, Methods, Technical Info
- **Funding References**: Grant numbers, funder information
- **Conference**: Full conference metadata
- **Poster Content**: Structured section content
- **Image/Table Captions**: All figure and table captions
- **Domain**: Research field classification

---

### 4. Poster Content Sub-JSON (`{poster_id}_sub-json.json`)

A subset of the full JSON containing only the poster-derived content. This file is optimized for:
- AI/ML model training and inference
- Lightweight API responses
- Quick content preview

**Contents include:**
- Basic identifiers
- Minimal creator information (names, contact, affiliations)
- Title
- Poster content sections (Abstract, Introduction, Methods, Results, etc.)
- Image and table captions

**Key difference from full JSON:**
- Excludes external metadata (ORCIDs, ROR identifiers, DOIs)
- Excludes funding and rights information
- Excludes conference administrative details
- Focuses on what can be extracted directly from the poster image

---

## Annotated Posters

| ID | Domain | Conference | Year |
|----|--------|------------|------|
| 42 | Biomedical Informatics | AACR Annual Meeting | 2025 |
| 4737132 | - | - | - |
| 5128504 | - | - | - |
| 6724771 | - | - | - |
| 8228476 | - | - | - |
| 8228568 | - | - | - |
| 10890106 | - | - | - |
| 15963941 | - | - | - |
| 16083265 | - | - | - |
| 17268692 | - | - | - |

---

## Contributing

To add a new manual annotation:

1. Create a folder with a unique identifier: `{poster_id}/`
2. Add the original poster file: `{poster_id}.pdf` (or appropriate format)
3. Create the structured markdown: `{poster_id}_raw.md`
4. Create the sub-JSON with poster content: `{poster_id}_sub-json.json`
5. Create the full JSON with complete metadata: `{poster_id}.json`

---

## License

These annotations are provided for research and development purposes. Individual poster content remains subject to the original authors' rights and conference publication policies.
