def drop_unused(spell: dict) -> dict:
    del spell['school']
    del spell['classes']
    del spell['subclasses']
    if 'dc' in spell:
        del spell['dc']

    return spell
