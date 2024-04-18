from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("FCoref")
class FCorefPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import torch
        from transformers import AutoTokenizer, AutoModel
        from fastcoref import spacy_component
        import spacy

        # device = "gpu" if torch.cuda.is_available() else "cpu"
        # self.tokenizer = AutoTokenizer.from_pretrained("biu-nlp/f-coref")
        # self.model = AutoModel.from_pretrained("biu-nlp/f-coref")

        # self.model = FCoref(device=device)

        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("fastcoref")

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:
            doc = self.nlp(  # for multiple texts use nlp.pipe
                entry["text"], component_cfg={"fastcoref": {"resolve_text": True}}
            )
            results.append({**entry, "text": doc._.resolved_text})

        # input_data = self.tokenizer(text, return_tensors="pt")
        # print(input_data)
        # preds = self.model(**input_data)
        return results
