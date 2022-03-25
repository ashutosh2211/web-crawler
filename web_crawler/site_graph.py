import logging
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class SiteGraph:

    def __init__(self):
        self._item_lock = defaultdict(Lock)
        self._adj_list = defaultdict(list)

    @property
    def adj_list(self):
        return self._adj_list

    def add(self, key, value=None) -> None:
        with self._item_lock[key]:
            if value:
                self.adj_list[key].append(value)
            else:
                self.adj_list[key]

        del self._item_lock[key]
