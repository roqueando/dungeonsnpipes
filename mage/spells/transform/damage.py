def transform_damage(batch: list) -> list:
    return list(map(_flatten_damage, batch))


def _flatten_damage(spell: dict) -> dict:
    if not 'damage' in spell and not 'damage_at_slot_level' in spell:
        spell['damage'] = 'No damage'
        spell['total_damage_scale'] = []
        return spell

    level = spell['level']
    damage_type = spell['damage']['damage_type']['name']
    dice = spell['damage']['damage_at_slot_level'][str(level)]

    spell['total_damage_scale'] = [total_damage(
        v) for _, v in spell['damage']['damage_at_slot_level'].items()]
    spell['damage'] = f'{dice} of {damage_type} damage'
    return spell


def total_damage(value: str) -> int:
    multi, dice = value.split("d")
    return int(multi) * int(dice)
