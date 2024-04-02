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

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:
            # print(f"----> {entry['text']}")
            inputs = self.tokenizer(entry["text"], return_tensors="pt").to(self.device)
            num_beams = 15
            output = self.model.generate(**inputs, max_length=1000, num_beams=num_beams)

            decoded_output = self.tokenizer.decode(
                output[0].to("cpu"), skip_special_tokens=True
            )
            # print(f"\t {decoded_output}")
            results.append(
                {**entry, "triplets": [{"type": "knowgl", "content": decoded_output}]}
            )
        return results
        # This can take a while too
