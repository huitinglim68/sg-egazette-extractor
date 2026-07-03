---
name: sg-egazette-extractor
description: Extracts structured notice data from saved HTML files of Singapore e-Gazette browse listing pages. Use for parsing e-Gazette browse results to obtain notice titles, publication dates, links, and their order on the page.
---

# Singapore e-Gazette HTML Extractor

## Usage

Run the extraction script against a saved HTML file from an e-Gazette browse results page:

```bash
python /home/ubuntu/skills/sg-egazette-extractor/scripts/extract_notices.py <html_file> [--page_number N]
```

The script outputs a JSON array to stdout. Each object represents one notice entry in top-to-bottom page order.

## Output Schema

```json
[
  {
    "title": "string",
    "listing_publication_date": "DD MMM YYYY or Not Available",
    "listing_link": "absolute URL or Not Available",
    "page_number": 1,
    "position_on_page": 1
  }
]
```

## Key Rules

- **Source of truth**: The saved HTML file only — do not open linked pages or PDFs unless another skill explicitly instructs it.
- **Dates**: Extract from the listing page HTML only; normalize to "DD MMM YYYY". Never infer from link text or PDF content.
- **Order**: Preserve exact top-to-bottom page order; do not deduplicate.
- **Links**: Convert relative links to absolute using `https://www.egazette.gov.sg`.
- **Exclusions**: Skip headings, navigation, filter labels, pagination, and category labels — extract notice entries only.
- **Filtering**: Do not filter by date unless explicitly instructed.

## Notes on the Script

`scripts/extract_notices.py` contains placeholder CSS selectors that were written before a real HTML sample was available. If extraction returns empty results, inspect the actual HTML structure and update the selectors in `extract_notices()` accordingly.
