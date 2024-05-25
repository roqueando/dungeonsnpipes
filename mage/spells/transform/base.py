from dataclasses import dataclass
from typing import Callable

FEET_CONSTANT = 3.2808
SQUARE_METERS = 1.5


@dataclass
class SpellBatch:
    MAX_SIZE = 30


@dataclass
class Transformer:
    spell: dict

    def apply(self, func: Callable):
        self.spell = func(self.spell)
        return self
