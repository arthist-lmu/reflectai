from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("TripletsPrinter")
class TripletsPrinterPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []

        for entry in text_entries:
            print(entry["id"])

            for triplets in entry.get("triplets", []):
                for triplet in triplets["content"]:
                    print(
                        f"\t {triplet['subject']['label']},{triplet['relation']['label']},{triplet['object']['label']}"
                    )

            yield entry

