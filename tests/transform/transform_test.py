from dungeonsnpipes.extract.api_extractor import DND_API_BASE_URL, get_spells_from_api

from dungeonsnpipes.transform.transform import turn_into_batches
from tests.mocks.spells_mock import get_spells_mock, get_spells_for_batch_mock
from tests.setup.main import TestSuite

def test_turning_into_batches(requests_mock):
    suite = TestSuite()
    suite.mock_spells(requests_mock, get_spells_for_batch_mock)
    spells = get_spells_from_api()

    batches = turn_into_batches(spells)
    first_batch = batches[0]
    second_batch = batches[1]

    assert len(batches) == 2
    assert len(first_batch.spells) == 10
    assert len(second_batch.spells) == 5
