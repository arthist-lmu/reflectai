from typing import List, Dict, Generator
import json
from kg_pipeline.manager import Manager

from difflib import SequenceMatcher
from kg_pipeline.plugin import Plugin

import logging
import hashlib


def flat_dict(data_dict, parse_json=False):
    result_map = {}
    for k, v in data_dict.items():
        if isinstance(v, dict):
            embedded = flat_dict(v)
            for s_k, s_v in embedded.items():
                s_k = f"{k}.{s_k}"
                if s_k in result_map:
                    logging.error(f"flat_dict: {s_k} alread exist in output dict")

                result_map[s_k] = s_v
            continue

        if k not in result_map:
            result_map[k] = []
        result_map[k] = v
    return result_map


def get_hash_for_dict(data):

    dict_hash = hashlib.sha256(json.dumps(flat_dict(data)).encode()).hexdigest()

    return dict_hash


class LevenshteinMatcher:
    def __init__(self, threshold):
        self.threshold = threshold

    def __call__(self, pred_string, gt_strig, t):

        ratio = SequenceMatcher(
            lambda x: x == " ", pred_string.lower(), gt_strig.lower()
        ).ratio()
        if ratio > self.threshold:  # assuming that the string are similar enough
            return True

        return False


class ExactMatcher:
    def __init__(self):
        pass

    def __call__(self, pred_string, gt_strig, t):
        return pred_string.lower() == gt_strig.lower()


default_config = {}
default_parameters = {}


@Manager.export("EvaluatorMatthias")
class EvaluatorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def convert_annotation_to_triplets(self, data):
        triplets = []
        annotations = data.get("annotations")

        for sub, rel in annotations.items():
            for prop, obj in rel.items():
                if prop == "s_class_name":
                    continue
                if isinstance(obj[0], list):
                    for i, obj_i in enumerate(obj[0]):
                        triplets.append(
                            {
                                "subject": {"label": sub},
                                "relation": {
                                    "label": prop,
                                    "wikidata_id": "wdt:P180",
                                },
                                "object": {"label": obj_i},
                                "class_name": obj[1]["o_class_name"][i],
                            }
                        )
                else:
                    triplets.append(
                        {
                            "subject": {"label": sub},
                            "relation": {
                                "label": prop,
                                "wikidata_id": "wdt:P180",
                            },
                            "object": {"label": obj[0]},
                            "class_name": obj[1]["o_class_name"],
                        }
                    )

        return triplets

    def triplets_to_plain_list(self, triplets):
        for x in triplets:
            yield x["subject"]["label"], x["relation"]["label"], x["object"]["label"]

    def evaluate_triplet_match(self, pred_triplets, gt_triplets, comp=None):
        if comp is None:
            comp = ExactMatcher()

        gt_lut = {}
        pred_lut = set()
        total_pred = 0
        for s, p, o in self.triplets_to_plain_list(pred_triplets):

            for gt_s, gt_p, gt_o in self.triplets_to_plain_list(gt_triplets):
                gt_dict = {"s": gt_s, "p": gt_p, "o": gt_o}
                gt_hash = get_hash_for_dict(gt_dict)
                gt_lut.setdefault(gt_hash, {"count": 0, "data": gt_dict})
                if (
                    comp(s, gt_s, "subject")
                    and comp(p, gt_p, "prop")
                    and comp(o, gt_o, "object")
                ):
                    gt_lut[gt_hash]["count"] += 1

                    # check if we already match this prediction and only count the first prediction
                    if gt_hash not in pred_lut:
                        pred_lut.add(gt_hash)
                        total_pred += 1

                else:
                    total_pred += 1

        total_gt = len(gt_lut)
        total_matched = len([x for x in gt_lut.values() if x["count"] > 0])

        return total_matched, total_gt, total_pred

    def call(self, text_entries: List[Dict]) -> Generator:
        total_matched_all = 0
        total_gt_all = 0
        total_pred_all = 0
        for x in text_entries:
            gt_triplets = self.convert_annotation_to_triplets(x)
            total_matched, total_gt, total_pred = self.evaluate_triplet_match(
                pred_triplets=x["triplets"][0]["content"],
                gt_triplets=gt_triplets,
                comp=LevenshteinMatcher(0.5),
            )
            total_matched_all += total_matched
            total_gt_all += total_gt
            total_pred_all += total_pred
            yield x

        precision = total_matched_all / total_pred_all
        recall = total_matched_all / total_gt_all
        print("Precision: ", precision)
        print("Recall: ", recall)
