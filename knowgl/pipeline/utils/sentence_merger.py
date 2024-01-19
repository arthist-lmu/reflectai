from pipeline.plugin import Plugin
from pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("SentenceMerger")
class SentenceMergerPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def merge_sentence_list(self, text_entries: List[Dict]) -> Dict:
        text = " ".join(x["text"] for x in text_entries)

        return {**text_entries[0], "text": text}

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []

        doc_cache = None
        current_document_id = -1
        for entry in text_entries:
            if entry["document"] != current_document_id:
                if doc_cache is not None:
                    results.append(self.merge_sentece_list(doc_cache))
                doc_cache = []

            doc_cache.append(entry)

            if doc_cache is not None:
                results.append(self.merge_sentece_list(doc_cache))

        return results
