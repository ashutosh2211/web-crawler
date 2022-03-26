import logging
import os.path

import yaml


class CustomYAMLDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


class YAMLOutput:

    def __init__(self, custom_dumper=CustomYAMLDumper):
        self._custom_dumper = custom_dumper

    def write(self, data):
        logging.info(yaml.dump(data, Dumper=self._custom_dumper, allow_unicode=True, default_flow_style=False))


class FileOutput:

    def __init__(self, output_dir="output"):
        self._output_dir = output_dir
        self.create_output_dir(output_dir)

    @staticmethod
    def create_output_dir(output_dir):
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

    def write(self, data, file_name):
        file_path: str = os.path.abspath(f"{self._output_dir}/{file_name}")
        with open(file_path, "w") as file:
            yaml.dump(data, file, Dumper=CustomYAMLDumper, allow_unicode=True, default_flow_style=False)
