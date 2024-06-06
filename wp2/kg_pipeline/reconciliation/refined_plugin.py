from typing import Generator

import numpy as np
from refined.inference.processor import Refined

from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager


default_config = {}
default_parameters = {}


# https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
def levenshtein_distance(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


@Manager.export("Refined")
class RefinedPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers', entity_set="wikipedia")

    @staticmethod
    def match_refined(spans: list[list], label:str):
        distances = []
        for span in spans:
            distance = levenshtein_distance(span.text, label)
            distances.append(distance)

        lowest_ind = np.argmin(distances)

        return distances[lowest_ind], spans[lowest_ind]

    def call(self, text_entries: list[dict]) -> Generator[dict,None,None]:
        for entry in text_entries:
            
            spans = self.refined.process_text(entry["text"])

            for triplets in entry["triplets"]:
                for triplet in triplets["content"]:
                    if 'wikidata_id' in triplet["subject"]:
                        continue
                    sub = triplet["subject"]["label"]
                    obj = triplet["object"]["label"]

                    _, sub_match = self.match_refined(spans, str(sub))
                    _, obj_match = self.match_refined(spans, str(obj))

                    if sub_match.predicted_entity and sub_match.predicted_entity.wikidata_entity_id:
                        triplet['subject']['wikidata_label'] = sub_match.predicted_entity.wikipedia_entity_title
                        triplet['subject']['wikidata_id'] = "wd:" + sub_match.predicted_entity.wikidata_entity_id

                    else:
                        triplet['wikidata_label'] = None
                        triplet['wikidata_id'] = None

                    if obj_match.predicted_entity and obj_match.predicted_entity.wikidata_entity_id:
                        triplet['object']['wikidata_label'] = obj_match.predicted_entity.wikipedia_entity_title
                        triplet['object']['wikidata_id'] = "wd:" + obj_match.predicted_entity.wikidata_entity_id
                    else:
                        triplet['object']['wikidata_label'] = None
                        triplet['object']['wikidata_id'] = None

            yield entry
