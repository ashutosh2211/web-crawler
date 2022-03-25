import logging
import traceback
from threading import Thread, Event

logger = logging.getLogger(__name__)


class LoopingThread(Thread):

    def __init__(self, stop_event: Event, target, args=None, kwargs=None, daemon=False):
        super().__init__(target=target, daemon=daemon, args=args or (), kwargs=kwargs or {})
        self._stop_event = stop_event

    def run(self):
        while self._stop_event.is_set():
            try:
                self._target(*self._args, **self._kwargs)
            except Exception as exc:
                traceback.print_exc()
                logger.exception(exc)
