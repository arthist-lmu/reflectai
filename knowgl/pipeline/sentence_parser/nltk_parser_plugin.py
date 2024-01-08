import nltk
from pipeline.plugin import Plugin
from pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("NLTKSentenceSplitter")
class NLTKSentenceSplitterPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nltk.download("punkt")

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        from nltk.tokenize import sent_tokenize

        results = []
        for entry in text_entries:
            sents = sent_tokenize(entry["text"])
            for i, t in enumerate(sents):
                results.append({**entry, "text": t, "sentences_nr": i})
        return results
