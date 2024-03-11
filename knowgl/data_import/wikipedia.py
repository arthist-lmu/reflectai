import sys
import argparse
import json
import uuid

#### example input
{
    "url": "https:\/\/en.wikipedia.org\/wiki\/Scene_in_the_Northwest:_Portrait_of_John_Henry_Lefroy",
    "title": "Scene in the Northwest: Portrait of John Henry Lefroy",
    "text": {
        "entry": "Scene in the Northwest: Portrait of John Henry Lefroy, also known as The Surveyor, is a painting by Paul Kane circa 1845. It sold at auction in 2002 for C$5.1 million, making it the most expensive Canadian painting ever sold at that time. It was purchased by media magnate Ken Thomson, who donated it to the Art Gallery of Ontario. The painting depicts British explorer John Henry Lefroy on his successful expedition to map the Magnetic North Pole. Lefroy returned to Toronto in November 1844 and it is likely that Kane painted him soon after that. Lefroy helped convince George Simpson to fund Kane's own western expeditions, which Kane began in June 1845. In the painting, Lefroy is dressed in the outfit of a coureur des bois wearing snow shoes, standing in front of a dog sled. In the background one of his companions walks towards a native woman's tipi. Lefroy returned to England in 1853 and took the painting with him. The original remained in the Lefroy family for some 150 years, but they had no knowledge of the artist or its value. It was forgotten in Canada until researchers at the Library and Archives Canada and the Art Gallery of Ontario learned of its existence and located it in the possession of one of Lefroy's descendants.[1] They opted to put it up for auction in 2002. It sold at auction in February 2002 at Sotheby's Canada in Toronto for $5,062,500. The painting was appraised at $450,000 to $550,000, but a competitive auction vastly exceeded its appraised value as Thomson's agent competed with two American bidders.[2] Its sale price more than doubled the previous record for a Canadian painting\u2014$2.2 million for Lawren Harris's Baffin Island, which had been bought by Thomson the previous year. The sale price of Scene in the Northwest was almost ten times more than had ever had been paid for a Kane work; the previous record was $525,000 for Portrait of Maungwudaus in 1999.[3] While scholars had no knowledge of the original painting for over a century, a copy of the painting did remain in Canada. This version was acquired by the Glenbow Museum in Calgary in the 1950s. Its artist, and who was depicted, had been forgotten, leading to many decades of debate. Some scholars credited the Glenbow painting to Kane and others to Cornelius Krieghoff. The rediscovery of the much higher-quality original has led to the consensus opinion that it is a copy of Kane's piece done by a lesser artist of the same period. One possibility is that it was created by Kane's wife, Harriet Clench, herself a skilled painter."
    },
    "images": [
        "https:\/\/upload.wikimedia.org\/wikipedia\/commons\/2\/24\/Kane_The_Surveyor.jpg"
    ],
    "language": "EN",
}

#### example output
{
    "id": "",  # hash of the url
    "meta": {
        "url": "https:\/\/en.wikipedia.org\/wiki\/Scene_in_the_Northwest:_Portrait_of_John_Henry_Lefroy",
    },  # year, author,
    "text": [
        {
            "content": "Scene in the Northwest: Portrait of John Henry Lefroy",
            "page": 0,
            "type": "title",
            "language": "en",
        },
        {
            "content": "Scene in the Northwest: ",
            "page": 0,
            "type": "text",
            "language": "en",
        },
    ],
    "images": [
        {
            "url": "https:\/\/upload.wikimedia.org\/wikipedia\/commons\/2\/24\/Kane_The_Surveyor.jpg",
            "page": 0,
        }
    ],
}


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
