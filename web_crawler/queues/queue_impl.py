from queue import Queue, Empty
from typing import Optional

from web_crawler.fields import URLData
from web_crawler.queues.queue_interfaces import QueueInterface


class QueueImpl(QueueInterface):

    def __init__(self):
        self._queue = Queue()

    def enqueue(self, elem: URLData):
        self._queue.put(elem)

    def dequeue_sync(self) -> URLData:
        return self._queue.get()

    def dequeue_async(self) -> Optional[URLData]:
        try:
            elem = self._queue.get_nowait()
        except Empty:
            return None

        return elem

    def task_complete(self) -> None:
        self._queue.task_done()

    def size(self) -> int:
        return self._queue.qsize()

# class QueueProducerImpl(QueueProducer):
#
#     def __init__(self, queue: QueueImpl):
#         self._queue = queue
#
#     def put(self, elem: Any) -> None:
#         self._queue.enqueue(elem)
#
#     def get(self):
#         try:
#             elem = self._queue.dequeue_async()
#         except Empty:
#             return None
