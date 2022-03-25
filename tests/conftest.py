import os

import pytest

from web_crawler.config.http_config import Config

FIXTURES_PATH = "tests/fixtures"
DIRECTORY = os.getcwd()


@pytest.fixture(scope='module')
def valid_config_fixture():
    path = os.path.join(DIRECTORY, FIXTURES_PATH, "test_valid_config.yml")
    config = Config(path)
    return config
