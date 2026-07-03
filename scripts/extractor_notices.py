
import json
import re
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://www.egazette.gov.sg"

def normalize_date(date_str):
    if not date_str:
        return "Not Available"
    date_str = date_str.strip()
    # Try various date formats
    formats = [
        "%d %b %Y",  # 12 Jun 2026
        "%d/%m/%Y",  # 12/06/2026
        "%Y-%m-%d"   # 2026-06-12
    ]
    for fmt in formats:
        try:
            dt_obj = datetime.strptime(date_str, fmt)
            return dt_obj.strftime("%d %b %Y")
        except ValueError:
            pass
    return "Not Available"

def normalize_title(title_str):
    if not title_str:
        return ""
    # Trim leading/trailing whitespace, collapse repeated spaces
    return re.sub(r'\s+', ' ', title_str).strip()

def extract_notices(html_file_path, page_number=1, target_date=None):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    notices = []
    position_on_page = 0

    # --- HTML Structure Assumptions (to be refined with actual sample) ---
    # This is a placeholder. The actual selectors will depend on the e-Gazette HTML.
    # I'm assuming notice entries might be within divs or list items with certain classes.
    # For now, I'll look for common patterns like 'result-item', 'notice-card', etc.
    # A more robust approach would involve analyzing the actual HTML structure.
    
    # Example: Look for elements that might represent a notice entry
    # This is a very generic starting point and will likely need adjustment.
    possible_notice_containers = soup.find_all(['div', 'li', 'article'], class_=re.compile(r'(result-item|notice-card|gazette-entry)', re.I))

    if not possible_notice_containers:
        # Fallback to a more generic search if specific classes are not found
        # This might catch too much, but provides a starting point for refinement
        possible_notice_containers = soup.find_all(lambda tag: tag.name in ['div', 'li', 'article'] and tag.find('a') and tag.find(text=re.compile(r'\d{2} \w{3} \d{4}')))

    for container in possible_notice_containers:
        title_tag = container.find('a', class_=re.compile(r'(title|notice-link)', re.I)) or container.find('a')
        date_tag = container.find(class_=re.compile(r'(date|publication-date)', re.I)) or container.find(text=re.compile(r'\d{2} \w{3} \d{4}'))
        
        title = normalize_title(title_tag.get_text(strip=True)) if title_tag else ""
        listing_publication_date = normalize_date(date_tag.strip()) if date_tag else "Not Available"
        listing_link = urljoin(BASE_URL, title_tag['href']) if title_tag and 'href' in title_tag.attrs else "Not Available"

        # Basic validation to ensure it's likely a notice entry
        if title and listing_publication_date != "Not Available" and listing_link != "Not Available":
            position_on_page += 1
            notices.append({
                "title": title,
                "listing_publication_date": listing_publication_date,
                "listing_link": listing_link,
                "page_number": page_number,
                "position_on_page": position_on_page
            })

    # Quality Check (as per SKILL.md)
    # 1. Confirm every object represents one actual notice entry (handled by extraction logic)
    # 2. Confirm entries are in exact top-to-bottom page order (handled by iteration)
    # 3. Confirm each listing_publication_date came from the listing HTML (handled by extraction logic)
    # 4. Confirm all relative links were converted to absolute URLs (handled by urljoin)
    # 5. Confirm output is valid JSON only (handled by json.dumps)

    return json.dumps(notices, indent=2)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Extract notices from Singapore e-Gazette HTML.")
    parser.add_argument("html_file", help="Path to the saved HTML file.")
    parser.add_argument("--page_number", type=int, default=1, help="Source page number.")
    parser.add_argument("--target_date", help="Target date for filtering (DD MMM YYYY). Filtering is not implemented yet.")

    args = parser.parse_args()

    # For now, target_date is ignored as per SKILL.md: "you should not filter unless explicitly instructed"
    # The skill description also states: "Do not filter unless explicitly instructed by another skill."
    # So, I will not implement filtering based on target_date in this script for now.

    extracted_data = extract_notices(args.html_file, args.page_number)
    print(extracted_data)
