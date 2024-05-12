from typing import Dict
from requests import RequestException, request
import json

DND_API_BASE_URL = "https://www.dnd5eapi.co/api"

class SpellResponse:
    def __init__(self, count: int, result: object) -> None:
        self.count = count
        self.result = result

def get_spells_from_api() -> SpellResponse:
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
        response = request(
                "GET", f'{DND_API_BASE_URL}/spells',
                headers=config['headers'], data=config['payload'])
        data = response.json()
        return SpellResponse(
                count=data['count'],
                result=data['results'])
    except RequestException as e:
        raise SystemExit(e)
