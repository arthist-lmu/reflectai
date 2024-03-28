import sys
import argparse
import json
import uuid


# {
#     "url": "http://www.akademos.asm.md/files/O%20noua%20platforma%20stratefica%20pentru%20comunitatea%20stiintifica%20din%20RM.pdf",
#     "title": "A NEW STRATEGIC PLATFORM FOR THE SCIENTIFIC COMMUNITY OF MOLDOVA",
#     "journal": "Akademos: Revista de Ştiinţă, Inovare, Cultură şi Artă",
#     "language": ["EN", "RO", "RU"],
#     "subject": ["Arts in general", "Science"],
# }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer doaj data to a common format"
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
                            "language": language.lower(),
                        },
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
