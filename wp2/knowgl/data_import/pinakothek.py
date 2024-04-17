import sys
import argparse
import json
import uuid

### example input
{
    "url": "https://www.sammlung.pinakothek.de/de/bookmark/artwork/k2xnQ1m4Pd",
    "title": "Afrikanischer Mythos,",
    "text": {
        "Material / Technik / Bildträger": "schwarzer Plastikabfall",
        "Maße des Objekts": "550 cm",
        "Ausgestellt": "Nicht ausgestellt",
        "Inventarnummer": "B 810",
        "Erwerb": "1985 erworben als Ankauf aus der Galerie Bernd Klüser, München.",
        "Bestand": "Bayerische Staatsgemäldesammlungen - Sammlung Moderne Kunst\r\nin der Pinakothek der Moderne München",
        "Zitiervorschlag": "Tony Cragg, Afrikanischer Mythos, 1985, Bayerische Staatsgemäldesammlungen - Sammlung Moderne Kunst\r\nin der Pinakothek der Moderne München, URL: (Zuletzt aktualisiert am 19.06.2023)",
    },
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer pinakothek data to a common format"
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

            """ language = line_data["language"]
            if isinstance(language, (list, set)):
                for l in language:
                    if l.lower() == "en":
                        language = "en"                                          
                    if language != "en":
                    print(f"Unknown language: {line_data}")
                    exit(1) """

            results.append(
                {
                    "id": line_id,
                    "meta": {"url": line_data["url"]},
                    "title": line_data["title"],
                    "text": line_data["text"],
                    "images": [
                        {
                            "url": line_data["url"],
                            "page": 0,
                            "id": uuid.uuid5(uuid.NAMESPACE_URL, line_data["url"]).hex,
                        }
                        # for x in line_data.get("images", [])
                    ],
                }
            )

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
