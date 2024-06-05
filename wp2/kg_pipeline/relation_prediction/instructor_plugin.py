from kg_pipeline.plugin import Plugin
from kg_pipeline.manager import Manager
from typing import List, Dict

default_config = {'model': 'mistral'}
default_parameters = {}

# Plugin expects ollama to be running on localhost. Depending on the binary
# location start e.g. with
# - srun -G 1 --mem 20G /nfs/home/user/ollama serve
# - ./ollama run mistral

@Manager.export("Instructor")
class InstructorPlugin(
    Plugin, config=default_config, parameters=default_parameters, version="0.1"
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = self.config['model']

        import instructor
        from openai import OpenAI
        self.client = instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON
        )

    def call(self, text_entries: List[Dict]) -> List[Dict]:
        from instructor.retry import InstructorRetryException
        from relation_prediction.gollie_plugin import templates
        from relation_prediction.gollie_plugin.utils_typing import Generic
        from pydantic import BaseModel
        import inspect

        modules = [
            module
            for name, module in inspect.getmembers(templates)
            if not name.startswith('__')
        ]
        for entry in text_entries:
            triplets = []
            for module in modules:
                for class_ in module.ENTITY_DEFINITIONS:
                    if not issubclass(class_, Generic):
                        continue

                    pydantic_class = type(
                        class_.__name__,
                        (BaseModel,),
                        {'__module__': class_.__module__,
                         '__annotations__': class_.__annotations__}
                    )

                    try:
                        resp = self.client.chat.completions.create(
                            model=self.model_name,
                            response_model=pydantic_class,
                            messages=[{"role": "user", "content": entry['text']}],
                        )
                    except InstructorRetryException:
                        print('InstructorRetryException')
                        continue

                    try:
                        triplets.extend(module.ENTITY_PARSER[class_.__name__](resp))
                    except Exception as e:
                        print('Exception when converting to triplet:', e)

            entry['triplets'].append({
                "type": f"instructor <{self.model_name}>",
                "content": triplets
            })
            yield entry
