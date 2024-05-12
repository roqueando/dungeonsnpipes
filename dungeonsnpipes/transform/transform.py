from dungeonsnpipes.extract.api_extractor import SpellResponse
import math

class SpellBatch:
    MAX_SIZE = 10
    def __init__(self) -> None:
        self.spells = []


def turn_into_batches(response: SpellResponse) -> list[SpellBatch]:
    """Get the SpellResponse object and create a list of batches"""
    batch_count = math.ceil(response.count / SpellBatch.MAX_SIZE)
    count = 0
    spell_batches = []
    while count < batch_count:
        batch = SpellBatch()
        for spell in response.result[:SpellBatch.MAX_SIZE]:
            batch.spells.append(spell)

        spell_batches.append(batch)
        response.result = response.result[SpellBatch.MAX_SIZE:]
        count += 1

    return spell_batches
