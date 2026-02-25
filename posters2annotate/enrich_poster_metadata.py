#!/usr/bin/env python3
"""
Enrich poster annotation JSON files with Zenodo metadata and organize into
the canonical subfolder structure matching the existing manual_poster_annotation layout.

Source: poster_metadata_all/poster_metadata/ (draft annotations)
Target: posters2annotate/<id>/<id>.json, <id>_sub-json.json, <id>_raw.md

For zenodo-prefixed files: fetches metadata from Zenodo API to fill in
missing/incorrect fields (conference, dates, publisher, etc.)
For non-zenodo files: ensures schema-required fields are present.
"""

import json
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError

BASE_DIR = Path(__file__).parent  # posters2annotate/
METADATA_DIR = BASE_DIR / "poster_metadata_all" / "poster_metadata"
SCHEMA_PATH = BASE_DIR.parent.parent / "posters-science-json-schema" / "poster_schema.json"

ZENODO_API = "https://zenodo.org/api/records"

ZENODO_PUBLISHER = {
    "name": "Zenodo",
    "publisherIdentifier": "https://ror.org/01zzys052",
    "publisherIdentifierScheme": "ROR",
    "schemeURI": "https://ror.org",
}

LICENSE_MAP = {
    "cc-by-4.0": {
        "rights": "Creative Commons Attribution 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by/4.0/",
        "rightsIdentifier": "CC-BY-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    },
    "cc-by-sa-4.0": {
        "rights": "Creative Commons Attribution Share Alike 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by-sa/4.0/",
        "rightsIdentifier": "CC-BY-SA-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    },
    "cc-by-nc-4.0": {
        "rights": "Creative Commons Attribution Non Commercial 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by-nc/4.0/",
        "rightsIdentifier": "CC-BY-NC-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    },
    "cc0-1.0": {
        "rights": "Creative Commons Zero v1.0 Universal",
        "rightsUri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "rightsIdentifier": "CC0-1.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    },
}

LANG_MAP = {
    "eng": "en", "deu": "de", "fra": "fr", "spa": "es",
    "ita": "it", "por": "pt", "nld": "nl", "jpn": "ja",
    "zho": "zh", "rus": "ru", "pol": "pl", "tur": "tr",
}

# Schema field ordering for readability
FIELD_ORDER = [
    "$schema", "identifiers", "creators", "titles", "publisher",
    "publicationYear", "subjects", "dates", "language", "types",
    "relatedIdentifiers", "sizes", "formats", "version", "rightsList",
    "descriptions", "fundingReferences", "conference", "researchField",
    "content", "imageCaptions", "tableCaptions",
]

REQUIRED_FIELDS = [
    "creators", "titles", "publicationYear", "subjects",
    "descriptions", "publisher", "conference", "formats",
]


# ── Zenodo API ──────────────────────────────────────────────────────

def fetch_zenodo_record(record_id: str) -> dict:
    """Fetch a single Zenodo record by ID."""
    url = f"{ZENODO_API}/{record_id}"
    print(f"  Fetching {url} ...")
    req = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        print(f"  ERROR: HTTP {e.code} fetching record {record_id}")
        return {}


def extract_zenodo_id(filename: str) -> str | None:
    """Extract Zenodo record ID from a filename like zenodo_4446908_..."""
    m = re.match(r"zenodo_(\d+)_", filename)
    return m.group(1) if m else None


def normalize_language(lang: str) -> str:
    if not lang:
        return "en"
    lang_lower = lang.lower()
    return LANG_MAP.get(lang_lower, lang_lower[:2] if len(lang_lower) > 2 else lang_lower)


def convert_zenodo_meeting(meeting: dict) -> dict:
    """Convert Zenodo meeting metadata to schema conference object."""
    conference = {}
    if meeting.get("title"):
        conference["conferenceName"] = meeting["title"]
    if meeting.get("acronym"):
        conference["conferenceAcronym"] = meeting["acronym"]
    if meeting.get("place"):
        conference["conferenceLocation"] = meeting["place"]
    if meeting.get("url"):
        conference["conferenceUri"] = meeting["url"]
    dates_str = meeting.get("dates", "")
    if dates_str and " - " in dates_str:
        parts = dates_str.split(" - ")
        conference["conferenceStartDate"] = parts[0].strip()
        conference["conferenceEndDate"] = parts[1].strip()
    return conference


def build_zenodo_metadata(record: dict) -> dict:
    """Build enrichment data from a Zenodo API record."""
    meta = record.get("metadata", {})
    result = {}

    doi = record.get("doi")
    if doi:
        result["_doi"] = doi

    creators = []
    for c in meta.get("creators", []):
        entry = {"name": c.get("name", ""), "nameType": "Personal"}
        if c.get("affiliation"):
            entry["affiliation"] = [{"name": c["affiliation"]}]
        if c.get("orcid"):
            entry["nameIdentifiers"] = [{
                "nameIdentifier": f"https://orcid.org/{c['orcid']}",
                "nameIdentifierScheme": "ORCID",
                "schemeURI": "https://orcid.org",
            }]
        creators.append(entry)
    if creators:
        result["_creators"] = creators

    title = meta.get("title")
    if title:
        result["_title"] = title

    pub_date = meta.get("publication_date")
    if pub_date:
        try:
            result["publicationYear"] = int(pub_date[:4])
        except (ValueError, TypeError):
            pass
        result["_dates"] = [{"date": pub_date, "dateType": "Issued"}]

    description = meta.get("description")
    if description:
        result["_description"] = re.sub(r"<[^>]+>", "", description).strip()

    keywords = meta.get("keywords", [])
    if keywords:
        result["_keywords"] = keywords

    language = meta.get("language")
    if language:
        result["language"] = normalize_language(language)

    license_info = meta.get("license")
    if license_info:
        lid = license_info.get("id", "") if isinstance(license_info, dict) else str(license_info)
        result["_license_id"] = lid

    meeting = meta.get("meeting") or meta.get("meetings")
    if meeting:
        if isinstance(meeting, dict):
            result["_conference"] = convert_zenodo_meeting(meeting)
        elif isinstance(meeting, list) and meeting:
            result["_conference"] = convert_zenodo_meeting(meeting[0])

    grants = meta.get("grants", [])
    if grants:
        funders = []
        for g in grants:
            entry = {}
            funder = g.get("funder", {})
            if funder.get("name"):
                entry["funderName"] = funder["name"]
            if g.get("title"):
                entry["awardTitle"] = g["title"]
            if g.get("code"):
                entry["awardNumber"] = g["code"]
            if entry:
                funders.append(entry)
        if funders:
            result["_funding"] = funders

    return result


# ── Enrichment logic ────────────────────────────────────────────────

def enrich(data: dict, zenodo_meta: dict | None = None,
           full_data: dict | None = None) -> tuple[dict, list[str]]:
    """
    Enrich a poster JSON dict with missing metadata.
    zenodo_meta: data from Zenodo API (for zenodo posters)
    full_data: corresponding _full.json data (for _sub-json inheritance)
    Returns (enriched_data, list_of_changes).
    """
    changes = []

    # Helper: try zenodo first, then _full fallback
    def fill_from(field, zenodo_key=None, transform=None):
        if field in data and data[field]:
            return
        # Try Zenodo
        if zenodo_meta and zenodo_key and zenodo_meta.get(zenodo_key):
            val = zenodo_meta[zenodo_key]
            if transform:
                val = transform(val)
            data[field] = val
            changes.append(f"+ {field} (from Zenodo)")
            return
        # Try _full.json
        if full_data and field in full_data and full_data[field]:
            data[field] = full_data[field]
            changes.append(f"+ {field} (from _full.json)")
            return

    # --- Required fields ---

    # publisher
    if "publisher" not in data or not data.get("publisher"):
        if zenodo_meta:
            data["publisher"] = ZENODO_PUBLISHER.copy()
            changes.append("+ publisher (Zenodo)")
        elif full_data and full_data.get("publisher"):
            data["publisher"] = full_data["publisher"]
            changes.append(f"+ publisher (from _full: {full_data['publisher'].get('name', '?')})")

    # conference
    if "conference" not in data or not data.get("conference"):
        if zenodo_meta and zenodo_meta.get("_conference"):
            conf = zenodo_meta["_conference"].copy()
            if "conferenceYear" not in conf:
                conf["conferenceYear"] = zenodo_meta.get("publicationYear",
                                                          data.get("publicationYear", 2025))
            data["conference"] = conf
            changes.append(f"+ conference ({conf.get('conferenceName', 'Zenodo')})")
        elif full_data and full_data.get("conference"):
            data["conference"] = full_data["conference"]
            changes.append(f"+ conference (from _full)")
        elif zenodo_meta:
            year = zenodo_meta.get("publicationYear", data.get("publicationYear", 2025))
            data["conference"] = {"conferenceName": "Unknown Conference", "conferenceYear": year}
            changes.append("+ conference (placeholder)")

    # Ensure conferenceYear if conference exists
    if "conference" in data and data["conference"] and "conferenceYear" not in data["conference"]:
        year = data.get("publicationYear")
        if zenodo_meta:
            year = zenodo_meta.get("publicationYear", year)
        if year:
            data["conference"]["conferenceYear"] = year
            changes.append(f"+ conferenceYear ({year})")

    # publicationYear
    if "publicationYear" not in data:
        if zenodo_meta and zenodo_meta.get("publicationYear"):
            data["publicationYear"] = zenodo_meta["publicationYear"]
            changes.append(f"+ publicationYear ({zenodo_meta['publicationYear']})")
        elif full_data and full_data.get("publicationYear"):
            data["publicationYear"] = full_data["publicationYear"]
            changes.append(f"+ publicationYear (from _full: {full_data['publicationYear']})")

    # dates
    if "dates" not in data or not data.get("dates"):
        if zenodo_meta and zenodo_meta.get("_dates"):
            data["dates"] = zenodo_meta["_dates"]
            changes.append(f"+ dates ({data['dates'][0]['date']})")
        elif full_data and full_data.get("dates"):
            data["dates"] = full_data["dates"]
            changes.append("+ dates (from _full)")

    # descriptions
    fill_from("descriptions", "_description",
              lambda d: [{"description": d, "descriptionType": "Abstract"}])

    # subjects
    fill_from("subjects", "_keywords",
              lambda kws: [{"subject": kw} for kw in kws])

    # formats
    if "formats" not in data or not data.get("formats"):
        data["formats"] = ["application/pdf"]
        changes.append("+ formats (application/pdf)")

    # creators
    fill_from("creators", "_creators")

    # titles
    fill_from("titles", "_title", lambda t: [{"title": t}])

    # --- Optional enrichment from Zenodo ---
    if zenodo_meta:
        # DOI in identifiers
        doi = zenodo_meta.get("_doi")
        if doi:
            ids = data.get("identifiers", [])
            if not any(i.get("identifierType") == "DOI" for i in ids):
                ids.insert(0, {"identifier": doi, "identifierType": "DOI"})
                data["identifiers"] = ids
                changes.append(f"+ DOI ({doi})")

        # language
        if "language" not in data and zenodo_meta.get("language"):
            data["language"] = zenodo_meta["language"]
            changes.append(f"+ language ({zenodo_meta['language']})")

        # rightsList
        if ("rightsList" not in data or not data.get("rightsList")):
            lid = zenodo_meta.get("_license_id", "").lower()
            if lid in LICENSE_MAP:
                data["rightsList"] = [LICENSE_MAP[lid]]
                changes.append(f"+ rightsList ({lid})")

    # --- Reorder keys for readability ---
    ordered = {}
    for key in FIELD_ORDER:
        if key in data:
            ordered[key] = data[key]
    for key in data:
        if key not in ordered:
            ordered[key] = data[key]

    return ordered, changes


def validate(data: dict) -> list[str]:
    """Check for missing required schema fields."""
    issues = []
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            issues.append(f"MISSING required: {field}")
    if "conference" in data and data["conference"]:
        conf = data["conference"]
        if "conferenceName" not in conf:
            issues.append("conference.conferenceName missing")
        if "conferenceYear" not in conf:
            issues.append("conference.conferenceYear missing")
    return issues


# ── File discovery & naming ─────────────────────────────────────────

def discover_posters() -> list[dict]:
    """
    Discover poster sets in poster_metadata/.
    Returns list of dicts with keys: base, folder_id, zenodo_id,
    full_path, sub_path, raw_path, pdf_path.
    """
    posters = {}
    for f in sorted(METADATA_DIR.glob("*.json")):
        stem = f.stem
        if stem.endswith("_full"):
            base = stem[:-5]
            posters.setdefault(base, {})["full"] = f
        elif stem.endswith("_sub-json"):
            base = stem[:-9]
            posters.setdefault(base, {})["sub"] = f

    # Also find _raw.md files
    for f in sorted(METADATA_DIR.glob("*_raw.md")):
        stem = f.stem
        if stem.endswith("_raw"):
            base = stem[:-4]
            if base in posters:
                posters[base]["raw"] = f

    result = []
    for base, files in sorted(posters.items()):
        zenodo_id = extract_zenodo_id(base + "_")

        # Determine folder ID
        if zenodo_id:
            folder_id = zenodo_id
        else:
            folder_id = base

        # Find PDF in posters2annotate/
        pdf_path = None
        for ext in ("*.pdf", "*.PDF"):
            for pdf in BASE_DIR.glob(ext):
                # Match by checking if base appears in pdf name (allow fuzzy)
                pdf_base = pdf.stem
                if zenodo_id and f"zenodo_{zenodo_id}" in pdf.name:
                    pdf_path = pdf
                    break
                elif not zenodo_id and base == pdf_base:
                    pdf_path = pdf
                    break
            if pdf_path:
                break

        result.append({
            "base": base,
            "folder_id": folder_id,
            "zenodo_id": zenodo_id,
            "full": files.get("full"),
            "sub": files.get("sub"),
            "raw": files.get("raw"),
            "pdf": pdf_path,
        })

    return result


def save_json(data: dict, path: Path):
    """Write JSON with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ── Main ────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE (no files modified) ===\n")

    posters = discover_posters()
    print(f"Found {len(posters)} posters to process\n")

    # Fetch Zenodo metadata
    zenodo_cache = {}
    for p in posters:
        if p["zenodo_id"]:
            print(f"  {p['base']} → Zenodo ID {p['zenodo_id']}")
            record = fetch_zenodo_record(p["zenodo_id"])
            if record:
                zenodo_cache[p["base"]] = build_zenodo_metadata(record)
            time.sleep(0.5)
        else:
            print(f"  {p['base']} → no Zenodo ID (skip API)")

    print(f"\n{'='*60}")
    print("ENRICHING & ORGANIZING")
    print(f"{'='*60}\n")

    all_valid = True
    for p in posters:
        fid = p["folder_id"]
        zmeta = zenodo_cache.get(p["base"])
        target_dir = BASE_DIR / fid
        print(f"\n── {fid}/ ──")

        # Process _full.json first
        full_data = None
        if p["full"]:
            with open(p["full"], "r", encoding="utf-8") as f:
                full_data = json.load(f)
            enriched, changes = enrich(full_data, zenodo_meta=zmeta)
            full_data = enriched  # save for sub-json inheritance

            target_full = target_dir / f"{fid}.json"
            if changes:
                for c in changes:
                    print(f"  {fid}.json: {c}")
            else:
                print(f"  {fid}.json: OK (no metadata changes)")

            issues = validate(enriched)
            if issues:
                all_valid = False
                for issue in issues:
                    print(f"  {fid}.json VALIDATION: {issue}")
            else:
                print(f"  {fid}.json: PASS validation")

            if not dry_run:
                save_json(enriched, target_full)
                print(f"  → {target_full.relative_to(BASE_DIR)}")

        # Process _sub-json.json
        if p["sub"]:
            with open(p["sub"], "r", encoding="utf-8") as f:
                sub_data = json.load(f)
            enriched_sub, changes_sub = enrich(sub_data, zenodo_meta=zmeta,
                                                full_data=full_data)

            target_sub = target_dir / f"{fid}_sub-json.json"
            if changes_sub:
                for c in changes_sub:
                    print(f"  {fid}_sub-json.json: {c}")
            else:
                print(f"  {fid}_sub-json.json: OK (no metadata changes)")

            issues_sub = validate(enriched_sub)
            if issues_sub:
                all_valid = False
                for issue in issues_sub:
                    print(f"  {fid}_sub-json.json VALIDATION: {issue}")
            else:
                print(f"  {fid}_sub-json.json: PASS validation")

            if not dry_run:
                save_json(enriched_sub, target_sub)
                print(f"  → {target_sub.relative_to(BASE_DIR)}")

        # Copy _raw.md
        if p["raw"]:
            target_raw = target_dir / f"{fid}_raw.md"
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p["raw"], target_raw)
            print(f"  → {target_raw.relative_to(BASE_DIR)} (raw text)")

        # Copy PDF
        if p["pdf"]:
            target_pdf = target_dir / f"{fid}{p['pdf'].suffix}"
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p["pdf"], target_pdf)
            print(f"  → {target_pdf.relative_to(BASE_DIR)} (poster file)")
        else:
            print(f"  ! No PDF found for {p['base']}")

    print(f"\n{'='*60}")
    if all_valid:
        print("ALL FILES PASS required-field validation!")
    else:
        print("SOME FILES have validation issues (see above).")
    print(f"{'='*60}")

    if dry_run:
        print("\n(Dry run - no files modified. Run without --dry-run to apply.)")
    else:
        print(f"\nOrganized {len(posters)} posters into subfolders under: {BASE_DIR}/")


if __name__ == "__main__":
    main()
