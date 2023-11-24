import os
import sys
import re
import argparse
from transformers import pipeline


class Translator:
    def __init__(self):
        pass

    def __call__(self, text):
        pass


class NLLB200(Translator):
    def __init__(self):
        model_ckpt = "facebook/nllb-200-distilled-1.3B"
        self.pipe = pipeline(
            "translation", model=model_ckpt, src_lang="eng_Latn", tgt_lang="deu_Latn"
        )

    def __call__(self, text):
        preds = self.pipe(text)
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
    translator = NLLB200()

    print(translator(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
