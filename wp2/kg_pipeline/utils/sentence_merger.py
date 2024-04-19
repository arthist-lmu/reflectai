from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
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

        result = {**text_entries[0], "text": text}

        if "triplets" in text_entries[0]:
            new_triplets = {}
            for entry in text_entries:
                for triplets in entry["triplets"]:
                    if triplets["type"] not in new_triplets:
                        new_triplets[triplets["type"]] = []
                    new_triplets[triplets["type"]].extend(triplets["content"])

            result["triplets"] = []
            for key, value in new_triplets.items():
                result["triplets"].append({"type": key, "content": value})

        return result

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
