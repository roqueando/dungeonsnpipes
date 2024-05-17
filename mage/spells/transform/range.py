import math
from .base import FEET_CONSTANT, SQUARE_METERS

def transform_range(batch: list) -> list:
    return list(map(_calculate_range, batch))

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

