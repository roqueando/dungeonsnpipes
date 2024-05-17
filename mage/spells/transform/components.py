def transform_components(batch: list) -> list:
    return list(map(_concat_components, batch))

def _concat_components(spell: dict) -> dict:
    spell['components'] = ', '.join(spell['components'])
    return spell
