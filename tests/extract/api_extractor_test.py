from dungeonsnpipes.extract.api_extractor import get_spells_from_api, DND_API_BASE_URL

from tests.mocks.spells_mock import get_spells_mock

def test_api_extractor_get_spells_from_api(requests_mock):
    requests_mock.get(f'{DND_API_BASE_URL}/spells', status_code=200, text=get_spells_mock())
    response = get_spells_from_api()
    assert response.count > 0
