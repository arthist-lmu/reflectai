import sys
import argparse

import json
import uuid


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer wikipedia data to a common format"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_path", help="verbose output")
    parser.add_argument("-o", "--output_path", help="verbose output")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    results = []

    with open(args.input_path) as f:
        for line in f:
            line_data = json.loads(line)
            line_id = uuid.uuid5(uuid.NAMESPACE_URL, line_data["url"]).hex

            language = line_data.get("language", ["de"])
            if isinstance(language, (list, set)):
                for l in language:
                    if l.lower() == "en":
                        language = "en"
                    if l.lower() == "de":
                        language = "de"

                if language != "en" and language != "de":
                    print(f"Unknown language: {line_data}")
                    exit(1)

            images = []
            if line_data.get("images"):
                images.append(
                    {
                        "url": line_data.get("images"),
                        "page": 0,
                        "id": uuid.uuid5(
                            uuid.NAMESPACE_URL, line_data.get("images")
                        ).hex,
                    }
                )
            results.append(
                {
                    "id": line_id,
                    "meta": {"url": line_data["url"]},
                    "text": [
                        {
                            "content": line_data["title"],
                            "page": 0,
                            "type": "title",
                            "language": language.lower(),
                        },
                        {
                            "content": line_data["text"]["Description"],
                            "page": 0,
                            "type": "text",
                            "language": language.lower(),
                        },
                    ],
                    "images": images,
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
