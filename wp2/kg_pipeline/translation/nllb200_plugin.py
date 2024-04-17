from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("NLLB200")
class NLLB200Plugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from transformers import pipeline
        import torch
        from transformers import AutoTokenizer, AutoModel
        from fastcoref import spacy_component
        import spacy

        model_ckpt = "facebook/nllb-200-distilled-600M"
        self.pipe = pipeline(
            "translation",
            model=model_ckpt,
            src_lang="deu_Latn",
            tgt_lang="eng_Latn",
            max_length=2000,
        )

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:

            preds = self.pipe(entry["text"])

            print(f'{entry["text"]} ------> {preds[0]["translation_text"]}')
            results.append({**entry, "text": preds[0]["translation_text"]})
        return results
