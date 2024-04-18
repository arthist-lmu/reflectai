import sys
import argparse
import json
import uuid


"""
{
  "url": "https://www.rijksmuseum.nl/en/collection/RP-T-1897-A-3376/catalogue-entry",
  "title": "View of Ruins at the Bank of a River",
  "text": {
    "entry": "Compared with the other four drawings by Van der Kabel in the museum’s collection, the present sheet marks a profound shift in style. The handling of earlier works, using delicate chalk strokes, is replaced by broadly applied passages of wash, conveying a sense of serenity that is echoed by the classical Arcadian composition. The scene is structured by a steady rhythm of verticals, diagonals and curves from the two tall fir trees and the ruins of the tower, vaults and column. The staffage has also changed in character: the figures are less angular and have slenderer proportions, with simple, rounded contours. Though the drawing’s full date has unfortunately been trimmed at lower right, its last digit is most probably an ‘8’, based on comparison with a stylistically related drawing dated 1658 in the Statens Museum for Kunst, Copenhagen (inv. no. TU 82 e/8).12 Another similar drawing from 1658 appeared on the Paris art market in 1995.13 Van der Kabel’s stylistic evolution can also be appreciated in an undated painting by him that was auctioned in Paris the same year, 1995.14 This stylistic shift towards Arcadian classicism may well have been prompted through exposure to works by French artists such as Gaspard Dughet (1615-1675). Two quickly drawn views of Lyon on a double-sided sheet in the Frits Lugt Collection, Fondation Custodia, Paris (inv. no. 39, recto and verso),15 feature a similar classical approach, including elegant staffage. These views suggest that the present drawing might have been made in Lyon, still belonging to a pre-Italian phase of Van der Kabel’s oeuvre. A stay in Lyon circa 1658-60, en route to Italy, where he is documented between circa 1660 and 1665, has often been hypothesized but never proven.16 Annemarie Stefes, 2019"
  },
  "images": [
    "http:////lh3.ggpht.com/o_MhFbQDEJgZQxpgXN9n5AIE4duD_6PY27YFkeP39XNZXzyi2zYsJimw49_dSe8YlYzf66yJaRHJR4EpRaOA8KP9jfA=s800"
  ],
  "language": "EN"
}
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer leiden data to a common format"
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
                            "content": line_data["text"]["entry"],
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
