import logging
import time
from threading import Event
from typing import List

from web_crawler.config.http_config import Config
from web_crawler.datastore import DataStore
from web_crawler.fields import URLData
from web_crawler.loop_thread import LoopingThread
from web_crawler.queues.queue_impl import QueueImpl
from web_crawler.site_graph import SiteGraph
from web_crawler.validators.domain_validator import DomainValidator
from web_crawler.validators.duplicate_validators import DuplicateURLValidator, DuplicateURLQueuedValidator
from web_crawler.workers.fetch_worker import URLFetchWorker
from web_crawler.workers.fetcher import URLFetcher
from web_crawler.workers.parser import URLParser
from web_crawler.workers.parser_worker import URLResponseParserWorker
from web_crawler.workers.worker_interface import Worker


class WebCrawler:

    def __init__(self, seed_urls: List[str],
                 fetch_concurrency: int,
                 parse_concurrency: int,
                 http_config: Config,
                 **kwargs):
        self._seed_urls = list(set(seed_urls))
        self._fetch_concurrency = fetch_concurrency
        self._parse_concurrency = parse_concurrency
        self._http_config = http_config
        self._additional_params = kwargs

    def crawl(self):
        visiting_urls_queue = QueueImpl()
        parser_queue = QueueImpl()
        site_graph = SiteGraph()
        seed_urls = list(filter(None, self._seed_urls))

        data_store = DataStore(visiting_urls_queue, parser_queue)
        data_store.allowed_domains = self._additional_params.get("allowed_domains", [])

        for _seed_url in seed_urls:
            stripped_seed_url = URLParser.strip_trailing_slash(_seed_url)
            data_store.add_url_to_fetch(URLData(stripped_seed_url))
            data_store.increment_rem_task_count()

        dup_url_fetched_validator = DuplicateURLValidator(data_store)
        dup_url_queued_validator = DuplicateURLQueuedValidator(data_store)
        domain_filter = DomainValidator(data_store)

        url_fetcher = URLFetcher(
            dup_url_fetched_validator,
            domain_filter,
            data_store,
            self._http_config
        )

        parse_worker = URLParser(
            domain_filter,
            dup_url_queued_validator,
            data_store,
            site_graph
        )

        fetch_url_worker = URLFetchWorker(url_fetcher)

        parse_worker = URLResponseParserWorker(parse_worker)

        thread_signal = Event()

        url_fetch_threads = self.create_thread_workers(self._fetch_concurrency, fetch_url_worker, thread_signal)
        parse_url_threads = self.create_thread_workers(self._parse_concurrency, parse_worker, thread_signal)

        thread_signal.set()

        self.start_threads(url_fetch_threads)
        self.start_threads(parse_url_threads)

        try:
            while data_store.remaining_task_count > 0:
                time.sleep(5)
                logging.info(f"Visited url count: {len(site_graph.adj_list)}")
                continue
        except KeyboardInterrupt:
            thread_signal.clear()
            while any(thread.is_alive() for thread in url_fetch_threads + parse_url_threads):
                continue
            return site_graph, data_store.unvisited_urls

        thread_signal.clear()
        return site_graph, data_store.unvisited_urls

    @staticmethod
    def create_thread_workers(concurrency: int, worker_func: Worker, signal: Event):
        threads = []
        for _ in range(concurrency):
            threads.append(LoopingThread(signal, target=worker_func.execute))

        return threads

    @staticmethod
    def start_threads(threads):
        for t in threads:
            t.start()
