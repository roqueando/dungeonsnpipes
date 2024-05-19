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


def transform_description(batch: list) -> list:
    return list(map(_concat_descriptions, batch))


def _concat_descriptions(spell: dict) -> dict:
    try:
        api_spell = get_api_spell_index(spell['index'])
        resource = {**api_spell}
        resource['description'] = '\n'.join(api_spell['desc'])
        resource['higher_level_description'] = '\n'.join(
            api_spell['higher_level'])
        del resource['desc']
        del resource['higher_level']
        return resource
    except:
        raise Exception("Request goes wrong")
