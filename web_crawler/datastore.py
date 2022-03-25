from typing import List

from web_crawler.atomic_count import AtomicInteger
from web_crawler.fields import URLData
from web_crawler.locked_set import LockedSet
from web_crawler.queues.queue_interfaces import QueueInterface


class DataStore:

    def __init__(self, url_fetch_queue: QueueInterface, content_parse_queue: QueueInterface):
        self._url_fetch_queue = url_fetch_queue
        self._content_parse_queue = content_parse_queue
        self._seen_urls = LockedSet()
        self._queued_urls = LockedSet()
        self._unvisited_urls = LockedSet()
        self._seen_pages = LockedSet()
        self._allowed_domains = LockedSet()
        self._remaining_task_count = AtomicInteger(0)

    @property
    def seen_urls(self) -> LockedSet:
        return self._seen_urls

    @property
    def seen_pages(self) -> LockedSet:
        return self._seen_pages

    @property
    def allowed_domains(self) -> LockedSet:
        return self._allowed_domains

    @allowed_domains.setter
    def allowed_domains(self, allowed_domains: List[str]):
        self._allowed_domains = self._allowed_domains.set(allowed_domains)

    @property
    def remaining_task_count(self) -> int:
        return self._remaining_task_count.value

    @property
    def unvisited_urls(self) -> LockedSet:
        return self._unvisited_urls

    def is_url_seen(self, url: str) -> bool:
        return self._seen_urls.contains(url)

    def is_page_seen(self, page_hash: str) -> bool:
        return page_hash in self._seen_pages

    def is_url_queued(self, url: str) -> bool:
        return self._queued_urls.contains(url)

    def set_url_seen(self, url: str) -> None:
        self._seen_urls.add(url)

    def set_url_queued(self, url: str):
        self._queued_urls.add(url)

    def set_page_seen(self, page_hash: str) -> None:
        self._seen_pages.add(page_hash)

    def add_unvisited_url(self, url: str):
        self._unvisited_urls.add(url)

    def increment_rem_task_count(self, val=1) -> None:
        self._remaining_task_count.inc(val)

    def decrement_rem_task_count(self, val=1) -> None:
        self._remaining_task_count.dec(val)

    def add_url_to_fetch(self, url_data: URLData) -> None:
        self._url_fetch_queue.enqueue(url_data)

    def add_page_to_parse(self, url_data: URLData):
        self._content_parse_queue.enqueue(url_data)

    def get_next_url_to_fetch(self):
        return self._url_fetch_queue.dequeue_async()

    def get_next_page_to_parse(self):
        return self._content_parse_queue.dequeue_async()

    def mark_url_fetch_complete(self):
        self._url_fetch_queue.task_complete()

    def mark_page_parse_complete(self):
        self._content_parse_queue.task_complete()
