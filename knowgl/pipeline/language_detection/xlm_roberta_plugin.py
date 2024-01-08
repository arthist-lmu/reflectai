from transformers import pipeline
import torch
from pipeline.plugin import Plugin
from pipeline.manager import Manager
import numpy as np

default_config = {}


default_parameters = {}


@Manager.export("XLMRobertaLanguageDetection")
class XLMRobertaLanguageDetectionPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_ckpt = "papluca/xlm-roberta-base-language-detection"
        self.pipe = pipeline("text-classification", model=model_ckpt)

    def call(self, text_entries):
        results = []
        for entry in text_entries:
            preds = self.pipe(
                entry["text"], return_all_scores=True, truncation=True, max_length=128
            )[0]

            max_probs = np.argmax([x["score"] for x in preds])
            results.append({**entry, "language": preds[max_probs]["label"]})
        return results
