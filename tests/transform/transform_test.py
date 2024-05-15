import dungeonsnpipes.extract.api_extractor as api_extractor
from dungeonsnpipes.extract.api_extractor import SpellResponse
import dungeonsnpipes.transform.transform as transform
from tests.mocks.spells_mock import get_spells_for_batch_mock
import json
import requests
import tests.mocks.request_mock as request_mock


def test_turning_into_batches(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spells_batch)
    spells = api_extractor.get_spells_from_api()

    batches = transform.turn_into_batches(spells)
    first_batch = batches[0]
    second_batch = batches[1]

    assert len(batches) == 2
    assert len(first_batch.spells) == 10
    assert len(second_batch.spells) == 5


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


def test_transformer(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)
    spells = __create_spell_response()
    batches = transform.turn_into_batches(spells)
    solved = []
    for batch in batches:
        new_batch = transform.Transformer(batch=batch.spells) \
            .apply(transform.transform_description) \
            .apply(transform.transform_components) \
            .apply(transform.transform_range) \
            .apply(transform.transform_damage)
        solved += new_batch.batch

    should_description_be_transformed(solved[0])
    should_range_be_transformed(solved[0])
    should_components_be_transformed(solved[0])
    should_damage_be_transformed(solved[0])


def __create_spell_response() -> SpellResponse:
    batch_mock = json.loads(get_spells_for_batch_mock())
    response = SpellResponse(
        count=batch_mock['count'], result=batch_mock['results'])
    return response
