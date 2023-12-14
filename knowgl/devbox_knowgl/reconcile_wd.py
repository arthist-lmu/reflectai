
import json

file_path = "statements.json"

with open(file_path, "r") as file:
    statements = json.load(file)


import requests


def get_wikidata_id(label, type_id=None):
    if type_id:
        # type_param = f"%2C%22type%22%3A%22{type_id}"
        type_param = f"""\"type":"{type_id}","""
    else:
        type_param = ""
    # url = f"""https://wikidata.reconci.link/en/api?queries=%7B%22q0%22%3A%7B%22query%22%3A%22{label}{type_param}%22%2C%22limit%22%3A1%7D%7D"""
    url = f"""https://wikidata.reconci.link/en/api?queries={{"q0":{{"query":"{label}",{type_param}"limit":1}}}}"""
    response = requests.get(url)
    data = json.loads(response.text)

    if "q0" in data and len(data["q0"]["result"]) > 0:
        return data["q0"]["result"][0]
    else:
        if type_id:
            # Try again without type
            return get_wikidata_id(label)
        return None


def get_wikidata_property(query):
    url = f"https://wikidata.reconci.link/en/suggest/property?prefix={query['label']}"
    response = requests.get(url)
    data = json.loads(response.text)

    return data["result"][0] if data["result"] else None


def process_statements(statements):
    for statement in statements:
        for key, value in statement.items():
            if key in ["subject", "object"]:
                if value["type"] is not None:
                    # Try to get type id from Wikidata
                    type_id = get_wikidata_id(value["type"])
                    if type_id:
                        # Reconcliation against type
                        result = get_wikidata_id(value["label"], type_id["id"])
                        # If no result, try reconcliation against no type
                    else:
                        result = get_wikidata_id(value["label"])
                else:
                    result = get_wikidata_id(value["label"])

                if result:
                    value["result"] = {
                        "description": result.get("description", ""),
                        "id": result["id"],
                        "wd_name": result.get("name", ""),
                    }
                else:
                    print(f"No matching entity found for: {value['label']}")
                    value["result"] = {
                        "description": "",
                        "id": "",
                        "wd_name": "*New: " + value["label"],
                    }

            elif key == "relation":
                result = get_wikidata_property(value)
                value["result"] = result if result else ""
                if not result:
                    print(f"No matching property found for: {value['label']}")
    return statements


reconciled_statements = process_statements(statements)


print(json.dumps(reconciled_statements, indent=4))


from pyvis.network import Network

graph = Network(height="800px", width="100%", notebook=True)

for statement in reconciled_statements:
    try:
        graph.add_node(
            statement["subject"]["result"]["id"],
            label=statement["subject"]["result"]["wd_name"],
        )
        graph.add_node(
            statement["object"]["result"]["id"],
            label=statement["object"]["result"]["wd_name"],
        )
        graph.add_edge(
            statement["subject"]["result"]["id"],
            statement["object"]["result"]["id"],
            label=statement["relation"]["label"],
        )
    except:
        print("Error adding statement to graph: " + str(statement))

graph.show("knowledge_graph_wiki1.html")


