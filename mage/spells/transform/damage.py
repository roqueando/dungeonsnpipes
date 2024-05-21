def transform_damage(spell: dict) -> dict:
    if not 'damage' in spell:
        spell['damage'] = 'No damage'
        spell['total_damage_scale'] = []
        return spell

    if not 'damage_type' in spell['damage']:
        damage_type = 'Neutral'
    else:
        damage_type = spell['damage']['damage_type']['name']

    level = spell['level']
    dice = ''

    if 'damage_at_slot_level' in spell['damage']:
        dice = spell['damage']['damage_at_slot_level'][str(level)]
        spell['total_damage_scale'] = total_damage_at_scale(spell, 'damage_at_slot_level')
        spell['damage'] = f'{dice} of {damage_type} damage'
        return spell

    if 'damage_at_character_level' in spell['damage']:
        spell['total_damage_scale'] = total_damage_at_scale(spell, 'damage_at_character_level')
        dice_list = [f'{level_dice}={spell_dice}' for level_dice, spell_dice in spell['damage']['damage_at_character_level'].items()]
        spell['damage'] = f'{", ".join(dice_list)} of {damage_type} damage'
        return spell

    return spell


def total_damage_at_scale(spell:dict, index: str) -> list[int]:
    return [total_damage(v) for _, v in spell['damage'][index].items()]

def total_damage(value: str) -> int:
    if '+' in value:
        roll, summatory = value.split("+")
        multi, dice = roll.split('d')
        if 'd' in summatory:
            multi_sum, dice_sum = summatory.split('d')
            first = int(multi) * int(dice)
            second = int(multi_sum) * int(dice_sum)
            return first + second

        if 'd' not in summatory or '+' not in summatory:
            return int(multi) * int(dice)

        return (int(multi) * int(dice)) + int(summatory)

    if 'd' not in value:
        return int(value)

    multi, dice = value.split("d")
    return int(multi) * int(dice)
