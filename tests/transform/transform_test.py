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


def test_all_transformation(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)
    spells = __create_spell_response()

    batches = transform.turn_into_batches(spells)
    solved_batches = []
    for batch in batches:
        result = transform.transform_description(batch)
        solved_batches.append(result)

    first_result = solved_batches[0][0]

    def it_should_test_description_transform():
        assert first_result['description'] == "A simple description\nMore description"
        assert first_result['higher_level'] == "Higher level description\nMore description"

    it_should_test_description_transform()


def __create_spell_response() -> SpellResponse:
    batch_mock = json.loads(get_spells_for_batch_mock())
    response = SpellResponse(
        count=batch_mock['count'], result=batch_mock['results'])
    return response
