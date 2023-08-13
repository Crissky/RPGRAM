from collections import defaultdict
from random import choice, choices
from typing import Union

from rpgram.boosters import Equipment
from rpgram import Consumable
from rpgram.enums import EquipmentEnum


# CONSTANTS
BONUS_RARITY = {
    'COMMON': 1, 'UNCOMMON': 2, 'RARE': 3,
    'EPIC': 4, 'LEGENDARY': 5, 'MYTHIC': 6,
}
WEAPON_BONUS_MATERIAL = {
    'WOOD': 1, 'IRON': 2, 'STEEL': 3, 'OBSIDIAN': 4,
    'RUNITE': 5, 'MITHRIL': 6, 'ADAMANTIUM': 7,
}
ARMOR_BONUS_MATERIAL = {
    'CLOTH': 1, 'LEATHER': 2, 'IRON': 3, 'STEEL': 4,
    'RUNITE': 5, 'MITHRIL': 6, 'ADAMANTIUM': 7,
}
ACCESSORY_BONUS_MATERIAL = {
    'BRONZE': 1, 'SILVER': 2, 'GOLD': 3,
    'PEARL': 4, 'PLATINUM': 5, 'DIAMOND': 6,
}


# FUNCTIONS
def weighted_choice(**items):
    '''Função que retorna um item escolhido de forma aleatória.
    O item é escolhido de forma aleatória, baseado em sua probabilidade.
    O parâmetro items deve ser um dicionário, em que a chave é o item
    e o valor a propabilidade de ser escolhido.
    '''
    population = list(items.keys())
    weights = items.values()
    return choices(population, weights=weights)[0]


def random_group_level(level):
    min_level = int(level * 0.75)
    max_level = int(level * 1.25) + 1
    new_level = choice(range(min_level, max_level))
    return max(new_level, 1)


def choice_type_item():
    types_item = {
        'CONSUMABLE': 150, 'HELMET': 100, 'ONE_HAND': 100,
        'TWO_HANDS': 100, 'ARMOR': 100, 'BOOTS': 100,
        'RING': 25, 'NECKLACE': 25,
    }
    return weighted_choice(**types_item)


def choice_rarity():
    rarities = {
        'COMMON': 100, 'UNCOMMON': 50, 'RARE': 25,
        'EPIC': 12.5, 'LEGENDARY': 6.25, 'MYTHIC': 3.125,
    }
    return weighted_choice(**rarities)


def choice_weapon_material():
    materials = {
        'WOOD': 320, 'IRON': 160, 'STEEL': 80, 'OBSIDIAN': 40,
        'RUNITE': 20, 'MITHRIL': 10, 'ADAMANTIUM': 5,
    }
    return weighted_choice(**materials)


def choice_armor_material():
    materials = {
        'CLOTH': 320, 'LEATHER': 160, 'IRON': 80, 'STEEL': 40,
        'RUNITE': 20, 'MITHRIL': 10, 'ADAMANTIUM': 5,
    }
    return weighted_choice(**materials)


def choice_accessory_material():
    materials = {
        'BRONZE': 100, 'SILVER': 50, 'GOLD': 25,
        'PEARL': 12.5, 'PLATINUM': 6.25, 'DIAMOND': 3.125,
    }
    return weighted_choice(**materials)


def get_total_bonus(equip_type: str, rarity: str, material: str, group_level: int):
    rarity_bonus = BONUS_RARITY[rarity]
    if equip_type in ['TWO_HANDS', 'ARMOR']:
        equip_type_bonus = 2
    elif equip_type in ['ONE_HAND']:
        equip_type_bonus = 1
    elif equip_type in ['HELMET', 'BOOTS']:
        equip_type_bonus = 0.5
    elif equip_type in ['RING', 'NECKLACE']:
        equip_type_bonus = 0.25

    if equip_type in ['ONE_HAND', 'TWO_HANDS']:
        material_bonus = WEAPON_BONUS_MATERIAL[material]
    elif equip_type == ['HELMET', 'ARMOR', 'BOOTS']:
        material_bonus = ARMOR_BONUS_MATERIAL[material]
    elif equip_type == ['RING', 'NECKLACE']:
        material_bonus = ACCESSORY_BONUS_MATERIAL[material]

    bonus = int(
        (group_level * equip_type_bonus) +
        (group_level * rarity_bonus) +
        (group_level * material_bonus)
    )
    penality = random_group_level(group_level)

    return bonus, penality


def get_consumable():
    ...


def get_attribute_probability(weapon: str):
    if weapon in ['SWORD']:
        attr_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 2, 'bonus_physical_defense': 2,
            'bonus_magical_defense': 2, 'bonus_hit': 5,
            'bonus_evasion': 5,
        }

    return attr_prob


def create_equipment(bonus: int, penality: int, equip_type: str, weapon: str, rarity: str, material: str, group_level: int):
    attr_prob = get_attribute_probability(weapon)
    equipment_dict = defaultdict(int)
    for _ in range(bonus):
        attribute = weighted_choice(**attr_prob)
        equipment_dict[attribute] += 1

    for _ in range(penality):
        attribute = weighted_choice(**attr_prob)
        equipment_dict[attribute] -= 1

    name = f'{rarity.title()} {material.title()} {equip_type.title()} '
    return Equipment(
        name=name,
        equip_type=equip_type,
        requirements={'level': group_level},
        rarity=rarity,
        **equipment_dict
    )


def get_equipment(equip_type: str, group_level: int):
    rarity = choice_rarity()
    weapon = None
    if equip_type in ['ONE_HAND', 'TWO_HANDS']:
        material = choice_weapon_material()
        if equip_type == 'ONE_HAND':
            weapon = choice(['SWORD', 'DAGGER', 'WAND'])
        elif equip_type == 'TWO_HANDS':
            weapon = choice(['GREAT_SWORD', 'BOW', 'STAFF'])
    elif equip_type == ['HELMET', 'ARMOR', 'BOOTS']:
        material = choice_armor_material()
    elif equip_type == ['RING', 'NECKLACE']:
        material = choice_accessory_material()
    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )
    bonus, penality = get_total_bonus(
        equip_type, rarity, material, group_level
    )
    equipment = create_equipment(
        bonus, penality, equip_type, weapon, rarity, material, group_level)


def choice_item(group_level: int) -> Union[Consumable, Equipment]:
    '''Função que retorna um item escolhido de forma aleatória.'''
    group_level = random_group_level(group_level)
    choiced_item = choice_type_item()
    equipment_types = [e.name.lower() for e in EquipmentEnum]
    if choiced_item == 'CONSUMABLE':
        item = get_consumable()
    elif choiced_item in equipment_types:
        item = get_equipment(choiced_item, group_level)

    return item


if __name__ == '__main__':
    from collections import Counter

    def test_count(func):
        print(func.__name__)
        items = []
        for i in range(1000):
            items.append(func())
        result = Counter(items)
        for item in result.most_common():
            print(f'{item[0]}: {item[1]},', end=' ')
        print()
    test_count(choice_type_item)
    test_count(choice_rarity)
    test_count(choice_weapon_material)
    test_count(choice_armor_material)
    test_count(choice_accessory_material)
