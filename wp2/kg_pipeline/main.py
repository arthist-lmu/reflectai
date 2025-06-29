import os
import sys
import re
import json
import argparse
from typing import List, Dict
from tqdm import tqdm
import logging


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
    parser.add_argument(
        "-k",
        "--class_name",
        action="store_true",
        help="Whether to include the class name in the triplets or not",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--prefix",
        action="store_true",
        help="Whether to put the 'Work of Art: ' prefix in front of text",
        default=False,
    )

    args = parser.parse_args()
    return args


def read_dataset(path: str, with_class_name=False, with_prefix=False) -> List[Dict]:
    results = []
    with open(path, "r") as file:
        for i, line in enumerate(file):
            data = json.loads(line)
            prefix = ""
            if with_prefix:
                prefix = "The art work is called "
            text = prefix + "; ".join(text["content"] for text in data["text"])
            results.append(
                dict(
                    id=data["id"],
                    document_index=i,
                    original_file=path,
                    text=text,
                    language=data["text"][0].get("language", None),
                    triplets=data.get("triplets", []),
                    annotations=data.get("annotations", {}),
                    with_class_name=with_class_name,
                )
            )

    return results


def read_pipeline_output(path: str) -> List[Dict]:
    results = []
    with open(path, "r") as file:
        for i, line in enumerate(file):
            data = json.loads(line)
            results.append(data)

    return results


def main():
    args = parse_args()

    datasets = []
    for path in args.input_paths:
        try:
            datasets.extend(read_dataset(path, args.class_name, args.prefix))
        except:
            logging.warning("Reading pipeline output")
            datasets.extend(read_pipeline_output(path))

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
