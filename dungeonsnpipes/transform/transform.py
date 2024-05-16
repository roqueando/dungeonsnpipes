from typing import Callable
from dungeonsnpipes.extract.api_extractor import SpellResponse, get_api_spell_index
from dataclasses import dataclass
from multiprocessing import Process
import math

FEET_CONSTANT = 3.2808
SQUARE_METERS = 1.5


class SpellBatch:
    MAX_SIZE = 30

    def __init__(self) -> None:
        self.spells: list[SpellResponse] = []

@dataclass
class Transformer:
    batch: list

    def apply(self, func: Callable):
        self.batch = func(self.batch)
        return self

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


def transform_description(batch: list) -> list:
    return list(map(_concat_descriptions, batch))

def transform_range(batch: list) -> list:
    return list(map(_calculate_range, batch))


def transform_components(batch: list) -> list:
    return list(map(_concat_components, batch))


def transform_damage(batch: list) -> list:
    return list(map(_flatten_damage, batch))


def total_damage(value: str) -> int:
    multi, dice = value.split("d")
    return int(multi) * int(dice)

def _concat_descriptions(spell: dict) -> dict:
    try:
        api_spell = get_api_spell_index(spell['index'])
        resource = {**api_spell}
        resource['description'] = '\n'.join(api_spell['desc'])
        resource['higher_level_description'] = '\n'.join(
            api_spell['higher_level'])
        del resource['desc']
        del resource['higher_level']
        return resource
    except:
        raise Exception("Request goes wrong")

def _flatten_damage(spell: dict) -> dict:
    if not 'damage' in spell and not 'damage_at_slot_level' in spell:
        spell['damage'] = 'No damage'
        spell['total_damage_scale'] = []
        return spell

    level = spell['level']
    damage_type = spell['damage']['damage_type']['name']
    dice = spell['damage']['damage_at_slot_level'][str(level)]

    spell['total_damage_scale'] = [total_damage(
        v) for _, v in spell['damage']['damage_at_slot_level'].items()]
    spell['damage'] = f'{dice} of {damage_type} damage'
    return spell


def _concat_components(spell: dict) -> dict:
    spell['components'] = ', '.join(spell['components'])
    return spell

def _calculate_range(spell: dict) -> dict:
    match spell['range']:
        case 'Touch' | 'Self':
            spell['squares'] = 1
        case 'Special' | 'Sight' | 'Unlimited':
            spell['squares'] = 999
        case _:
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
