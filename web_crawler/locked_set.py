from threading import Lock
from typing import List


class LockedSet():
    """A set where add(), remove(), and 'in' operator are thread-safe"""

    def __init__(self):
        self._lock = Lock()
        self._objs = set()

    @property
    def objs(self):
        return self._objs

    def set(self, elems: List):
        with self._lock:
            self._objs = set(elems)
            return self

    def add(self, elem):
        with self._lock:
            self._objs.add(elem)

    def remove(self, elem):
        with self._lock:
            self._objs.remove(elem)

    def contains(self, elem):
        with self._lock:
            return elem in self._objs

    def size(self):
        with self._lock:
            return len(self.objs)

    def __contains__(self, elem):
        return self.contains(elem)
