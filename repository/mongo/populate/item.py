from random import choice, choices
from rpgram.enums import EquipmentEnum


def weighted_choice(**items):
    '''Função que retorna um item escolhido de forma aleatória.
    O item é escolhido de forma aleatória, baseado em sua probabilidade.
    O parâmetro items deve ser um dicionário, em que a chave é o item
    e o valor a propabilidade de ser escolhido.
    '''
    population = list(items.keys())
    weights = items.values()
    return choices(population, weights=weights)[0]


def choice_type_item():
    types_item = {
        'consumable': 150,
        'helmet': 100,
        'one_hand': 100,
        'two_hands': 100,
        'armor': 100,
        'boots': 100,
        'ring': 25,
        'necklace': 25,
    }
    return weighted_choice(**types_item)


def choice_rarity():
    rarities = {
        'common': 100,
        'uncommon': 50,
        'rare': 25,
        'epic': 12.5,
        'legendary': 6.25,
        'mythic': 3.125,
    }
    return weighted_choice(**rarities)


def choice_weapon_material():
    materials = {
        'wood': 320,
        'iron': 160,
        'steel': 80,
        'obsidian': 40,
        'runite': 20,
        'mithril': 10,
        'adamantium': 5,
    }
    return weighted_choice(**materials)


def choice_armor_material():
    materials = {
        'cloth': 320,
        'leather': 160,
        'iron': 80,
        'steel': 40,
        'runite': 20,
        'mithril': 10,
        'adamantium': 5,
    }
    return weighted_choice(**materials)


def choice_accessory_material():
    materials = {
        'bronze': 100,
        'silver': 50,
        'gold': 25,
        'pearl': 12.5,
        'platinum': 6.25,
        'diamond': 3.125,
    }
    return weighted_choice(**materials)


def get_consumable():
    ...


def get_equipment(equip_type: str):
    rarity = choice_rarity()
    if equip_type in ['one_hand', 'two_hands']:
        material = choice_weapon_material()
    elif equip_type == ['helmet', 'armor', 'boots']:
        material = choice_armor_material()
    elif equip_type == ['ring', 'necklace']:
        material = choice_accessory_material()
    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )


def choice_item():
    choiced_item = choice_type_item()
    equipment_types = [e.name.lower() for e in EquipmentEnum]
    if choiced_item == 'consumable':
        get_consumable()
    elif choiced_item in equipment_types:
        get_equipment(choiced_item)


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
