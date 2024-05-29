import os
import sys
import re
import json
import argparse
from typing import List, Dict
from tqdm import tqdm
import hashlib

def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_paths", nargs="+", help="path to input files")
    parser.add_argument("-o", "--output_path", help="path to the output file")
    args = parser.parse_args()
    return args


def read_input_path(path: str) -> List[Dict]:
    results = {}
    with open(path, "r") as file:
        for i, line in enumerate(file):
            data = json.loads(line)
            entry_hash = hashlib.sha256(json.dumps({"id":data["id"], "document_index": data["document_index"], "entry_index": data["entry_index"]}).encode()).hexdigest()
            
            results[entry_hash] = data
    return results


def main():
    args = parse_args()

    inputs = []
    for input_path in args.input_paths:
        inputs.append(read_input_path(input_path))

    import nltk
    from trankit import Pipeline

    p = Pipeline("english")
    p.add("german")

    with open(args.output_path, "w") as f:
        for x in inputs:
            for _, entry in x.items():
                sents = p(entry["text"])["sentences"]

                for i, t in enumerate(sents):
                    f.write(t["text"]+"\n")
                    print(f"I: {i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
