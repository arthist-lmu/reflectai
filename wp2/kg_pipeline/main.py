import os
import sys
import re
import json
import argparse
from typing import List, Dict
from tqdm import tqdm


from kg_pipeline.manager import Manager

from output import OutputWrapper


def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_paths", nargs="+", help="path to input files")
    parser.add_argument("-o", "--output_path", help="path to the output file")
    parser.add_argument("-c", "--cache_path", help="path to a cache folder")
    parser.add_argument("-p", "--pipeline", help="pipeline definition input")
    parser.add_argument(
        "-n", "--number", type=int, help="number of samples selected from the dataset"
    )
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
            text = '; '.join(text['content'] for text in data['text'])
            results.append(
                dict(
                    id=data["id"],
                    document_index=i,
                    original_file=path,
                    text=text,
                    language=data['text'][0].get("language", None),
                )
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
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils"),            
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "reconciliation"),

        ]
    )

    if args.number:
        datasets = datasets[: args.number]

    if args.output_path:
        os.makedirs(args.output_path, exist_ok=True)

    for p in pipeline_definition:
        print("################################")
        print(p["plugin"])
        plugin = manager.build_plugin(p["plugin"], p.get("config", {}))
        if args.output_path:
            plugin = OutputWrapper(
                plugin, {"output_path": args.output_path, "format": "json"}
            )
        new_datasets = []
        plugin_iterator = plugin(datasets)
        

        for x in tqdm(plugin_iterator):
            new_datasets.append(x)
            
        datasets = new_datasets
    return 0


if __name__ == "__main__":
    sys.exit(main())
