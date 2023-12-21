from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"  # Change to Neo4j instance URI
username = "neo4j"             # Change to your username
password = "password"          # Change to your password

driver = GraphDatabase.driver(uri, auth=(username, password))

def add_triplet(tx, subject, predicate, object):
    query = (
        "MERGE (s:Resource {name: $subject}) "
        "MERGE (o:Resource {name: $object}) "
        "MERGE (s)-[r:RELATIONSHIP {name: $predicate}]->(o)"
    )
    tx.run(query, subject=subject, predicate=predicate, object=object)

def import_triplets(file_path):
    with driver.session() as session:
        with open(file_path, 'r') as file:
            for line in file:
                triplet = json.loads(line)
                session.write_transaction(add_triplet, triplet['subject'], triplet['predicate'], triplet['object'])

# Replace
import_triplets('path/to/your/file.jsonl')

driver.close()
