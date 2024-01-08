import os
import sys
import re
import json
import argparse
from typing import List, Dict


from .manager import Manager


def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_paths", nargs="+", help="path to input files")
    parser.add_argument("-o", "--output_path", help="path to the output file")
    parser.add_argument("-p", "--pipeline", help="pipeline definition input")
    parser.add_argument(
        "-t", "--tmp_path", help="save single step results in a tmp folder"
    )
    args = parser.parse_args()
    return args


def read_dataset(path: str) -> List[Dict]:
    results = []
    with open(path, "r") as file:
        for i, line in enumerate(file):
            data = json.loads(line)
            results.append(
                dict(original_file=path, text=data["text"]["entry"], document=i)
            )

    return results


def main():
    args = parse_args()

    datasets = []
    for path in args.input_paths:
        datasets.extend(read_dataset(path))

    pipeline_definition = json.loads(args.pipeline)

    manager = Manager(
        [
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "coreference_resolution"
            ),
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "language_detection"
            ),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "sentence_parser"),
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "relation_prediction"
            ),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "translation"),
        ]
    )

    datasets = datasets[:1]

    for p in pipeline_definition:
        plugin = manager.build_plugin(p["plugin"])
        new_datasets = plugin(datasets)
        datasets = new_datasets
        print(new_datasets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
