from typing import Any
from urllib import parse as url_parse

from web_crawler.datastore import DataStore
from web_crawler.validators.validator_interface import Validator


class DomainValidator(Validator):

    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def validate(self, url: Any):
        url_parsed_obj = url_parse.urlparse(url)
        netloc = url_parsed_obj.netloc

        if self._data_store.allowed_domains.size() == 0:
            return True
        if self._data_store.allowed_domains.contains(netloc):
            return True

        return False
