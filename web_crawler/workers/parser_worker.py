import logging

from web_crawler.workers.parser import URLParser
from web_crawler.workers.worker_interface import Worker

logger = logging.getLogger(__name__)


class URLResponseParserWorker(Worker):

    def __init__(self, url_parser: URLParser):
        self._url_parser = url_parser

    def execute(self):
        self._url_parser.parse()
