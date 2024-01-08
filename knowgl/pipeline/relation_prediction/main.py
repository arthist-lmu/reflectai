import os
import sys
import re
import argparse
import torch
from transformers import AutoTokenizer, AutoModel
from fastcoref import FCoref, spacy_component
import spacy


class CoreferenceResolution:
    def __init__(self):
        pass

    def __call__(self, text):
        pass


class FCoref(CoreferenceResolution):
    def __init__(self):
        # device = "gpu" if torch.cuda.is_available() else "cpu"
        # self.tokenizer = AutoTokenizer.from_pretrained("biu-nlp/f-coref")
        # self.model = AutoModel.from_pretrained("biu-nlp/f-coref")

        # self.model = FCoref(device=device)

        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("fastcoref")

    def __call__(self, text):
        doc = self.nlp(  # for multiple texts use nlp.pipe
            text, component_cfg={"fastcoref": {"resolve_text": True}}
        )

        # input_data = self.tokenizer(text, return_tensors="pt")
        # print(input_data)
        # preds = self.model(**input_data)
        return doc._.resolved_text


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
    coreference_resolution = FCoref()

    print(coreference_resolution(args.text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
