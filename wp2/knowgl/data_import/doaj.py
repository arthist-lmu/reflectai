import sys
import argparse
import json
import uuid


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer doaj data to a common format"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument(
        "-i", "--input_path", help="path to input file"
    )  # Correct help text
    parser.add_argument(
        "-o", "--output_path", help="path to output file"
    )  # Correct help text

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    results = []
    with open(args.input_path) as f:
        for line in f:
            line_data = json.loads(line)
            line_id = uuid.uuid5(uuid.NAMESPACE_URL, line_data["url"]).hex

            language = "unknown"
            if isinstance(line_data.get("language", []), (list, set)):
                if "EN" in [l.upper() for l in line_data["language"]]:
                    language = "en"
                if "DE" in [l.upper() for l in line_data["language"]]:
                    language = "de"
                else:
                    continue

            results.append(
                {
                    "id": line_id,
                    "meta": {
                        "url": line_data["url"],
                        "subject": line_data["subject"],
                        "journal": line_data["journal"],
                    },
                    "text": [
                        {
                            "content": line_data["title"],
                            "page": 0,
                            "type": "title",
                            "language": language,
                        },
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return
