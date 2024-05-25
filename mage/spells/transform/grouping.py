import itertools


def group_by_level(batch: list) -> list:
    groups = []
    for key, g in itertools.groupby(batch, lambda x: x['level']):
        groups.append({str(key): list(g)})

    return groups
