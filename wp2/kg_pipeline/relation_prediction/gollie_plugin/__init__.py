import logging
from typing import Generator

from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager


default_config = {
    "model": "HiTZ/GoLLIE-13B",
    # "template": ["iconography","museum_mentions","painting_alias",
    #             "painting_content","painting_genre","painting_material",
    #             "painting_metadata"]

    # "template": ["a_ts_content_layer_initialdescription", "ts_content_layer_initialdescription", 
    #              "ts_content_layer_llmeasylanguage", "ts_content_layer_wikidata", 
    #              "ts_metadata_layer_wikidata copy", "ts_metadata_layer_wikidata_initialdescription copy", 
    #              "ts_metadata_layer_wikidata_llmeasylanguage" ]

    "template": ["a_ts_content_layer_initialdescription"]
}
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

        self.templates = []
        for template in self.config.get('template'):
            template_definition = importlib.import_module(
                "kg_pipeline.relation_prediction.gollie_plugin.templates.{}".format(
                    template
                )
            )
            self.templates.append({
                'name': template,
                'entity_parser': template_definition.ENTITY_PARSER,
                'entity_definitions': template_definition.ENTITY_DEFINITIONS,
                'guidelines': [
                    inspect.getsource(definition)
                    for definition in template_definition.ENTITY_DEFINITIONS
                ]
            })

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("GPU available")
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

        """
        self.template = Template(template_string)

    def convert_to_triplets(self, gollie_outputs: list, entity_parser: dict, with_class_name=False) -> list[dict]:
        results = []
        for x in gollie_outputs:
            if x.__class__.__name__ in entity_parser:
                try:
                    triplets = entity_parser[x.__class__.__name__](x)
                    if with_class_name:
                        for t in triplets:
                            t.update({'class_name':x.__class__.__name__})
                except Exception as e:
                    print('Error converting Gollie output to triplet', e)
                    continue
                results.extend(triplets)

        return results

    def call(self, text_entries: list[dict]) -> Generator[dict,None,None]:
        import black
        from .utils_typing import AnnotationList

        for entry in text_entries:
            triplets = []
            for template in self.templates:
                formated_text = self.template.render(
                    guidelines=template['guidelines'],
                    text=entry["text"],
                )

                prompt = black.format_str(formated_text, mode=black.Mode())
                prompt += "result = "

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
                    pad_token_id=self.tokenizer.pad_token_id
                )
                try:
                    result = AnnotationList.from_output(
                        self.tokenizer.decode(model_ouput[0], skip_special_tokens=True).split(
                            "result = "
                        )[-1],
                        task_module="kg_pipeline.relation_prediction.gollie_plugin.templates.{}".format(
                            template['name']
                        ),
                    )
                except Exception as e:
                    logging.error(f"Gollie parse error: {e}")
                    continue

                triplets.extend(
                    self.convert_to_triplets(result, template['entity_parser'], entry['with_class_name'])
                )

            entry['triplets'].append({"type": "gollie", "content": triplets})
            yield entry
