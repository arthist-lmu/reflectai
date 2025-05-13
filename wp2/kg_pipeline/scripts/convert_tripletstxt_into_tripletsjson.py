import os
import json
from convert_inception import xmi_parse_helper

# Transforms the output of the TripletsPrinter into a json file

def triplettxt_totripletjson():
    # transform txt triplet file into a json triplet file
    with open('./gollie_results_of_the annotated_texts.txt', 'r', encoding='utf-8') as fp:
        trips = {}
        for line in fp.readlines():
            if line.startswith('\t'):
                i = 0
                for a in line.split(';  '):
                    if i == 3:
                        i = 0

                    if i == 0:
                        s = a
                    elif i == 1:
                        p = a
                    else:
                        o = a
                    i += 1

                triplet = (s.replace('\t ', ''), p, o.replace('\n', ''))
                trips = xmi_parse_helper(trips, triplet)

        with open(f'./gollie_resultset_of_the annoated_texts.json', 'w', encoding='utf-8') as fp:
                json.dump(trips, fp, indent=4, ensure_ascii=False)