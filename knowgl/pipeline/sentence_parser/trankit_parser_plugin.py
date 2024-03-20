import nltk
from pipeline.plugin import Plugin
from pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("TrankitSentenceSplitter")
class TrankitSentenceSplitterPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from trankit import Pipeline

        self.p = Pipeline("english")
        self.p.add("german")

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:
            sents = self.p(entry["text"])["sentences"]

            for i, t in enumerate(sents):
                results.append({**entry, "text": t["text"], "sentences_index": i})

        return results
