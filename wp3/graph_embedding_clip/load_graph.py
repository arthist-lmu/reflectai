from pathlib import Path
import shutil
import zipfile

import requests
import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph


def load_artgraph():
    # info available at: https://zenodo.org/records/6337958
    url = 'https://zenodo.org/records/6337958/files/artgraph-rdf.zip?download=1'
    filename = Path('artgraph.zip')
    with requests.get(url, stream=True) as r:
        with filename.open('wb') as f:
            shutil.copyfileobj(r.raw, f)
    
    dirname = Path(filename.stem)
    with zipfile.ZipFile(filename, 'r') as zipf:
        zipf.extractall(dirname)

    filename.unlink()
    
    return dirname


def load_ttl_graph_to_nx(filename):
    graph = rdflib.Graph()
    graph = graph.parse(filename, format='ttl')
    return rdflib_to_networkx_graph(graph)


def graph_to_tsv(graph: rdflib.graph.Graph, outfile):
    # necessary for pykeen
    with Path(outfile).open('w') as f:
        for s, o, p in graph:
            s = s.replace('\n', ' ')
            o = o.replace('\n', ' ')
            p = p.replace('\n', ' ')
            f.write(f"{s}\t{o}\t{p}\n")
