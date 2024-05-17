import mage.spells.extract.base as extract
import requests
import tests.mocks.request_mock as request_mock

def test_mage_spells_extract(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spells)
    response = extract.get_spells_from_api()
    assert response['count'] > 0

def test_mage_spell_index(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spell_index)
    response = extract.get_api_spell_index('acid-arrow')

    assert response['desc'][0] == 'A simple description'
    assert response['range'] == '90 feet'
