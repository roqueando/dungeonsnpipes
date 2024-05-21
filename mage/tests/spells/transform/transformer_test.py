# from .utils import create_spell_response
import json
import requests
import tests.mocks.spells_mock as spells_mock
from tests.mocks.spells_mock import get_spells_for_batch_mock
import mage.spells.transform.batch as transform_batch
import mage.spells.transform.base as base
import mage.spells.transform.description as description
import mage.spells.transform.components as components
import mage.spells.transform.range as transform_range
import mage.spells.transform.damage as damage
import mage.spells.transform.grouping as grouping


def create_spell_response() -> dict:
    batch_mock = json.loads(get_spells_for_batch_mock())
    response = {
        'count': batch_mock['count'],
        'results': batch_mock['results'],
    }
    return response


def test_transformer_damage_at_character_level():
    spell = json.loads(spells_mock.get_spell_index_mock_at_character_level())
    transformer = base.Transformer(spell=spell) \
        .apply(description.transform_description) \
        .apply(components.transform_components) \
        .apply(transform_range.transform_range) \
        .apply(damage.transform_damage)

    assert transformer.spell['damage'] == '1=1d6, 5=2d6, 11=3d6, 17=4d6 of Acid damage'
    assert transformer.spell['total_damage_scale'] == [6, 12, 18, 24]

def test_transformer():
    spell = json.loads(spells_mock.get_spell_index_mock())
    transformer = base.Transformer(spell=spell) \
        .apply(description.transform_description) \
        .apply(components.transform_components) \
        .apply(transform_range.transform_range) \
        .apply(damage.transform_damage)


    assert transformer.spell['description'] == "A simple description\nMore description"
    assert transformer.spell['higher_level_description'] == "Higher level description\nMore description"
    assert transformer.spell['squares'] == 18
    assert transformer.spell['components'] == "V, S, M"
    assert transformer.spell['damage'] == '4d4 of Acid damage'
    assert transformer.spell['total_damage_scale'] == [
        16, 20, 24, 28, 32, 36, 40, 44
    ]

