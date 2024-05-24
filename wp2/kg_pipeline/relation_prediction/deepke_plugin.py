import copy
import json
from typing import List, Dict

from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager


default_config = {}
default_parameters = {}


@Manager.export("DeepKE")
class DeepKePlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        import torch
        from transformers import (
            AutoConfig,
            AutoTokenizer,
            AutoModelForCausalLM,
            BitsAndBytesConfig
        )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = 'zjunlp/OneKE'
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            config=config,
            device_map="auto",
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        self.model.eval()


    def call(self, text_entries: List[Dict]) -> List[Dict]:
        from transformers import GenerationConfig

        for entry in text_entries:
            system_prompt = '<<SYS>>\nYou are a helpful assistant. 你是一个乐于助人的助手。\n<</SYS>>\n\n'

            prompt = {
                "instruction": "You are an expert specializing in relation extraction. Please extract relationship triples that comply with the schema definition from the input; return an empty list for non-existent relationships. Please respond in the JSON string format.",
                "schema": {
                    "PaintingSubject": "Main Subject of a painting",
                    "PaintingGenre": "The genre of a painting like abstract, portrait, still life or landscape",
                    "CreatorRelation": "The name or pseudonym of the painter that created the painting.",
                    "MuseumsMentioned": "A museum that is mentioned in the article",
                    "PaintingMaterial": "The material of a painting mentioned in the article like oil painting on canvas",
                    "LocationCreationRelation": "The name of the location where the painting was created"
                },
                "example": [
                    {
                        "input" : "Still Life with Silver-Gilt Glass Holder - This intimate little banquet piece, which has never before been published, is executed in Abraham van Beyeren's typical manner with rapid brushstrokes and thickly applied highlights. The composition is dominated by the winged wine glass on the right and the silver-gilt glass holder with the figure of Bacchus in the middle, which is very probably a variation of the salt cellar created in 1639 by the Amsterdam silversmith Johannes Lutma",
                        "output": {
                            "CreatorRelation": [
                                {
                                    "subject": "Still Life with Silver-Gilt Glass Holder",
                                    "object": "Abraham van Beyeren"
                                }
                            ],
                            "PaintingSubject": [
                                {
                                    "subject": "Still Life with Silver-Gilt Glass Holder",
                                    "object": "silver-gilt glass holder"
                                },
                                {
                                    "subject": "Still Life with Silver-Gilt Glass Holder",
                                    "object": "winged wine glass"
                                }
                            ]
                        }
                    }
                ],
                "input": entry['text']
            }

            chunk_size = 2
            triplets = []

            for chunk_i in range(0, len(prompt['schema']), chunk_size):
                # We only use chunk_size schemas at the same time in prompt
                # so filter out schemas and examples here
                schemas = sorted(prompt['schema'].keys())[chunk_i:chunk_i+chunk_size]
                prompt_partial = copy.deepcopy(prompt)
                for schema in set(prompt_partial['schema']).difference(schemas):
                    del prompt_partial['schema'][schema]
                for example in prompt_partial['example']:
                    for schema in set(example['output']).difference(schemas):
                        del example['output'][schema]
                prompt_partial['example'] = [
                    example
                    for example in prompt_partial['example']
                    if len(example['output']) > 0
                ]

                prompt_partial = json.dumps(prompt_partial)
                sintruct = '[INST] ' + system_prompt + prompt_partial + '[/INST]'

                input_ids = self.tokenizer.encode(sintruct, return_tensors="pt").to(self.device)
                input_length = input_ids.size(1)

                generation_output = self.model.generate(
                    input_ids=input_ids,
                    generation_config=GenerationConfig(
                        max_length=1024,
                        max_new_tokens=512,
                        return_dict_in_generate=True,
                        stop_strings=[']}'],
                    ),
                    pad_token_id=self.tokenizer.eos_token_id,
                    tokenizer=self.tokenizer
                )
                generation_output = generation_output.sequences[0]
                generation_output = generation_output[input_length:]
                output = self.tokenizer.decode(generation_output, skip_special_tokens=True)

                try:
                    output = json.loads(output)
                except json.decoder.JSONDecodeError:
                    print('Skipping invalid JSON')
                    continue

                triplets.extend(self.rewrite_triplets(output))

            yield {**entry, "triplets": [{"type": "deepke", "content": triplets}]}


    def rewrite_triplets(self, triplets):
        reformatted = []
        for relation, duplets in triplets.items():
            try:
                for duplet in duplets:
                    reformatted.append({
                        'relation': {'label': relation},
                        'subject': {'label': duplet['subject']},
                        'object': {'label': duplet['object']}
                    })
            except TypeError:
                continue

        return reformatted
