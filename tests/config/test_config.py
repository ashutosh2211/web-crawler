import os

import pytest

from web_crawler.config.http_config import Config

FIXTURES_PATH = "tests/fixtures"
DIRECTORY = os.getcwd()


class TestConfig:

    def test_config_with_path(self, valid_config_fixture):
        assert len(valid_config_fixture.get_var("headers")) == 1

    def test_config_with_invalid_path(self):
        path = "test"

        with pytest.raises(AssertionError) as exc:
            Config(path)

        assert f"Config file not present at path: {os.path.join(os.getcwd(), path)}" == str(exc.value)

    def test_config_with_missing_var(self, valid_config_fixture):
        var = "test"
        with pytest.raises(ValueError) as exc:
            valid_config_fixture.get_var(var)

        assert f"Please set the {var} variable in the config file {valid_config_fixture.get_config_file()}" \
               == str(exc.value)
