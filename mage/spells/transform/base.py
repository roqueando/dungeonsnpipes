from dataclasses import dataclass
from typing import Callable

FEET_CONSTANT = 3.2808
SQUARE_METERS = 1.5


@dataclass
class SpellBatch:
    MAX_SIZE = 30


@dataclass
class Transformer:
    batch: list

    def apply(self, func: Callable):
        self.batch = func(self.batch)
        return self
