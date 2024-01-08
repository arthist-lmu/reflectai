import os
import sys
import re
import argparse
from transformers import pipeline


class LanguageDetection:
    def __init__(self):
        pass

    def __call__(self, text):
        pass


class XLMRobertaBaseLanguageDetection(LanguageDetection):
    def __init__(self):
        model_ckpt = "papluca/xlm-roberta-base-language-detection"
        self.pipe = pipeline("text-classification", model=model_ckpt)

    def __call__(self, text):
        preds = self.pipe(text, return_all_scores=True, truncation=True, max_length=128)
        return preds


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
    language_detection = XLMRobertaBaseLanguageDetection()

    print(language_detection(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
