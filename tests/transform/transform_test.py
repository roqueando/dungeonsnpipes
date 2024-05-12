from dungeonsnpipes.extract.api_extractor import DND_API_BASE_URL

from dungeonsnpipes.transform.transform import turn_into_batches
from tests.mocks.spells_mock import get_spells_mock

def test_turning_into_batches(requests_mock):
    requests_mock.get(f'{DND_API_BASE_URL}/spells', status_code=200, text=get_spells_for_batch_mock())
    response = get_spells_from_api()
    batches = turn_into_batches(response)
    first_batch = batches[0]
    second_batch = batches[1]

    assert len(batches) == 2
    assert len(first_batch.spells) == 10
    assert len(second_batch.spells) == 5
