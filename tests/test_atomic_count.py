from threading import Thread

import pytest

from web_crawler.atomic_count import AtomicInteger


@pytest.fixture(scope="class")
def atomic_int_fixture():
    return AtomicInteger()


class TestAtomicInteger:

    def test_increment(self, atomic_int_fixture: AtomicInteger):

        def func(atomic_int: AtomicInteger):
            for i in range(3):
                atomic_int.inc()

        threads = []
        for _ in range(3):
            threads.append(Thread(target=func, args=(atomic_int_fixture,)))

        for t in threads:
            t.start()
            t.join()

        assert atomic_int_fixture.value == 9

    def test_decrement(self):

        def func(atomic_int: AtomicInteger):
            for i in range(3):
                atomic_int.dec()

        atomic_int = AtomicInteger(10)

        threads = []
        for _ in range(2):
            threads.append(Thread(target=func, args=(atomic_int,)))

        for t in threads:
            t.start()
            t.join()

        assert atomic_int.value == 4
