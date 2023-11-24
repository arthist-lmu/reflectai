import os
import sys
import re
import argparse
import spacy


class SentenceParser:
    def __init__(self):
        pass

    def __call__(self, text):
        pass


class SpacyParser(SentenceParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def __call__(self, text):
        doc = self.nlp(text)
        return list(doc.sents)


def parse_args():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument(
        "-t", "--text", required=True, help="text for language detection"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    parser = SpacyParser()

    print(parser(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
