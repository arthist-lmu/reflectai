import csv
import json

"""
Convert via survey tool created annotations into our data set jsonl format.
"""


def read_file(path):
    with open(path) as f:
        reader = csv.DictReader(f, delimiter=';')
        return [line for line in reader]


def get_wikipedia_text(url):
    import wikipediaapi

    lang = url.removeprefix('https://')[:2]
    title = url.split('/')[-1]
    wiki_wiki = wikipediaapi.Wikipedia("ReflectAI/0.1 (elias.entrup@tib.eu)", lang)
    page = wiki_wiki.page(title)
    return page.text


def get_tate_text(url):
    import requests

    key = url.split('-')[-1].upper()
    url = f'https://www.tate.org.uk/api/v2/artworks/?acno={key}&fields=*'
    r = requests.get(url)
    return r.json()['items'][0]['resources'][0]['content']


def get_leiden_text(url):
    import requests
    from bs4 import BeautifulSoup

    r = requests.get(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    )
    root = BeautifulSoup(r.content)
    return root.find_all('div', class_='entry-content')[0].text


def fetch_text(url):
    if 'wikipedia.org' in url:
        return get_wikipedia_text(url)
    elif 'theleidencollection.com' in url:
        return get_leiden_text(url)
    elif 'tate.org.uk' in url:
        return get_tate_text(url)
    else:
        print('ERROR')


def convert(item):
    url = item.pop('URL – A004x01')
    title = item.pop('Title – A021x01')

    triplets = []
    for key in item.keys():
        if '–' not in key or not item[key]:
            continue

        relation = key.split(' - ')[0]
        if 'Depicts' in relation:
            relation = 'Depicts'

        triplets.append({
            'subject': {'label': title},
            'relation': {'label': relation},
            'object': {'label': item[key].strip()},
        })

    if len(triplets) == 0 or not url:
        return

    language = 'en'
    if 'https://de.w' in url:
        language = 'de'

    return {
        "triplets": triplets,
        "id": url,
        "text": {
            "content": fetch_text(url),
            "language": language
        }
    }


def write_file(items, path):
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(item) + '\n')


if __name__ == '__main__':
    items = read_file('data_triple_evaluation_2024-06-10_14-17.csv')
    items = [convert(item) for item in items]
    items = [item for item in items if item is not None]
    write_file(items, 'manual_test_set.jsonl')
