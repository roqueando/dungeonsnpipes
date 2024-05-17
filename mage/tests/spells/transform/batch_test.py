import requests
import tests.mocks.request_mock as request_mock
import mage.spells.extract.base as extract
import mage.spells.transform.base as transform
import mage.spells.transform.batch as transform_batch


def test_turn_into_batches(monkeypatch):
    monkeypatch.setattr(requests, "get", request_mock.mock_get_spells_batch)
    spells = extract.get_spells_from_api()
    transform.SpellBatch.MAX_SIZE = 10
    batches = transform_batch.turn_into_batches(spells)

    first_batch = batches[0]
    second_batch = batches[1]

    assert len(batches) == 2
    assert len(first_batch['spells']) == 10
    assert len(second_batch['spells']) == 5
