from typing import List, Dict, Generator
import json
import numpy as np

from kg_pipeline.manager import Manager
from kg_pipeline.plugin import Plugin


def filter_for_actual_labels(lst, labels):
    # implement the testing for the actual testing wheter it is in the lables or not
    return lst


def remove_entry(remove, structure, subject, predicate):
    # removes the object from the triplets entry: problem it is either a list or a single object
    if type(structure[subject][predicate]) == list and len(structure[subject][predicate]) > 1:
        # remove the remove entry
        structure[subject][predicate].remove(remove)
    else:
        # remove the whole po pair
        structure[subject].pop(predicate)


default_config = {"truth": "ground_truth", "predicted": "gollie", "check": "label"}
default_parameters = {'annotation': '../test/annotation_test.json', 'gollie':'../test/gollie_test.json'}


# @Manager.export("Evaluator")
# class EvaluatorPlugin(
#     Plugin, config=default_config, parameters=default_parameters, version="0.1"
# ):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def call(self, text_entries: List[Dict]) -> Generator:
#         total_predicted = 0
#         total_truth = 0
#         total_overlap = 0
#         entry_overlap = []
#         for entry in text_entries:
#             try:
#                 truth_triplets = [
#                     triplets['content']
#                     for triplets in entry['triplets']
#                     if triplets['type'] == self.config['truth']
#                 ][0]
#                 predicted_triplets = [
#                     triplets['content']
#                     for triplets in entry['triplets']
#                     if triplets['type'] == self.config['predicted']
#                 ][0]
#             except IndexError:
#                 print('ERROR: Could not find ground truth or predicted triplets')
#                 print(entry)
#                 continue
#             total_truth += len(truth_triplets)
#             gt_triplets = [
#                 '{},{},{}'.format(
#                     triplet['subject'][self.config['check']],
#                     triplet['relation'][self.config['check']],
#                     triplet['object'][self.config['check']]
#                 ).lower()
#                 for triplet in truth_triplets
#             ]

#             predicted = 0

#             for triplet in predicted_triplets:
#                 try:
#                     triplet_str = '{},{},{}'.format(
#                         triplet['subject'][self.config['check']],
#                         triplet['relation'][self.config['check']],
#                         triplet['object'][self.config['check']]
#                     ).lower()
#                 except (AttributeError, KeyError):
#                     print('Wrong format for triplet')
#                     print(triplet)
#                     continue
#                 total_predicted += 1
#                 if triplet_str in gt_triplets:
#                     predicted += 1
#             entry_overlap.append(predicted/len(truth_triplets))
#             total_overlap += predicted

#             yield entry

#         print('Total predicted', total_predicted)
#         print('Total ground truth', total_truth)
#         print('Total overlap', total_overlap)
#         print('Mean overlap per entry', np.mean(entry_overlap))


@Manager.export("Evaluator")
class EvaluatorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> Generator:
        with open(self._parameters['annotation'], 'r', encoding='utf-8', ) as fp:
            reference = json.load(fp)
        with open(self._parameters['gollie'], 'r', encoding='utf-8', ) as fp:
            predictions = json.load(fp)
        # evaluates the correctly found subjects and predicate object pairs

        # if not len(reference) or (len(reference) and not isinstance(reference[0], list)):
        #     reference = [reference]
        # if not len(predictions) or (len(predictions) and not isinstance(predictions[0], list)):
        #     predictions = [predictions]

        # assert len(reference) == len(
        #     predictions
        # ), f"Reference ({len(reference)}) and prediction ({len(predictions)}) amount must be equal."

        # ref = filter_for_actual_labels(ref, [])
        # pre = filter_for_actual_labels(pre, [])

        s_tp = s_total_pos = s_total_pre = 0
        po_tp = po_total_pos = po_total_pre = 0

        pred_keys = predictions.keys()
        ref_keys = reference.keys()
        s_total_pre = len(pred_keys)
        s_total_pos = len(ref_keys)

        for _ , ref_po_pairs in reference.items():
            for ref_objects in ref_po_pairs.values():
                if type(ref_objects) == list:
                    po_total_pos += len(ref_objects)
                else:
                    po_total_pos += 1

        for s_pred, pred_po_pairs in predictions.items():
            if s_pred in ref_keys:
                s_tp += 1
                for predicate, objects in pred_po_pairs.items():
                    if predicate in reference[s_pred].keys():
                        if type(objects) != list:
                            objects = [objects]

                        for obj in objects:
                            po_total_pre += 1
                            if type(reference[s_pred][predicate]) == list and obj in reference[s_pred][predicate]\
                                    or obj == reference[s_pred][predicate] and type(reference[s_pred][predicate]) != list:
                                po_tp += 1
                                remove_entry(obj, reference, s_pred, predicate)

        s_precision = s_tp / s_total_pre if s_total_pre > 0.0 else 0.0
        po_precision = po_tp / po_total_pre if po_total_pre > 0.0 else 0.0
        s_recall = s_tp / s_total_pos if s_total_pos > 0.0 else 0.0
        po_recall = po_tp / po_total_pos if po_total_pos > 0.0 else 0.0
        s_f1_score = 2 * s_precision * s_recall / (s_precision + s_recall) if (s_precision + s_recall) > 0.0 else 0.0
        po_f1_score = 2 * po_precision * po_recall / (po_precision + po_recall) if (po_precision + po_recall) > 0.0 else 0.0

        print('subject F1 Score: ', s_f1_score, 'Predicate object pair F1 Score: ', po_f1_score)
        print('subject Precision: ', s_precision, 'Predicate object pair Precision: ', po_precision)
        print('subject Recall: ', s_recall, 'Predicate object pair Recall: ', po_recall)

        print(text_entries)
        yield text_entries

