import copy
import json
from typing import List, Dict

import spacy
import glirel

from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager


default_config = {}
default_parameters = {}

#TODO: some relations are returned multiple times by the model

@Manager.export("Glirel")
class GlirelPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nlppipe = spacy.load('en_core_web_sm')
        self.nlppipe.add_pipe("glirel", after="ner")
        self.nlp = spacy.load('en_core_web_sm')

        # check labels and meaning via:
        #   for label in nlp.get_pipe("ner").labels:
        #       print(label, end=': ')
        #       spacy.explain(x)
        self.labels = {"glirel_labels": {
            "main subject": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['FAC', 'PRODUCT', 'EVENT', 'PERSON', 'LOC', 'GPE']
            },
            "genre": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['PRODUCT']
            },
            "creator": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['PERSON']
            },
            "located in": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['GPE', 'FAC', 'LOC', 'ORG']
            },
            "made from material": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['PRODUCT']
            },
            "location of creation": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['GPE', 'FAC', 'LOC']
            },
            "movement": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['PRODUCT']
            },
            "alias": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['WORK_OF_ART']
            },
            "description": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['FAC', 'PRODUCT', 'EVENT', 'PERSON', 'LOC', 'GPE']
            },
            "language": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['LANGUAGE']
            },
            "inception": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['DATE']
            },
            "shown with features": {
                "allowed_head": ['WORK_OF_ART',
                    'FAC', 'PRODUCT', 'EVENT', 'PERSON'], "allowed_tail": ['FAC', 'PRODUCT', 'EVENT']
            },
            "depicts": {
                "allowed_head": ['WORK_OF_ART'],
                "allowed_tail": ['FAC', 'PRODUCT', 'EVENT', 'PERSON', 'LOC', 'GPE']
            },
            }
        }

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        for entry in text_entries:
            docs = list(self.nlppipe.pipe([(entry['text'], self.labels)], as_tuples=True))
            doc = self.nlp(entry['text'])
            relations = docs[0][0]._.relations

            def relation_to_text(rel, doc):
                return doc.text[doc[rel[0]].idx:(doc[rel[1]-1].idx+len(doc[rel[1]-1]))]

            relation_wikidata = {
                "main subject": "wdt:P921",
                "genre": None,
                "creator": "wdt:P170",
                "located in": "wdt:P276",
                "made from material": "wdt:P186",
                "location of creation": "wdt:P1071",
                "movement": "wdt:P135",
                "alias": None,
                "description": "schema:description",
                "language": None,
                "inception": "wdt:P571",
                "shown with features": "wdt:P1354",
                "depicts": "wdt:P180",
            }

            triplets = [
                {'subject': {'label': relation_to_text(relation['head_pos'], doc)},
                 'object': {'label': relation_to_text(relation['tail_pos'], doc)},
                 'relation': {
                     'label': relation['label'],
                     'wikidata_id': relation_wikidata.get(relation['label'])
                 }}
                for relation in relations
#               if relation['score'] > 0.7
            ]

            entry["triplets"].append({"type": "glirel", "content": triplets})
            yield entry
