from dataclasses import dataclass
from typing import Callable

FEET_CONSTANT = 3.2808
SQUARE_METERS = 1.5
ACCESS_KEY = '2w7Xan3d6L3gVumemkC3'
SECRET_KEY = 'wpjikukgZYot8iFjf7UxpuMeElqbLWha1h74G5Tv'


@dataclass
class SpellBatch:
    MAX_SIZE = 30


@dataclass
class Transformer:
    spell: dict

    def apply(self, func: Callable):
        self.spell = func(self.spell)
        return self
