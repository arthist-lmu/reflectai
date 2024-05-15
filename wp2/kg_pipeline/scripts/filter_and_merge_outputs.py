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

    results = {}
    for x in inputs:
        for key, value in x.items():
            if key not in results:
                results[key] = value
                continue
            
            for triplets_results_a in results[key]["triplets"]:
                for triplets_results_b in value["triplets"]:
                    if triplets_results_a["type"] == triplets_results_b["type"]:

                        triplets_results_a["content"].extend(triplets_results_b["content"])

    count = 0
    with open(args.output_path, "w") as f:
        for _,value in results.items():
            f.write(json.dumps(value)+"\n")
            for triplets in value["triplets"]:
                for triplet in triplets["content"]:
                    count +=1
    print(count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
