import spacy
from pipeline.plugin import Plugin
from pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("SpacySentenceSplitter")
class SpacySentenceSplitterPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nlp = spacy.load("en_core_web_sm")

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:
            doc = self.nlp(entry["text"])
            for i, t in enumerate(doc.sents):
                results.append({**entry, "text": t.text, "sentences_nr": i})
        return results
