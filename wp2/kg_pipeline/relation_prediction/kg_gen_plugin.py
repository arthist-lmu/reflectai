from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict, Generator
import logging

default_config = {
    "model": "ollama_chat/deepseek-r1:14b",
    "api_base": "http://gpu-p1080ti-01.research.tib.eu:11434",
    "context": "Art description",
}
default_parameters = {}

# Plugin expects ollama to be running on localhost. Depending on the binary
# location start e.g. with
# - srun -G 1 --mem 20G /nfs/home/user/ollama serve
# - ./ollama run mistral


@Manager.export("KGGen")
class KGGenPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.config)
        self.model_name = self.config.get("model", "ollama_chat/deepseek-r1:14b")
        self.api_base = self.config.get(
            "api_base", "http://gpu-p1080ti-01.research.tib.eu:11434"
        )

        from kg_gen import KGGen

        self.kg_gen_pipeline = KGGen(
            model=self.model_name,  # Default model
            temperature=0.0,  # Default temperature
            api_base=self.api_base,
            api_key="",
        )

    def call(self, text_entries: List[Dict]) -> Generator[Dict, None, None]:
        for entry in text_entries:
            triplets = []
            try:
                graph = self.kg_gen_pipeline.generate(
                    input_data=entry["text"],
                    context=self.config.get("context", "Art description"),
                )

                for x in graph.relations:

                    triplets.append(
                        {
                            "subject": {
                                "label": x[0],
                            },
                            "relation": {"label": x[1]},
                            "object": {"label": x[2]},
                        }
                    )

            except Exception as e:
                logging.error(e)
            entry["triplets"].append(
                {"type": f"kg-gen <{self.model_name}>", "content": triplets}
            )
            yield entry
