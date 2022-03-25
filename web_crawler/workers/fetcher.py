import logging
from typing import Dict, Any, List

import requests
from opnieuw import retry
from requests import Response, Timeout

from web_crawler.config.http_config import Config
from web_crawler.datastore import DataStore
from web_crawler.execptions import URLRetryException, URLResponseException
from web_crawler.fields import URLData
from web_crawler.utils import get_md5
from web_crawler.validators.validator_interface import Validator

logger = logging.getLogger(__name__)


class URLFetcher:

    def __init__(self,
                 duplicate_url_validator: Validator,
                 domain_validator: Validator,
                 data_store: DataStore,
                 http_config: Config):
        self._dup_url_validator = duplicate_url_validator
        self._domain_validator = domain_validator
        self._data_store = data_store
        self._http_config = http_config

    def fetch_urls(self):
        url_data: URLData = self._data_store.get_next_url_to_fetch()

        if not url_data:
            return

        if not self._run_validators(url_data.url, [self._dup_url_validator, self._domain_validator]):
            self._data_store.decrement_rem_task_count()
            return

        url = url_data.url
        self._data_store.set_url_seen(url)

        try:
            headers = self.get_http_headers(self._http_config, url)
            resp: Response = self.url_request(url, headers)

            if not resp or resp.status_code != 200:
                raise URLResponseException(f"Error in fetching response for {url}")

            resp_content = self.get_resp_from_content_type(resp)
            if resp_content:
                try:
                    resp_content_hash = get_md5(resp_content)
                except TypeError as exc:
                    logger.debug(exc)
                    raise URLResponseException("Content could not be hashed due to incorrect encoding")

                self._data_store.add_page_to_parse(URLData(url, resp_content))
                self._data_store.set_page_seen(resp_content_hash)
            else:
                raise URLResponseException("Empty Response content or content-type is not text/html")

        except (URLResponseException, URLRetryException) as exc:
            logger.debug(exc)
            self._data_store.add_unvisited_url(url_data.url)
            self._data_store.decrement_rem_task_count()

        self._data_store.mark_url_fetch_complete()

    def _run_validators(self, url: Any, filters: List[Validator]) -> bool:
        return all(_filter.validate(url) for _filter in filters)

    @staticmethod
    def get_resp_from_content_type(resp: Response):
        content_type = resp.headers.get("Content-Type")
        if content_type and "text/html" in content_type:
            return resp.content

    @staticmethod
    def get_http_headers(http_config: Config, url):
        try:
            headers = http_config.get_var("headers")
            timeout = http_config.get_var("default_timeout")

            return {
                "headers": URLFetcher.get_user_agent_by_url(url, headers.get("User-Agent")),
                "timeout": timeout
            }

        except KeyError as exc:
            logger.error("Unable to get headers", exc)
            return {}

    @staticmethod
    def get_user_agent_by_url(url, user_agent):
        if '//m.' in url:
            return user_agent['mobile']
        else:
            return user_agent['www']

    @staticmethod
    @retry(
        retry_on_exceptions=(ConnectionError, URLRetryException, Timeout),
        max_calls_total=1,
        retry_window_after_first_call_in_seconds=4,
    )
    def url_request(url: str, headers: Dict[str, str]):
        if not url:
            return

        resp = requests.get(url, headers=headers)
        if resp.status_code in (413, 429, 500, 502, 503, 504):
            raise URLRetryException(f"Retry for {url}")

        return resp
