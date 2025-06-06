from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict
import pandas as pd
import re

default_config = {}
default_parameters = {}


@Manager.export("TripletsPrinter")
class TripletsPrinterPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        total_triplets = 0
        try:
            save_txt = self._config["save_txt"]
        except KeyError:
            save_txt = '../test/gollie_testset/resultset.txt'
        
        try:
            save_csv = self._config["save_csv"]
        except KeyError:
            save_csv = '../test/gollie_testset/number_of_found_triplets.csv'

        
        dct = {}
        for entry in text_entries:
            try:
                end = re.search('^.*\n\n', entry['text']).end()
                match = entry['text'][:end-2]
            except (TypeError, AttributeError):
                match = entry["id"]
            
            with open(save_txt, 'a') as fp:
                print(f'{match}:', 'number of found triplets: ', len(entry['triplets'][0]["content"]))
                total_triplets += len(entry['triplets'][0]["content"])
                dct.update({match: len(entry['triplets'][0]["content"])})

                fp.write(match + '\n')
                for triplets in entry.get("triplets", []):   
                    for triplet in triplets["content"]:
                        print(
                            f"{match}\t {triplet['subject']['label']},{triplet['relation']['label']},{triplet['object']['label']}"
                        )
                    print()
                 
            yield entry

        dct.update({'total': total_triplets})
        pd.DataFrame.from_dict(dct, orient='index', columns=['Number of found Triplets'], ).to_csv(save_csv)

