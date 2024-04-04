import sys
import argparse
import json
import uuid
import re  # Import regular expressions


def parse_args():
    parser = argparse.ArgumentParser(description="Transfer met data to a common format")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument(
        "-i", "--input_path", help="path to input file"
    )  # Corrected help text
    parser.add_argument(
        "-o", "--output_path", help="path to output file"
    )  # Corrected help text

    args = parser.parse_args()
    return args


def extract_year(journal_text):
    # Use regular expression to find year in parentheses
    match = re.search(r"\((\d{4})\)", journal_text)
    return match.group(1) if match else "Unknown"


def main():
    args = parse_args()

    results = []
    with open(args.input_path) as f:
        for line in f:
            line_data = json.loads(line)
            line_id = uuid.uuid5(uuid.NAMESPACE_URL, line_data["url"]).hex

            language = line_data.get("language", "Unknown")
            if isinstance(language, (list, set)):
                language = "en" if "EN" in [l.upper() for l in language] else "Unknown"

            journal = line_data.get("journal", "Unknown")
            year = extract_year(journal)

            results.append(
                {
                    "id": line_id,
                    "meta": {
                        "url": line_data["url"],
                        "year": year,
                    },
                    "text": [
                        {
                            "content": line_data.get("title", "Unknown"),
                            "page": 0,
                            "type": "title",
                            "language": language.lower(),
                        },
                        {
                            "content": journal,
                            "page": 0,
                            "type": "text",
                            "language": language.lower(),
                        },
                    ],
                    "link": [
                        {
                            "url": line_data.get("url"),
                            "page": 0,
                            "id": uuid.uuid5(
                                uuid.NAMESPACE_URL, line_data.get("url")
                            ).hex,
                        }
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
