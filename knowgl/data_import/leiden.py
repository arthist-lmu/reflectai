import sys
import argparse


# {
#     "url": "https:\/\/www.theleidencollection.com\/artwork\/man-tuning-a-violin\/",
#     "title": "Man Tuning a Violin",
#     "text": {
#         "entry": "Paintings of musicians, either playing or tuning an instrument, were extremely popular in the Dutch Republic, a testament to the appeal of music in that culture, particularly among the upper classes. Here, a young man dressed in a fancy black satin cloak listens intently to the sounds of the violin he is tuning, the half-smile on his face indicating that he is pleased with the results. He is seated in an elegant but dimly lit interior with monumental pilasters, one of which is just behind him. A large roemer, conspicuously filled with white wine, is on the table in front of him, as are two well-worn portfolios, probably containing sheet music, and a large red velvet cap with a green feather. Also on the table is a thick tome with finger indexing on the pages, indicating that the young man\u2019s dedication to music is only one aspect of his scholarly concerns. Paintings of musicians also evoked associations with harmony and love, ones frequently expressed in the poetry and emblem books of the period. For example, Jacob Cats (1577\u20131660), in his Sinne- en Minnebeelden of 1618, wrote a poem accompanying an illustration of a man tuning his lute (fig 1)\u00a0that describes this activity as symbolic of two hearts \u201cthat vibrate to the same tune.\u201d1 Throughout his career, Frans van Mieris excelled in rendering different types of materials, including, as in this instance, glass, marble, and the fabric of the cloak and cap. This remarkable ability was one reason he achieved such inordinate fame during his lifetime. He often utilized this skill to emulate reality, sometimes also creating trompe l\u2019oeil images that deceive the eye into believing that a\u00a0painted image is\u00a0reality itself.2 During\u00a0the latter part of his career, however, at the time he painted this work, Van Mieris\u2019s art had become slicker and harder. He no longer sought to create the semblance of reality, but used his touch to create engaging but artificial images. Rhythmic accents that play across his fabrics bring energy and color to his paintings, but do not deceive the viewer into thinking them real. He also began to exaggerate expressions, as in the upward glance and half smile enlivening this young man\u2019s face. The exaggerated bend of the man\u2019s left arm, which neatly echoes one of the highlighted folds of the man\u2019s shimmering cloak, may have been a deliberate attempt to convey elegance and refinement, as he uses this sweeping gesture in some of his other late paintings.3\u00a0This attitude may have its roots in the manuals of civility that were published in the Dutch Republic during the seventeenth century.4\u00a0These codes of manners were called welstand, a word that refers to proper manners in the French tradition. One of the most popular French etiquette guides, Antoine de Courtin\u2019s Suite de la civilit\u00e9 fran\u00e7aise of 1671, was translated into Dutch the following year.5 The large roemer filled with wine brings to mind Van Mieris\u2019s documented alcohol abuse, which seems to have caused his affairs\u00a0to unravel rapidly in the last years of his life. In a letter dated 1675, one of Van Mieris\u2019s patrons wrote that Cunera van der Cock, the artist\u2019s wife, requested that some of the fee Van Mieris was owed for a painting be paid directly to her, without her husband\u2019s knowledge, because the money would otherwise disappear \u201clike acid on an etching plate.\u201d6\u00a0It is not impossible that the artist, who is known to have had a great sense of humor, even alluded to his drinking problems in this work by including the large roemer. Technical research has determined that Van Mieris reused an existing panel in painting this work (fig 2). When turned upside down, an X-radiograph of the painting shows a knee-length portrait of a lady, just as in Woman with a Lapdog, Accompanied by a Maidservant, also from 1680 (see FM-105). Less pronounced, but clearly visible on the X-radiograph, is a rectangular shape in the same position as the letter in Woman with a Lapdog.7\u00a0Probably Van Mieris started another version of that painting, but changed his mind and reused the panel for the present work.8\u00a0The subject of a figure tuning a string instrument had already been introduced by the artist as early as 1665 in the Rijksmuseum\u2019s A Woman Tuning a Theorbo, with a Company in the Background\u00a0(fig 3). This painting, which is almost the same size as Man Tuning a Violin, was once thought to have also been executed in 1680.9"
#     },
#     "images": [
#         "https:\/\/www.theleidencollection.com\/wp-content\/uploads\/2018\/03\/FM-111-Frans-van-Mieris-A-Man-Tuning-a-Violin.jpg",
#         "https:\/\/www.theleidencollection.com\/wp-content\/uploads\/2018\/03\/Cats-QuidNonSentitAmor.jpg",
#         "https:\/\/www.theleidencollection.com\/wp-content\/uploads\/2018\/03\/MierisFv_WomanTuningTherbo_Rijksmuseum_SK-A-262-13-1.jpg",
#         "https:\/\/www.theleidencollection.com\/wp-content\/uploads\/2018\/03\/FM-111_1831x2302_acf_cropped.jpg",
#     ],
#     "language": "EN",
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
