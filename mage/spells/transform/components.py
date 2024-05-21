def transform_components(spell: dict) -> dict:
    spell['components'] = ', '.join(spell['components'])
    return spell
