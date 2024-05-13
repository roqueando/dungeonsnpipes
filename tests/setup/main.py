from dungeonsnpipes.extract.api_extractor import DND_API_BASE_URL, SpellResponse, get_spells_from_api
from typing import Callable
from requests_mock import ANY


class TestSuite:
    __test__ = False

    def __init__(self):
        self.uri = f'{DND_API_BASE_URL}/spells'

    def mock_spells(self, requests_mock, mock: Callable[[], str]) -> None:
        requests_mock.get(f'{DND_API_BASE_URL}/spells', status_code=200,
                          text=mock())

    def mock_spell_index(self, requests_mock, mock: Callable[[], str]) -> None:
        requests_mock.get(ANY,
                          status_code=200, text=mock())
