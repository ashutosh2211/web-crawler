import logging
import os.path

import yaml


class CustomYAMLDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


class YAMLOutput:

    @staticmethod
    def write(data):
        logging.info(yaml.dump(data, Dumper=CustomYAMLDumper, allow_unicode=True, default_flow_style=False))


class FileOutput:

    @staticmethod
    def write(data, file_name):
        file_path: str = os.path.abspath(file_name)
        with open(file_path, "w") as file:
            yaml.dump(data, file, Dumper=CustomYAMLDumper, allow_unicode=True, default_flow_style=False)
