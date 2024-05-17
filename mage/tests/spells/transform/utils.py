import json
from tests.mocks.spells_mock import get_spells_for_batch_mock


def create_spell_response() -> dict:
    batch_mock = json.loads(get_spells_for_batch_mock())
    response = {
        'count': batch_mock['count'],
        'results': batch_mock['results'],
    }
    return response
