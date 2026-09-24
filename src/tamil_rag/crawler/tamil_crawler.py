from pathlib import Path
import json
import re

import requests
from bs4 import BeautifulSoup


PROJECT_MADURAI_URL = (
    "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0001.html"
)

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "thirukkural_project_madurai.json"


def fetch_page(url: str) -> str:
    """Fetch the HTML page from Project Madurai."""
    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "Tamil-Knowledge-System/1.0"
        },
    )

    response.raise_for_status()
    response.encoding = "utf-8"

    return response.text


def clean_text(text: str) -> str:
    """Clean whitespace while preserving the Tamil text."""
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()


def extract_kurals(html: str) -> list[dict]:
    """Extract Thirukkural verses from the Project Madurai page."""

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text("\n")

    lines = [
        clean_text(line)
        for line in text.splitlines()
        if clean_text(line)
    ]

    records = []

    number_occurrences = {}

    for index in range(1, len(lines)):
        current_line = lines[index]

        match = re.search(r"(\d+)\s*$", current_line)

        if not match:
            continue

        source_number_text = match.group(1)
        source_number = int(source_number_text)

        # Ignore numbers outside the Thirukkural range.
        if source_number > 1330 and source_number != 7811 and source_number != 12983:
            continue

        first_line = lines[index - 1]

        second_line = re.sub(
            r"\s*\d+\s*$",
            "",
            current_line,
        ).strip()

        if not first_line or not second_line:
            continue

        original_text = f"{first_line}\n{second_line}"

        # Track how many times a source number occurs.
        number_occurrences[source_number] = (
            number_occurrences.get(source_number, 0) + 1
        )

        occurrence = number_occurrences[source_number]

        # Project Madurai source numbering corrections.
        corrected_number = source_number
        correction = None

        if source_number == 71 and occurrence == 2:
            corrected_number = 72
            correction = "Project Madurai source repeats 71; corrected to 72."

        elif source_number == 752 and occurrence == 2:
            corrected_number = 753
            correction = "Project Madurai source repeats 752; corrected to 753."

        elif source_number == 7811:
            corrected_number = 781
            correction = "Project Madurai source contains 7811; corrected to 781."

        elif source_number == 12983:
            corrected_number = 1293
            correction = "Project Madurai source contains 12983; corrected to 1293."

        record = {
            "work": "Thirukkural",
            "author": "Thiruvalluvar",
            "kural_number": corrected_number,
            "original_text": original_text,
            "source": "Project Madurai",
            "source_url": PROJECT_MADURAI_URL,
        }

        if correction:
            record["source_number"] = source_number
            record["number_correction"] = correction

        records.append(record)

    # Remove duplicate corrected numbers while preserving order.
    unique_records = []
    seen = set()

    for record in records:
        number = record["kural_number"]

        if number not in seen:
            seen.add(number)
            unique_records.append(record)

    return unique_records

def save_records(records: list[dict]) -> None:
    """Save crawled records as UTF-8 JSON."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {
                "source": "Project Madurai",
                "source_url": PROJECT_MADURAI_URL,
                "work": "Thirukkural",
                "author": "Thiruvalluvar",
                "records": records,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )


def crawl_thirukkural() -> list[dict]:
    """Run the complete Thirukkural crawling process."""

    print("Fetching Project Madurai page...")

    html = fetch_page(PROJECT_MADURAI_URL)

    print("Extracting Thirukkural verses...")

    records = extract_kurals(html)

    print("Kurals extracted:", len(records))

    save_records(records)

    print("Saved to:", OUTPUT_FILE)

    return records


if __name__ == "__main__":
    crawl_thirukkural()