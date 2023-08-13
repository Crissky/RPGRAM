from collections import defaultdict
from random import choice, choices
from typing import Union

from rpgram.boosters import Equipment
from rpgram import Consumable
from rpgram.enums import EquipmentEnum


# CONSTANTS
BONUS_RARITY = {
    'common': 1, 'uncommon': 2, 'rare': 3,
    'epic': 4, 'legendary': 5, 'mythic': 6,
}
WEAPON_BONUS_MATERIAL = {
    'wood': 1, 'iron': 2, 'steel': 3, 'obsidian': 4,
    'runite': 5, 'mithril': 6, 'adamantium': 7,
}
ARMOR_BONUS_MATERIAL = {
    'cloth': 1, 'leather': 2, 'iron': 3, 'steel': 4,
    'runite': 5, 'mithril': 6, 'adamantium': 7,
}
ACCESSORY_BONUS_MATERIAL = {
    'bronze': 1, 'silver': 2, 'gold': 3,
    'pearl': 4, 'platinum': 5, 'diamond': 6,
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
        'consumable': 150, 'helmet': 100, 'one_hand': 100,
        'two_hands': 100, 'armor': 100, 'boots': 100,
        'ring': 25, 'necklace': 25,
    }
    return weighted_choice(**types_item)


def choice_rarity():
    rarities = {
        'common': 100, 'uncommon': 50, 'rare': 25,
        'epic': 12.5, 'legendary': 6.25, 'mythic': 3.125,
    }
    return weighted_choice(**rarities)


def choice_weapon_material():
    materials = {
        'wood': 320, 'iron': 160, 'steel': 80, 'obsidian': 40,
        'runite': 20, 'mithril': 10, 'adamantium': 5,
    }
    return weighted_choice(**materials)


def choice_armor_material():
    materials = {
        'cloth': 320, 'leather': 160, 'iron': 80, 'steel': 40,
        'runite': 20, 'mithril': 10, 'adamantium': 5,
    }
    return weighted_choice(**materials)


def choice_accessory_material():
    materials = {
        'bronze': 100, 'silver': 50, 'gold': 25,
        'pearl': 12.5, 'platinum': 6.25, 'diamond': 3.125,
    }
    return weighted_choice(**materials)


def get_total_bonus(equip_type: str, rarity: str, material: str, group_level: int):
    rarity_bonus = BONUS_RARITY[rarity]
    if equip_type in ['two_hands', 'armor']:
        equip_type_bonus = 2
    elif equip_type in ['one_hand']:
        equip_type_bonus = 1
    elif equip_type in ['helmet', 'boots']:
        equip_type_bonus = 0.5
    elif equip_type in ['ring', 'necklace']:
        equip_type_bonus = 0.25

    if equip_type in ['one_hand', 'two_hands']:
        material_bonus = WEAPON_BONUS_MATERIAL[material]
    elif equip_type == ['helmet', 'armor', 'boots']:
        material_bonus = ARMOR_BONUS_MATERIAL[material]
    elif equip_type == ['ring', 'necklace']:
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


def get_attribute_probability(equip_type: str):
    if equip_type in ['sword']:
        attr_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 2, 'bonus_physical_defense': 2,
            'bonus_magical_defense': 2, 'bonus_hit': 5,
            'bonus_evasion': 5,
        }

    return attr_prob


def create_equipment(bonus: int, penality: int, equip_type: str, rarity: str, material: str, group_level: int):
    attr_prob = get_attribute_probability(equip_type)
    equipment_dict = defaultdict(int)
    for i in range(bonus):
        attribute = weighted_choice(**attr_prob)
        equipment_dict[attribute] += 1

    for i in range(penality):
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
    if equip_type in ['one_hand', 'two_hands']:
        material = choice_weapon_material()
        if equip_type == 'one_hand':
            weapon = choice(['sword', 'dagger', 'wand'])
        elif equip_type == 'two_hands':
            weapon = choice(['great sword', 'bow', 'staff'])
    elif equip_type == ['helmet', 'armor', 'boots']:
        material = choice_armor_material()
    elif equip_type == ['ring', 'necklace']:
        material = choice_accessory_material()
    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )
    bonus, penality = get_total_bonus(
        equip_type, rarity, material, group_level
    )
    if weapon:
        equip_type = weapon
    equipment = create_equipment(
        bonus, penality, equip_type, rarity, material, group_level)


def choice_item(group_level: int) -> Union[Consumable, Equipment]:
    '''Função que retorna um item escolhido de forma aleatória.'''
    group_level = random_group_level(group_level)
    choiced_item = choice_type_item()
    equipment_types = [e.name.lower() for e in EquipmentEnum]
    if choiced_item == 'consumable':
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
