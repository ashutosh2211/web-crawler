from typing import Any

from web_crawler.datastore import DataStore
from web_crawler.validators.validator_interface import Validator


class DuplicateURLValidator(Validator):

    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def validate(self, url: Any):
        if self._data_store.is_url_seen(url):
            # print(f"URL seen already: {url}")
            return False

        return True


class DuplicateURLQueuedValidator(Validator):

    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def validate(self, url: Any):
        if self._data_store.is_url_queued(url):
            return False

        return True


class DuplicatePageValidator(Validator):

    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def validate(self, page_hash: Any):
        if self._data_store.is_page_seen(page_hash):

            return False

        return True
