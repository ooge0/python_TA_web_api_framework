from enum import Enum


class BaseLocators(Enum):
    def __str__(self):
        return self.value
