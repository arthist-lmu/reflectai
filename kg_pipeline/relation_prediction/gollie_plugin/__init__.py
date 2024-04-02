import torch
from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {}


default_parameters = {}


@Manager.export("Gollie")
class GolliePlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import inspect
        from jinja2 import Template
        from .triplet_relation import (
            ENTITY_DEFINITIONS,
        )
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("GPU available")
        # elif torch.backends.mps.is_available():
        # device = torch.device("mps")
        # print("MPS available")
        else:
            print("Falling back to CPU")
            self.device = torch.device("cpu")

        self.tokenizer = AutoTokenizer.from_pretrained("HiTZ/GoLLIE-13B")
        self.model = AutoModelForCausalLM.from_pretrained(
            "HiTZ/GoLLIE-13B", trust_remote_code=True, torch_dtype=torch.bfloat16
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

        self.guidelines = [
            inspect.getsource(definition) for definition in ENTITY_DEFINITIONS
        ]

        self.gold = ""

        self.template = Template(template_string)

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        import black
        from .utils_typing import AnnotationList

        results = []
        for entry in text_entries:
            print(f"#######################################")
            print(f"#######################################")
            print(f"----> {entry['text']}")

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
                max_new_tokens=128,
                do_sample=False,
                min_new_tokens=0,
                num_beams=1,
                num_return_sequences=1,
            )
            # print(model_ouput)

            result = AnnotationList.from_output(
                self.tokenizer.decode(model_ouput[0], skip_special_tokens=True).split(
                    "result = "
                )[-1],
                task_module="kg_pipeline.relation_prediction.gollie_plugin.triplet_relation",
            )
            for x in result:
                print(f"\t--> {x}")

            results.append(
                {**entry, "triplets": [{"type": "knowgl", "content": result}]}
            )
        return results
        # This can take a while too
