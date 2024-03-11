import sys
import argparse


# {
#     "url": "https:\/\/online-sammlung.hamburger-kunsthalle.de\/de\/objekt\/22301\/stehender-bauer-von-hinten-gesehen?term=&start=4660&context=default&position=4666",
#     "title": "Stehender Bauer, von hinten gesehen, um 1652",
#     "text": {
#         "description": "Auch diese Zeichnung kann um 1652 datiert werden, weil der K\u00fcnstler f\u00fcr ein Gem\u00e4lde diesen Jahres auf die recto-Studie zur\u00fcckgriff.(Anm.1) Von sp\u00e4terer Hand wurde das Papier beschnitten, vielleicht, um den stehenden Bauern der Vorderseite besser im Blatt zu platzieren. Auch die f\u00fcr Van Ostade ungew\u00f6hnliche Lavierung stammt sicher von sp\u00e4terer Hand, m\u00f6glicherweise von Cornelis Dusart (vgl. Inv.-Nr. 21872). Bei der r\u00fcckseitig dargestellten Figur gingen die H\u00e4nde durch die Beschneidung verloren. M\u00f6glicherweise hielten sie einen Hut, wie in der Detailstudie oben links separat skizziert. Die Wiederholung derartiger Details ist ein h\u00e4ufiges Ph\u00e4nomen auf den Figurenstudien des K\u00fcnstlers.(Anm.2)\n\nAnnemarie Stefes\n\n1 \u201eTanzende Bauern im Wirtshaus\u201c, Prag, N\u00e1rodn\u00ed Galerie, Inv.-Nr. DO 256.\n2 Z. B. auf Inv.-Nr. 22284, 22295, 22291."
#     },
#     "images": "https:\/\/online-sammlung.hamburger-kunsthalle.de\/resources\/superImageResolution\/148036.jpg",
#     "language": "DE",
# }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer wikipedia data to a common format"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_path", help="verbose output")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    return 0


if __name__ == "__main__":
    sys.exit(main())
