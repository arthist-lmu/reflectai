from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModel
from fastcoref import spacy_component
import spacy
from pipeline.plugin import Plugin
from pipeline.manager import Manager

default_config = {}


default_parameters = {}


@Manager.export("NLLB200")
class NLLB200Plugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_ckpt = "facebook/nllb-200-distilled-1.3B"
        self.pipe = pipeline(
            "translation", model=model_ckpt, src_lang="eng_Latn", tgt_lang="deu_Latn"
        )

    def call(self, text):
        preds = self.pipe(text)
        return preds
