import requests
from requests import RequestException

DND_API_BASE_URL = "https://www.dnd5eapi.co/api"

def get_api_spell_index(index: str) -> dict:
    try:
        response = requests.get(f'{DND_API_BASE_URL}/spells/{index}',
                                headers={'Accept': 'application/json'}, data={})
        return response.json()
    except RequestException as e:
        raise SystemExit(e)

def get_spells_from_api() -> dict:
    """
    Get all spells from API to ingest into a data lake
    """
    config = {
        'payload': {},
        'headers': {
            'Accept': 'application/json'
        }
    }
    try:
        response = requests.get(f'{DND_API_BASE_URL}/spells',
            headers=config['headers'], data=config['payload'])
        data = response.json()
        return data
    except RequestException as e:
        raise SystemExit(e)
