import importlib
import os
import re
import sys
import logging
import uuid

from typing import Union, Dict

from .plugin import Plugin

from packaging import version


class Manager:
    _plugins = {}

    def __init__(self, plugin_paths=None, configs=None):
        self.configs = configs
        if configs is None:
            self.configs = []

        self.plugin_paths = plugin_paths
        if not isinstance(self.plugin_paths, list):
            self.plugin_paths = [self.plugin_paths]

        for plugin_path in self.plugin_paths:
            self.find(plugin_path)

        print(self._plugins)
        self.plugin_list = self.build_plugin_list()

    @classmethod
    def export(cls, name):
        def export_helper(plugin):
            cls._plugins[name] = plugin
            return plugin

        return export_helper

    def find(self, path):
        file_re = re.compile(r"(.+?)\.py$")
        subfolder = path.split("knowgl/pipeline/")[-1]
        for pl in os.listdir(path):
            match = re.match(file_re, pl)
            if match:
                if match.group(1) in ["main", "__init__"]:
                    continue
                print(
                    "pipeline.{}.{}".format(subfolder.replace("/", "."), match.group(1))
                )
                a = importlib.import_module(
                    "pipeline.{}.{}".format(subfolder.replace("/", "."), match.group(1))
                )
                # print(a)
                function_dir = dir(a)
                if "register" in function_dir:
                    a.register(self)

    def plugins(self):
        return self.plugin_list

    def build_plugin_list(self, plugins=None, configs=None):
        if plugins is None:
            plugins = list(self._plugins.keys())

        # TODO add merge tools
        if configs is None:
            configs = self.configs

        plugin_list = []
        plugin_name_list = [x.lower() for x in plugins]

        for plugin_name, plugin_class in self._plugins.items():
            if plugin_name.lower() not in plugin_name_list:
                continue
            plugin_has_config = False
            plugin_config = {"params": {}}
            for x in configs:
                # print("############", flush=True)
                # print(x, flush=True)
                # print("############", flush=True)
                if x["type"].lower() == plugin_name.lower():
                    plugin_config.update(x)
                    plugin_has_config = True
            # if not plugin_has_config:
            #     continue
            plugin_list.append(
                {
                    "plugin_key": plugin_name,
                    "plugin_cls": plugin_class,
                    "config": plugin_config["params"],
                }
            )
        return plugin_list

    def build_plugin(self, plugin: str, config: Dict = None) -> Plugin:
        if plugin not in self._plugins:
            return None
        plugin_to_run = None
        for plugin_name, plugin_cls in self._plugins.items():
            if plugin_name == plugin:
                plugin_to_run = plugin_cls

        if plugin_to_run is None:
            logging.error(f"[AnalyserPluginManager] plugin: {plugin} not found")
            return None

        return plugin_to_run(config=config)
