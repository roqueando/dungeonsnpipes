from dungeonsnpipes.extract.api_extractor import SpellResponse, get_api_spell_index
from multiprocessing import Process
import math

FEET_CONSTANT = 3.2808
SQUARE_METERS = 1.5

class SpellBatch:
    MAX_SIZE = 10

    def __init__(self) -> None:
        self.spells: list[SpellResponse] = []


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


def transform_description(batch: SpellBatch) -> list:
    spell_resources = []
    for spell in batch.spells:
        try:
            api_spell = get_api_spell_index(spell['index'])
            resource = {**api_spell}
            resource['description'] = '\n'.join(api_spell['desc'])
            resource['higher_level_description'] = '\n'.join(api_spell['higher_level'])
            del resource['desc']
            del resource['higher_level']
            spell_resources.append(resource)
        except:
            raise Exception("Request goes wrong")

    return spell_resources


def transform_range(batch: list) -> list:
    return list(map(_calculate_range, batch))

def _calculate_range(spell: dict) -> dict:
    meters = round(int(spell['range'].split(' ')[0]) / FEET_CONSTANT, 2)
    spell['squares'] = math.floor(meters / SQUARE_METERS)
    del spell['range']
    return spell

def run_batches(batches: list[SpellBatch]):
    processes = []
    for batch in batches:
        proc = Process(target=transform_description, args=(batch,))
        proc.start()
        processes.append(proc)

    for process in processes:
        result = process.join()
        # print(result)
