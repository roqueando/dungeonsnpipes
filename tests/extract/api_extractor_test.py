import dungeonsnpipes.extract.api_extractor as api_extractor
import tests.mocks.request_mock as request_mock
import requests


def test_api_extractor_get_spells_from_api(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spells)
    response = api_extractor.get_spells_from_api()
    assert response.count > 0


def test_get_spells_from_index(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)
    response = api_extractor.get_api_spell_index('acid-arrow')

    assert response['desc'][0] == 'A simple description'
    assert response['range'] == '90 feet'
