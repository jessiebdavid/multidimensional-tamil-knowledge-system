from pathlib import Path
import json

from tamil_rag.preprocessing.normalizer import normalize_tamil_text


BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "thirukkural_project_madurai.json"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "thirukkural"
)

OUTPUT_FILE = OUTPUT_DIR / "thirukkural_normalized.json"


def load_raw_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_records(records):
    normalized_records = []

    for record in records:
        original_text = record["original_text"]

        normalized_text = normalize_tamil_text(original_text)

        chapter_number = ((record["kural_number"] - 1) // 10) + 1

        normalized_record = {
            "work": record["work"],
            "author": record["author"],
            "kural_number": record["kural_number"],
            "chapter_number": chapter_number,
            "original_text": original_text,
            "normalized_text": normalized_text,
            "source": record["source"],
            "source_url": record["source_url"],
        }

        if "source_number" in record:
            normalized_record["source_number"] = record["source_number"]

        if "number_correction" in record:
            normalized_record["number_correction"] = record[
                "number_correction"
            ]

        normalized_records.append(normalized_record)

    return normalized_records


def save_normalized_data(records):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "work": "Thirukkural",
        "author": "Thiruvalluvar",
        "source": "Project Madurai",
        "source_url": (
            "https://www.projectmadurai.org/"
            "pm_etexts/utf8/pmuni0001.html"
        ),
        "records": records,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main():
    print("Loading crawled Tamil data...")

    data = load_raw_data()

    records = data["records"]

    print("Raw records:", len(records))

    print("Normalizing Tamil text...")

    normalized_records = normalize_records(records)

    save_normalized_data(normalized_records)

    print("Normalized records:", len(normalized_records))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()