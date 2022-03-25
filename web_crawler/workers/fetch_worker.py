from web_crawler.workers.fetcher import URLFetcher
from web_crawler.workers.worker_interface import Worker


class URLFetchWorker(Worker):

    def __init__(self, url_fetcher: URLFetcher):
        self._url_fetcher = url_fetcher

    def execute(self):
        self._url_fetcher.fetch_urls()
