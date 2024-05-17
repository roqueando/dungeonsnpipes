from mage.spells.extract.base import get_api_spell_index


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
