from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict
import logging


default_config = {"model": "HiTZ/GoLLIE-13B", "template": "paintin_content"}


default_parameters = {}


@Manager.export("Gollie")
class GolliePlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import torch
        import inspect
        from jinja2 import Template
        import importlib
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM

        template_definition = importlib.import_module(
            "kg_pipeline.relation_prediction.gollie_plugin.templates.{}".format(
                self.config.get("template")
            )
        )

        self.ENTITY_PARSER = template_definition.ENTITY_PARSER
        self.ENTITY_DEFINITIONS = template_definition.ENTITY_DEFINITIONS

        self.guidelines = [
            inspect.getsource(definition) for definition in self.ENTITY_DEFINITIONS
        ]

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("GPU available")
        # elif torch.backends.mps.is_available():
        # device = torch.device("mps")
        # print("MPS available")
        else:
            print("Falling back to CPU")
            self.device = torch.device("cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(self.config.get("model"))
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.get("model"),
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
        )
        self.model.to(self.device)
        template_string = """
# The following lines describe the task definition
{%- for definition in guidelines %}
{{ definition }}
{%- endfor %}

# This is the text to analyze
text = {{ text.__repr__() }}

# The annotation instances that take place in the text above are listed here
result = [
{%- for ann in annotations %}
    {{ ann }},
{%- endfor %}
]
        """
        self.gold = ""
        self.template = Template(template_string)

    def convert_to_triplets(self, gollie_outputs: List):
        results = []
        for x in gollie_outputs:
            if x.__class__.__name__ in self.ENTITY_PARSER:
                triplets = self.ENTITY_PARSER[x.__class__.__name__](x)
                print("FOUND")
                print(triplets)
                results.extend(triplets)
            print(f"\t--> {x}")

        return results

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        import black
        from .utils_typing import AnnotationList

        results = []
        for entry in text_entries:
            # print(f"#######################################")
            # print(f"#######################################")
            # print(f"----> {entry['text']}")

            # Fill the template
            formated_text = self.template.render(
                guidelines=self.guidelines,
                text=entry["text"],
                annotations=self.gold,
                gold=self.gold,
            )
            # print(formated_text)

            black_mode = black.Mode()
            formated_text = black.format_str(formated_text, mode=black_mode)

            # print(formated_text)
            prompt, _ = formated_text.split("result =")
            prompt = prompt + "result ="

            # print(prompt)
            model_input = self.tokenizer(
                prompt, add_special_tokens=True, return_tensors="pt"
            )
            model_input["input_ids"] = model_input["input_ids"][:, :-1]
            model_input["attention_mask"] = model_input["attention_mask"][:, :-1]
            model_ouput = self.model.generate(
                **model_input.to(self.model.device),
                max_new_tokens=256,
                do_sample=False,
                min_new_tokens=0,
                num_beams=1,
                num_return_sequences=1,
            )
            try:
                result = AnnotationList.from_output(
                    self.tokenizer.decode(model_ouput[0], skip_special_tokens=True).split(
                        "result = "
                    )[-1],
                    task_module="kg_pipeline.relation_prediction.gollie_plugin.templates.{}".format(
                        self.config.get("template")
                    ),
                )
            except Exception as e:
                logging.error(f"Gollie parse error{e}")
                yield {**entry, "triplets": [{"type": "gollie", "content": []}]}
            # print("##########")
            # print(result)
            # print("##########")

            triplets = self.convert_to_triplets(result)

            # for x in triplets:
            #     print(x)
            yield {**entry, "triplets": [{"type": "gollie", "content": triplets}]}
            