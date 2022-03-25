from abc import ABC, abstractmethod


class Worker(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError("An implementation of this class is needed")
