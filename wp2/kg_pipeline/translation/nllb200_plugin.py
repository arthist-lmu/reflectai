from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {
    "src_lang": "de",
    "tgt_lang": "en",
}


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

        src_lang = self.translate_lang_flag(self.config.get("src_lang"))
        assert src_lang, f"Unknown language {self.config.get('src_lang')}"

        tgt_lang = self.translate_lang_flag(self.config.get("tgt_lang"))
        assert tgt_lang, f"Unknown language {self.config.get('tgt_lang')}"

        self.pipe = pipeline(
            "translation",
            model=model_ckpt,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            max_length=2000,
        )

    def translate_lang_flag(self, language):
        if language == "de":
            return "deu_Latn"
        if language == "en":
            return "eng_Latn"

        return None

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        results = []
        for entry in text_entries:

            if entry.get("language", None) == self.config.get("src_lang"):
                # print(entry)

                preds = self.pipe(entry["text"])

                # print(f'{entry["text"]} ------> {preds[0]["translation_text"]}')
                results.append(
                    {
                        **entry,
                        "text": preds[0]["translation_text"],
                        "language": self.config.get("tgt_lang"),
                    }
                )
            else:
                results.append(entry)

        return results
