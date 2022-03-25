import time
from threading import Event

from web_crawler.loop_thread import LoopingThread


class TestLoopingThread:

    def test_run_with_signal(self):
        signal: Event = Event()

        threads = []
        for _ in range(3):
            threads.append(LoopingThread(signal, lambda: _))

        signal.set()
        for t in threads:
            t.start()

        time.sleep(2)

        assert all(thread.is_alive() for thread in threads)

        signal.clear()

        time.sleep(2)

        assert not (any(thread.is_alive() for thread in threads))

    def test_run_with_exception(self, caplog):

        def _raise(exc):
            raise exc

        signal: Event = Event()

        threads = []
        for _ in range(3):
            threads.append(LoopingThread(signal, lambda: _raise(ValueError())))

        signal.set()
        for t in threads:
            t.start()

        time.sleep(1)
        signal.clear()

        for record in caplog.records:
            assert record.exc_info[0] == ValueError
