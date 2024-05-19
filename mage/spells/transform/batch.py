import math
from . import base
# from base import SpellBatch


def turn_into_batches(response: dict) -> list:
    """Get the SpellResponse object and create a list of batches"""

    batch_count = math.ceil(response['count'] / base.SpellBatch.MAX_SIZE)
    count = 0
    spell_batches = []
    while count < batch_count:
        batch = {'spells': []}
        for spell in response['results'][:base.SpellBatch.MAX_SIZE]:
            batch['spells'].append(spell)

        spell_batches.append(batch)
        response['results'] = response['results'][base.SpellBatch.MAX_SIZE:]
        count += 1

    return spell_batches
