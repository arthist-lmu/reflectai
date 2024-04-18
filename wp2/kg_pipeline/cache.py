import hashlib
import json
import logging
from typing import List, Dict
from kg_pipeline.plugin import Plugin


def flat_dict(data_dict, parse_json=False):
    result_map = {}
    for k, v in data_dict.items():
        if isinstance(v, dict):
            embedded = flat_dict(v)
            for s_k, s_v in embedded.items():
                s_k = f"{k}.{s_k}"
                if s_k in result_map:
                    logging.error(f"flat_dict: {s_k} alread exist in output dict")

                result_map[s_k] = s_v
            continue

        if k not in result_map:
            result_map[k] = []
        result_map[k] = v
    return result_map


def get_hash_for_plugin(
    plugin: str,
    output: str,
    version: str = None,
    parameters: List = [],
    inputs: List = [],
    config: Dict = {},
):
    plugin_call_dict = {
        "plugin": plugin,
        "output": output,
        "parameters": parameters,
        "inputs": inputs,
        "config": config,
        "version": version,
    }

    plugin_hash = hashlib.sha256(
        json.dumps(
            flat_dict(
                {
                    "plugin": plugin,
                    "output": output,
                    "parameters": parameters,
                    "inputs": inputs,
                    "config": config,
                    "version": version,
                }
            )
        ).encode()
    ).hexdigest()

    # logging.info(f"[HASH] {plugin_hash}")
    return plugin_hash


class CacheWrapper:
    def __init__(self, plugin: Plugin, config: Dict = None):
        super().__init__(config)
        self.r = redis.Redis(
            host=self.config.get("host"),
            port=self.config.get("port"),
            db=self.config.get("db"),
        )

    def set(self, id: str, data: Any) -> bool:
        try:
            packed = msgpack.packb(data)
            tag = self.config.get("tag")
            self.r.set(f"{tag}:{id}", packed)
        except Exception as e:
            logging.error(f"RedisCache {e}")

    def delete(self, id: str) -> bool:
        try:
            tag = self.config.get("tag")
            return self.r.delete(f"{tag}:{id}")
        except Exception as e:
            logging.error(f"RedisCache {e}")
            return None

    def get(self, id: str) -> Any:
        try:
            tag = self.config.get("tag")
            packed = self.r.get(f"{tag}:{id}")
            if packed is None:
                return None
            return msgpack.unpackb(packed)
        except Exception as e:
            logging.error(f"RedisCache {e}")
            return None

    def keys(self) -> List[str]:
        try:
            tag = self.config.get("tag")
            start = len(f"{tag}:")
            keys = self.r.scan_iter(f"{tag}:*", 500)

            # print([x for x in Batcher(keys, 2)])
            return [key[start:].decode("utf-8") for key in keys]
        except Exception as e:
            logging.error(f"RedisCache {e}")
            return []

    def __iter__(self) -> Iterator:
        try:
            tag = self.config.get("tag")
            start = len(f"{tag}:")
            keys = list(self.r.scan_iter(f"{tag}:*", 500))
            while len(keys) > 0:
                batch_keys = keys[:500]
                keys = keys[500:]

                values = self.r.mget(batch_keys)
                for k, v in zip(batch_keys, values):
                    yield k[start:].decode("utf-8"), msgpack.unpackb(v)

        except Exception as e:
            logging.error(f"RedisCache {e}")
            yield from []
