import torch
from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("KnowGL")
class KnowGLPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("GPU available")
        # elif torch.backends.mps.is_available():
        # device = torch.device("mps")
        # print("MPS available")
        else:
            print("Falling back to CPU")
            self.device = torch.device("cpu")

        # device = "gpu" if torch.cuda.is_available() else "cpu"
        # self.tokenizer = AutoTokenizer.from_pretrained("biu-nlp/f-coref")
        # self.model = AutoModel.from_pretrained("biu-nlp/f-coref")

        # self.model = FCoref(device=device)
        # This can take a while (download, and moving model to GPU)
        self.tokenizer = AutoTokenizer.from_pretrained("ibm/knowgl-large")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("ibm/knowgl-large").to(
            self.device
        )

    def parse_string(self, s):
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

        if not('object' in result and 'relation' in result and 'subject' in result):
            raise ValueError('Triplet incomplete')
        return result

    def convert_to_triplets(self, knowgl_outputs: List):
        results = []
        for x in knowgl_outputs.split("$"):
            try:
                results.append(self.parse_string(x))
            except Exception:
                print('Exception when parsing:', x)
                continue

        return results

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        for entry in text_entries:
            # print(f"----> {entry['text']}")
            inputs = self.tokenizer(entry["text"], return_tensors="pt").to(self.device)
            num_beams = 15
            output = self.model.generate(**inputs, max_length=1000, num_beams=num_beams)

            decoded_output = self.tokenizer.decode(
                output[0].to("cpu"), skip_special_tokens=True
            )

            # print(f"\t {decoded_output}")
            entry['triplets'].append({"type": "knowgl", "content": self.convert_to_triplets(decoded_output)})
            yield entry
        # This can take a while too
