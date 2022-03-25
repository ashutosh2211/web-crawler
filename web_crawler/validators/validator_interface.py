from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):

    @abstractmethod
    def validate(self, elem: Any) -> bool:
        raise NotImplementedError("An implementation of this class is needed")
