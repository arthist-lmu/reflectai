from typing import List, Dict, Generator

import numpy as np

from kg_pipeline.manager import Manager
from kg_pipeline.plugin import Plugin


default_config = {"truth": "ground_truth", "predicted": "gollie"}
default_parameters = {}


@Manager.export("Evaluator")
class EvaluatorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> Generator:
        total_predicted = 0
        total_truth = 0
        total_overlap = 0
        entry_overlap = []
        for entry in text_entries:
            try:
                truth_triplets = [
                    triplets['content']
                    for triplets in entry['triplets']
                    if triplets['type'] == self.config['truth']
                ][0]
                predicted_triplets = [
                    triplets['content']
                    for triplets in entry['triplets']
                    if triplets['type'] == self.config['predicted']
                ][0]
            except IndexError:
                print('ERROR: Could not find ground truth or predicted triplets')
                print(entry)
                continue
            total_truth += len(truth_triplets)
            gt_triplets = [
                '{},{},{}'.format(
                    triplet['subject']['label'].lower(),
                    triplet['relation']['label'].lower(),
                    triplet['object']['label'].lower()
                )
                for triplet in truth_triplets
            ]

            predicted = 0

            for triplet in predicted_triplets:
                total_predicted += 1
                try:
                    triplet_str = '{},{},{}'.format(
                        triplet['subject']['label'].lower(),
                        triplet['relation']['label'].lower(),
                        triplet['object']['label'].lower()
                    )
                except AttributeError:
                    print('Wrong format for triplet')
                    print(triplet)
                    continue
                if triplet_str in gt_triplets:
                    predicted += 1
            entry_overlap.append(predicted/len(truth_triplets))
            total_overlap += predicted

            yield entry

        print('Total predicted', total_predicted)
        print('Total ground truth', total_truth)
        print('Total overlap', total_overlap)
        print('Mean overlap per entry', np.mean(entry_overlap))
