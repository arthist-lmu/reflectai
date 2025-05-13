from typing import List, Dict, Generator

from kg_pipeline.manager import Manager
from kg_pipeline.plugin import Plugin


default_config = {"type1": None, "type2": None}
default_parameters = {}


@Manager.export("TripletMerger")
class TripletMergerPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def call(self, text_entries: List[Dict]) -> Generator:
        for entry in text_entries:
            try:
                type1_triplets = [
                    triplets['content']
                    for triplets in entry['triplets']
                    if triplets['type'] == self.config['type1']
                ][0]
                type2_triplets = [
                    triplets['content']
                    for triplets in entry['triplets']
                    if triplets['type'] == self.config['type2']
                ][0]
            except IndexError:
                print('ERROR: Could not find type1 or type2 triplets in entry')
                print(entry)
                continue

            merged_triplets = type1_triplets[:]
            type1_triplets_str = [
                self.convert_triplet_to_str(triplet)
                for triplet in type1_triplets
            ]
            for triplet in type2_triplets:
                if self.convert_triplet_to_str(triplet) not in type1_triplets_str:
                    merged_triplets.append(triplet)

            entry['triplets'].append({
                'type': 'merged',
                'content': merged_triplets
            })

            yield entry

    def convert_triplet_to_str(self, triplet):
        return '{},{},{}'.format(
            triplet['subject']['label'],
            triplet['relation']['label'],
            triplet['object']['label']
        ).lower()
