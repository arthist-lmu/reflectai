import torch
from pipeline.plugin import Plugin
from pipeline.manager import Manager
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
        import black
        from jinja2 import Template
        from .triplet_relation import (
            ENTITY_DEFINITIONS,
            PersonalSocialRelation,
            PhysicalRelation,
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

        self.tokenizer = AutoTokenizer.from_pretrained("HiTZ/GoLLIE-7B")
        self.model = AutoModelForCausalLM.from_pretrained(
            "HiTZ/GoLLIE-7B", trust_remote_code=True, torch_dtype=torch.bfloat16
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
        self.text = "Ana and Mary are sisters. Mary was at the supermarket while Ana was at home."
        self.gold = [
            PersonalSocialRelation(arg1="Ana", arg2="Mary"),
            PhysicalRelation(arg1="Mary", arg2="supermarket"),
            PhysicalRelation(arg1="Ana", arg2="home"),
        ]

        template = Template(template_string)
        # Fill the template
        formated_text = template.render(
            guidelines=self.guidelines,
            text=self.text,
            annotations=self.gold,
            gold=self.gold,
        )
        print(formated_text)

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
