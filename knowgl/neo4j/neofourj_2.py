from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"  # Change to Neo4j instance URI
username = "neo4j"  # Change to your username
password = "leonardo"  # Change to your password

driver = GraphDatabase.driver(uri, auth=(username, password))


def add_triplet(tx, subject_label, predicate_label, object_label):
    query = (
        "MERGE (s:Resource {name: $subject}) "
        "MERGE (o:Resource {name: $object}) "
        "MERGE (s)-[r:RELATIONSHIP {name: $predicate}]->(o)"
    )
    tx.run(query, subject=subject_label, predicate=predicate_label, object=object_label)


def import_triplets(file_path):
    with driver.session() as session:
        with open(file_path, "r") as file:
            data = json.load(file)
            for idx, triplet in enumerate(data):
                try:
                    # Check if 'subject', 'relation', and 'object' keys exist
                    if (
                        "subject" in triplet
                        and "relation" in triplet
                        and "object" in triplet
                    ):
                        # Extract labels
                        subject_label = triplet["subject"]["label"]
                        predicate_label = triplet["relation"]["label"]
                        object_label = triplet["object"]["label"]

                        session.execute_write(
                            add_triplet,
                            subject_label,
                            predicate_label,
                            object_label,
                        )
                    else:
                        print(f"Missing keys in triplet at index {idx}: {triplet}")
                except KeyError as e:
                    print(f"Key error in triplet at index {idx}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing triplet at index {idx}: {e}")
                    raise


# Replace with the path to your JSONL file
import_triplets("./statements.json")

driver.close()
