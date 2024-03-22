import sys
import argparse
import json
import uuid


"""
{
  "url": "https://resources.metmuseum.org/resources/metpublications/pdf/Abraham_Lincoln_The_Man_Standing_Lincoln_The_Metropolitan_Museum_Journal_v_48_2013.pdf",
  "title": "Abraham Lincoln: The Man (Standing Lincoln): A Bronze Statuette by Augustus Saint-Gaudens",
  "journal": "Metropolitan Museum Journal, v. 48 (2013)",
  "language": [
    "EN"
  ]
}
"""


def parse_args():
    parser = argparse.ArgumentParser(description="Transfer met data to a common format")

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

            language = line_data["language"]
            if isinstance(language, (list, set)):
                for l in language:
                    if l.lower() == "en":
                        language = "en"

                if language != "en":
                    print(f"Unknown language: {line_data}")
                    exit(1)

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
                            "content": line_data["journal"],
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
                        # for x in line_data.get("url", [])
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
