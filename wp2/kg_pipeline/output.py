import os
import msgpack
import json
from typing import Dict
from kg_pipeline.plugin import Plugin


class OutputWrapper:
    def __init__(self, plugin: Plugin, config: Dict = None):
        self.plugin = plugin
        self.output_path = config.get("output_path")
        self.format = config.get("format")

    def __call__(self, *args, **kwargs):
        result = self.plugin(*args, **kwargs)
        if self.format == "msgpack":
            with open(
                os.path.join(self.output_path, f"{self.plugin.__class__.__name__}.msg"),
                "wb",
            ) as f:
                for t in result:
                    f.write(msgpack.packb(t))
                    yield t
        else:
            with open(
                os.path.join(
                    self.output_path, f"{self.plugin.__class__.__name__}.jsonl"
                ),
                "w",
            ) as f:
                for t in result:
                    f.write(json.dumps(t) + "\n")
                    yield t
        