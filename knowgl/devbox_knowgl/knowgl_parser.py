
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU available")
#elif torch.backends.mps.is_available():
    #device = torch.device("mps")
    #print("MPS available")
else:
    print("Falling back to CPU")
    device = torch.device("cpu")


# This can take a while (download, and moving model to GPU)
tokenizer = AutoTokenizer.from_pretrained("ibm/knowgl-large")
model = AutoModelForSeq2SeqLM.from_pretrained("ibm/knowgl-large").to(device)


import json

file_path = "wikipedia-20220107.jsonl"

input_text = """"""
line_count = 0
with open(file_path, "r") as file:
    for line in file:
        data = json.loads(line)
        if data["text"]["language"] == "en":
            entry_text = data["text"]["entry"]
            input_text = input_text + entry_text + "\n"
            line_count += 1
            if line_count == 10:
                break

print("Input text pages: " + str(len(input_text)))

import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize

# Split the input text into sentences using nltk tokenizer
sentences = sent_tokenize(input_text)
print("Tokenized sentences into: " + str(len(sentences)) + " sentences")

import time 

start_time = time.time()
decoded_outputs = []

for sentence in sentences:
    inputs = tokenizer(sentence, return_tensors="pt").to(device)
    # This can take a while too
    num_beams = 15
    output = model.generate(**inputs, max_length=1000, num_beams=num_beams)

    decoded_output = tokenizer.decode(output[0].to(device), skip_special_tokens=True)
    decoded_outputs.append(decoded_output)

end_time = time.time()
print("Time to process: " + str(end_time - start_time) + " seconds")




def parse_string(s):
    s = s.strip("[]")
    # Split into subject, relation, object
    parts = s.split("|")
    result = {}
    for i, part in enumerate(parts):
        part = part.strip("()")
        mention_label_type = part.split("#")
        if i == 0:
            result["subject"] = {
                "mention": mention_label_type[0],
                "label": mention_label_type[1],
                "type": mention_label_type[2],
            }
        elif i == 1:
            result["relation"] = {"label": mention_label_type[0]}
        else:
            result["object"] = {
                "mention": mention_label_type[0],
                "label": mention_label_type[1],
                "type": mention_label_type[2],
            }
    return result


statements = []
for line in decoded_outputs:
    single_statement = line.split("$")
    for statement_text in single_statement:
        try:
            parsed_statement = parse_string(statement_text)
        except:
            print("Error parsing statement: " + statement_text)
        statements.append(parsed_statement)

print("Statements extracted: " + str(len(statements)))

import json

# Save statements to file to split the most ressource intensive steps
# First the knowledge extraction of the raw text
# After this the knowledge reconciliation with Wikidata
statements_json = json.dumps(statements, indent=4)

file_path = "statements.json"

with open(file_path, "w") as file:
    file.write(statements_json)

print("Statements saved to file:", file_path)

