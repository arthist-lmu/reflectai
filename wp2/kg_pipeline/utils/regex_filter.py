from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {"field": "", "filter": ".*"}


@Manager.export("RegexFilter")
class RegexFilterPlugin(
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
        current_document_index = -1
        current_entry_index = -1

        for entry in text_entries:

            if (
                entry["document_index"] != current_document_index
                or entry["entry_index"] != current_entry_index
            ):
                if doc_cache is not None:

                    results.append(self.merge_sentence_list(doc_cache))

                current_document_index = entry["document_index"]
                current_entry_index = entry["entry_index"]
                doc_cache = []

            doc_cache.append(entry)

        if doc_cache is not None:
            results.append(self.merge_sentence_list(doc_cache))

        return results
