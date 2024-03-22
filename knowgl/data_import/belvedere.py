import sys
import argparse
import json
import uuid


"""
{
  "url": "https://sammlung.belvedere.at/objects/23443/5jahresplan?ctx=38e3a89cffd339f987eeeef38ba7d801a2ac33a2&idx=11",
  "title": "5-Jahresplan",
  "text": {
    "description": "In ihren Videos, Fotoarbeiten und Installationen beobachtet Jermolaewa reale Begebenheiten und konzentriert sich hierbei auf einzelne Aspekte, die den Betrachtenden dazu animieren über Befindlichkeiten und Bedingungen des Alltags zu reflektieren. Dabei spielen Kategorien wie Zeit, Raum sowie geschichtlich und kulturelle Bezüge eine wichtige Rolle. Der Bildausschnitt, die Montage und die Wahl des Moments werden von der Künstlerin gezielt eingesetzt um das Skurrile und Absurde aufzuzeigen. In Ihren Arbeiten beschäftigt sich Jermolaewa unter anderen auch mit der russischen Kulturgeschichte die durch ihre Arbeitsweise Gegenstand einer subtilen Kritik wird. Five Year Plan ist ein andauerndes, nicht abgeschlossenes Projekt, für das Jermolaewa alle fünf Jahre die Passanten in der Moskauer U-Bahn filmt. Die Videos vergleichend betrachtend, ist festzustellen, dass kaum Änderungen in Kleidung und Werbung zu beobachten sind. Die einem Loop ähnlichen Aufnahmen zeigen weder den Anfang noch das Ende der Rolltreppe, die immer gleich bleibende Bewegung kommt einer Stagnation gleich. Der Fünf-Jahresplan war ein Vorhaben des Sowjetischen Regimes zur ökonomischen Förderung des Landes. Die Arbeit von Jermolaewa ist ein ironischer Kommentar, nimmt einen kritischen Standpunkt zur russischen Politik ein und zeigt den gefühlten Stillstand der Bevölkerung unter dem Regime auf. [Cathrin Mayer, 08/2011]"
  },
  "images": [
    "https://sammlung.belvedere.at/internal/media/dispatcher/36032",
    "https://sammlung.belvedere.at/internal/media/dispatcher/36031",
    "https://sammlung.belvedere.at/internal/media/dispatcher/36030"
  ],
  "language": "DE"
}
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer belvedere data to a common format"
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
