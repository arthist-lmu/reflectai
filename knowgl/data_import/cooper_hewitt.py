import sys
import argparse
import json
import uuid


"""
{
  "url": "https://collection.cooperhewitt.org/objects/68250857/",
  "title": "Textile (Netherlands)",
  "text": {
    "description": "In West Africa, special occasions are frequently marked by the creation of new designs for the colorful “Dutch Wax” fabrics which are so widely worn there. In its 167 years history, Vlisco has created innumerable commemorative fabrics for events of local or global importance. Their archives include a design commemorating the end of World War II featuring Franklin D. Roosevelt and Winston Churchill, one printed in 1963 for the creation of the independent Republic of Nigeria, and another from 1991 celebrating Nelson Mandela’s release from prison. \nLast year Vlisco created a fabric commemorating an event closer to home—the succession of King Willem-Alexander to the Dutch throne on April 30, 2013. The design features a portrait of the king with his wife, Queen Máxima, in a central medallion. The background shows one of Vlisco’s best-selling fabrics, called Fish Scales, coming off the rollers, as in the factory. \nThe fabric was printed as a limited edition, and was not available for purchase."
  },
  "images": [
    "https://images.collection.cooperhewitt.org/162344_8da7a8bb700f6157_b.jpg"
  ],
  "language": "EN"
}
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer cooper hewitt data to a common format"
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
                    "meta": {"url": line_data["url"]},
                    "text": [
                        {
                            "content": line_data["title"],
                            "page": 0,
                            "type": "title",
                            "language": language.lower(),
                        },
                        {
                            "content": line_data["text"]["description"],
                            "page": 0,
                            "type": "text",
                            "language": language.lower(),
                        },
                    ],
                    "images": [
                        {
                            "url": x,
                            "page": 0,
                            "id": uuid.uuid5(uuid.NAMESPACE_URL, x).hex,
                        }
                        for x in line_data.get("images", [])
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
