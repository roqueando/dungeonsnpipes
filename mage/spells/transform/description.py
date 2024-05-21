import requests
from requests import RequestException

def transform_description(spell: dict) -> dict:
    spell['description'] = '\n'.join(spell['desc'])
    spell['higher_level_description'] = '\n'.join(spell['higher_level'])

    del spell['desc']
    del spell['higher_level']
    return spell
