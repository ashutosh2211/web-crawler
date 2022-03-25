import os
from typing import Optional

import yaml
from yaml import SafeLoader


class Config(object):
    """
    Config object to parse and hold the config yml
    """
    _CONFIG_FILE: Optional[str] = None
    _CONFIG: Optional[dict] = None

    def __init__(self, config_file=None):
        if config_file is None:
            raise ValueError()

        if config_file:
            if not os.path.isabs(config_file):
                config_file = os.path.join(os.getcwd(), config_file)
        else:
            config_file = os.path.join(os.path.dirname(__file__), 'config.yml')

        assert os.path.exists(config_file), f"Config file not present at path: {config_file}"

        Config._CONFIG_FILE = config_file
        with open(config_file, 'r') as f:
            field_attributes = yaml.load(f, Loader=SafeLoader)
            Config._CONFIG = field_attributes

    @staticmethod
    def get_config_file() -> str:
        return Config._CONFIG_FILE

    @staticmethod
    def get_var(var: str):
        """
        Get config data for given variable
        :param var: lookup variable
        :return: config data stored for the variable
        """
        assert Config._CONFIG
        if var not in Config._CONFIG:
            raise ValueError(f"Please set the {var} variable in the config file {Config._CONFIG_FILE}")
        return Config._CONFIG[var]
