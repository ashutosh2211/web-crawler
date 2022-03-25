from threading import Thread

import pytest

from web_crawler.locked_set import LockedSet


@pytest.fixture(scope="class")
def locked_set():
    return LockedSet()


def add_to_locked_set(ls: LockedSet):
    for i in range(3):
        ls.add(i)


class TestLockedSet:

    def test_locked_set_add(self, locked_set: LockedSet):

        threads = []
        for _ in range(3):
            threads.append(Thread(target=add_to_locked_set, args=(locked_set,)))

        for t in threads:
            t.start()
            t.join()

        for i in range(0, 3):
            assert locked_set.contains(i)

    def test_contains(self, locked_set: LockedSet):

        vals = [1, 2, 3]
        locked_set = locked_set.set(vals)

        for i in vals:
            assert locked_set.contains(i)
