import sys
import argparse
import json
import uuid

# {
#     "url": "https://www.tate.org.uk/art/artworks/zoffany-three-sons-of-john-3rd-earl-of-bute-t07863",
#     "title": "Three Sons of John, 3rd Earl of Bute",
#     "text": {
#         "entry": "John Stuart, 3rd Earl of Bute, commissioned this portrait of three of his sons as a pair with one of three of his daughters (Tate T07864). It was painted not long after Zoffany had left his native Germany for England in 1760. Zoffany quickly established himself in London as the leading painter of lively conversation pieces such as this, which were greatly admired for their charming informality.\nIn his portraits of the Three Sons and Three Daughters of Lord Bute, the only known pair of portraits of children by Zoffany, the artist stresses the playful and mischievous aspect of childhood, yet succeeds in capturing the youngsters’ charm without undue sentiment.\nThe Earl of Bute was one of Zoffany’s earliest and most important patrons. As well as this portrait and its pair, he commissioned a full-length of his heir, John, Lord Mountstuart, later 1st Marquess of Bute, in Masquerade Dress c.1763-4 (private collection). The 3rd Earl was a great patron of the arts and formed an important collection, including paintings, prints and books. He was best-known as a close advisor and later favourite Prime Minister (1762–3) to the young King George III, although he resigned from that position in 1763, at around the time the Bute portraits were painted. Nevertheless, he remained one of the most powerful aristocrats in Britain. It was probably Lord Bute who, following this commission, introduced Zoffany to the King and Queen, initiating a highly successful period of Royal patronage for the artist.\nIn this animated portrait the three younger sons of the Earl have abandoned their archery in favour of birdnesting. On the left is the Hon. William Stuart (1755–1822) who reaches up to his brother to collect the bird and eggs in his black tricorn hat. The Hon. Charles Stuart (1753–1801) sits rather precariously up in the branches of the oak as he raids the nest. To the right is the Hon. Frederick Stuart (1751–1802) who clutches his bow and proudly points to the bull’s eye he has just scored on the distant target. William and Charles went on to have illustrious public careers: William subsequently became Archbishop of Armagh, while Charles was later made Lieutenant-General the Hon. Sir Charles Stuart, who captured Minorca from the Spaniards in 1798.\nThe compositions of both pendant portraits are carefully contrived geometric designs. Here, the pyramidal arrangement complements the diagonal composition used for the sisters’ portrait, who are shown playing with pet squirrels. The landscape setting for both paintings is the park at Luton Hoo, Bedfordshire, which had become the Bute family seat in 1763. The artist has paid close attention to detail and texture, particularly in the delicate foliage, the gnarled trunk of the tree and in the treatment of the poodle, which waits in hope for the spoils of the boys’ sport. The two paintings mark the beginning of a more sophisticated approach by Zoffany to group portraiture, the figures being given prominence over the landscape setting. The Bute portraits can be compared with the slightly earlier pair of conversation pieces that Zoffany produced for his other important patron, the actor David Garrick, both entitled Mr and Mrs Garrick at Hampton Gardens 1762 (Lord Lambton), in which the smaller, less assured figures are placed in more expansive landscapes.\nAll six children in the portraits are treated in a lively and affectionate manner with convincing personalities. Comparable earlier eighteenth-century images of children tended to be more stiff and formal, emphasising their dynastic importance in maintaining an aristocratic lineage, rather than their individual natures. Zoffany’s portraits of children anticipated a change in attitude towards children, who were beginning to be seen in a more sentimental light, in keeping with contemporary notions of sensibility. Zoffany’s ability to capture their energy and individuality can be seen in several of his portraits of children, including those of the royal family (Royal Collection). He seems to have had a genuine sympathy with children and their games and amusements that gives an attractive sincerity to his pictures of them.\n\nFurther reading\nLady Victoria Manners and G.C. Williamson, Johan Zoffany R.A. His Life and Works 1735–1810, 1920, p.186.Sacheverell Sitwell, Conversation Pieces, London 1936, p.39, reproduced pl. 48.Mary Webster, Johan Zoffany 1733–1810, exhibition catalogue, National Portrait Gallery, London 1977, no.20, reproduced.\nDiane PerkinsNovember 2003"
#     },
#     "images": ["https://www.tate.org.uk/art/images/work/T/T07/T07863_10.jpg"],
#     "language": "EN",
# }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transfer rijksmuseum data to a common format"
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
