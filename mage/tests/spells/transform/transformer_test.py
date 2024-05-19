# from .utils import create_spell_response
import json
import requests
import tests.mocks.request_mock as request_mock
from tests.mocks.spells_mock import get_spells_for_batch_mock
import mage.spells.transform.batch as transform_batch
import mage.spells.transform.base as base
import mage.spells.transform.description as description
import mage.spells.transform.components as components
import mage.spells.transform.range as range
import mage.spells.transform.damage as damage
import mage.spells.transform.grouping as grouping


def create_spell_response() -> dict:
    batch_mock = json.loads(get_spells_for_batch_mock())
    response = {
        'count': batch_mock['count'],
        'results': batch_mock['results'],
    }
    return response


def test_transformer(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)

    spells = create_spell_response()
    batches = transform_batch.turn_into_batches(spells)

    solved = []
    for batch in batches:
        new_batch = base.Transformer(batch=batch['spells']) \
            .apply(description.transform_description) \
            .apply(components.transform_components) \
            .apply(range.transform_range) \
            .apply(damage.transform_damage) \
            .apply(grouping.group_by_level)

        solved += new_batch.batch

    should_group_by_level(solved[0])
    should_description_be_transformed(solved[0][2][0])
    should_range_be_transformed(solved[0][2][0])
    should_components_be_transformed(solved[0][2][0])
    should_damage_be_transformed(solved[0][2][0])


def should_group_by_level(batch):
    assert len(batch) == 1
    assert 2 in batch
    assert True == True


def should_description_be_transformed(batch):
    assert batch['description'] == "A simple description\nMore description"
    assert batch['higher_level_description'] == "Higher level description\nMore description"


def should_range_be_transformed(batch):
    assert batch['squares'] == 18


def should_components_be_transformed(batch):
    assert batch['components'] == "V, S, M"


def should_damage_be_transformed(batch):
    assert batch['damage'] == '4d4 of Acid damage'
    assert batch['total_damage_scale'] == [
        16, 20, 24, 28, 32, 36, 40, 44
    ]
