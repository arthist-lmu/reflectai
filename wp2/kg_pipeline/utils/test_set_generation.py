import json
import time
from pathlib import Path

import ollama
import requests
from tqdm import tqdm

SPARQL_URL = 'https://query.wikidata.org/sparql'


def run_query(query):
    """Run SPARQL query against SPARLQ_URL API and return results."""
    header = {"User-Agent": "ArtMetaData/0.0 (elias.entrup@tib.eu)"}
    r = requests.get(
        SPARQL_URL,
        params={"format": "json", "query": query},
        headers=header
    )
    try:
        data = r.json()
    except json.JSONDecodeError:
        print('Exception fetching query from wikidata')
        print('Query: ', query)
        print('Response: ', r.content)
        time.sleep(10)
    time.sleep(1)
    return [statement for statement in data["results"]["bindings"]]


def get_art():
    """Get Wikidata ID and label of all art pieces."""
    query = """
        SELECT ?item ?label WHERE {
            {?item wdt:P279 wd:Q4502142 .}
            UNION {?item wdt:P279 wd:Q15709879 .}

            ?item rdfs:label ?label .
            FILTER (lang(?label) = "en") .

            FILTER (?label not in ("comics"@en, "album"@en)) .
            FILTER(!CONTAINS(LCASE(?label), "film"@en)) .
            FILTER(!CONTAINS(LCASE(?label), "doodle"@en)) .
        }
    """
    categories = [
        {'wikidata_id': category['item']['value'].rsplit('/')[-1],
         'label': category['label']['value']}
        for category in run_query(query)
    ]

    query = """
        SELECT ?item ?label WHERE {{
            {{?item wdt:P31 wd:{} .}}
            ?item rdfs:label ?label .
            FILTER (lang(?label) = "en") .
        }}
    """
    return [
        {
            'wikidata_id': piece['item']['value'].rsplit('/')[-1],
            'label': piece['label']['value'],
        }
        for category in categories
        for piece in run_query(query.format(category['wikidata_id']))
    ]


def get_relations(entity):
    """Get all relevant wikidata triplets for an art piece."""
    query = """
        SELECT ?wd ?wdLabel ?ps_Label ?ps_ WHERE {{
        VALUES ?item {{
            wd:{}
        }}
        ?item ?p ?statement.
        ?statement ?ps ?ps_.
        ?wd wikibase:claim ?p;
            wikibase:statementProperty ?ps.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
    """.format(entity['wikidata_id'])

    relations = ["P1354", "P276",  "P921", "P31", "P3828", "P6022", "P180",
                 "P135", "P186", "P170", "P1071", "P571"]

    return [
        {
            'subject': entity,
            'relation': {'wikidata_id': relation['wd']['value'].split('/')[-1],
                         'label': relation['wdLabel']['value']},
            'object': {'wikidata_id': relation['ps_']['value'].split('/')[-1],
                       'label': relation['ps_Label']['value']},
        }
        for relation in run_query(query)
        if relation['wd']['value'].split('/')[-1] in relations
    ]


def get_all_triplets():
    """Load all art pieces and their triplets from Wikidata."""
    pieces = get_art()
    return [
        {
            'subject': piece,
            'triplets': [{'type': 'ground_truth', 'content': get_relations(piece)}],
            'id': 'subject_' + piece['wikidata_id']
        }
        for piece in pieces
    ]


def generate_text(artpiece, model='mistral'):
    """Generate a description of an art piece with LLM based on triplets."""
    triplets_str = '- ' + '\n- '.join([
        t['relation']['label'] + ', ' + t['object']['label']
        for t in artpiece['triplets'][0]['content']
    ])
    prompt = """
    A piece of art called "{}" is described by the following triplets:
    {}
    Write a short description of the art piece which contains only this information
    """.format(artpiece['subject']['label'], triplets_str).replace('    ', '')
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt
    },
    ])
    return response['message']['content']


def main(filename=Path('test_set.jsonl')):
    if not filename.exists():
        print('Loading data from Wikidata')
        arts = get_all_triplets()
        with filename.open('w') as f:
            for art in arts:
                f.write(json.dumps(art) + '\n')
    else:
        with filename.open() as f:
            arts = [json.loads(l) for l in f]

    print('Generating text')
    for art in tqdm(arts):
        art['text'] = [{'content': generate_text(art), 'language': 'en'}]


    with filename.open('w') as f:
        for art in arts:
            f.write(json.dumps(art) + '\n')

    return arts


if __name__ == '__main__':
    main()
