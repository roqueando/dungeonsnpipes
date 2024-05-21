import itertools


def group_by_level(batch: list) -> list:
    groups = {}
    for key, g in itertools.groupby(batch, lambda x: x['level']):
        spells = ", ".join(list(map(lambda x: x['name'], list(g))))
        print(f'level {key}: \n{spells}')
        groups[str(key)] = list(g)

    return groups
