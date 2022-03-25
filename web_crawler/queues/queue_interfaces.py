from abc import ABC, abstractmethod


class QueueInterface(ABC):

    @abstractmethod
    def enqueue(self, elem):
        raise NotImplementedError("An implementation of this class is needed")

    @abstractmethod
    def dequeue_sync(self):
        raise NotImplementedError("An implementation of this class is needed")

    @abstractmethod
    def dequeue_async(self):
        raise NotImplementedError("An implementation of this class is needed")

    @abstractmethod
    def task_complete(self):
        raise NotImplementedError("An implementation of this class is needed")
