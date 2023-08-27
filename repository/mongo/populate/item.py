from bson import ObjectId
from collections import defaultdict
from random import choice, choices, random, randint
from typing import Dict, Hashable, Tuple, Union
from repository.mongo import ItemModel

from rpgram.boosters import Equipment
from rpgram import Consumable
from rpgram.enums import EquipmentEnum, DamageEnum
from rpgram import Item


# CONSTANTS
BONUS_RARITY = {
    'COMMON': 1, 'UNCOMMON': 2, 'RARE': 3,
    'EPIC': 4, 'LEGENDARY': 5, 'MYTHIC': 6,
}
WEAPON_BONUS_MATERIAL = {
    material: multiplier+1
    for multiplier, material in enumerate([
        'WOOD', 'BONE', 'COPPER', 'IRON', 'STEEL', 'OBSIDIAN',
        'RUNITE', 'MITHRIL', 'ADAMANTIUM',
    ])
}
ARMOR_BONUS_MATERIAL = {
    material: multiplier+1
    for multiplier, material in enumerate([
        'CLOTH', 'LEATHER', 'BONE', 'COPPER', 'IRON', 'STEEL',
        'RUNITE', 'MITHRIL', 'ADAMANTIUM',
    ])
}
ACCESSORY_BONUS_MATERIAL = {
    material: multiplier+1
    for multiplier, material in enumerate([
        'BRONZE', 'SILVER', 'GOLD',
        'PEARL', 'PLATINUM', 'DIAMOND',
    ])
}


# FUNCTIONS
def weighted_choice(**items) -> Hashable:
    '''Função que retorna um item escolhido de forma aleatória.
    O item é escolhido de forma aleatória, baseado em sua probabilidade.
    O parâmetro items deve ser um dicionário, em que a chave é o item
    e o valor a propabilidade de ser escolhido.
    '''
    population = list(items.keys())
    weights = items.values()
    return choices(population, weights=weights)[0]


def random_group_level(level: int) -> int:
    min_level = int(level * 0.75)
    max_level = int(level * 1.25) + 1
    new_level = choice(range(min_level, max_level))
    return max(new_level, 1)


def choice_type_item() -> str:
    types_item = {
        'CONSUMABLE': 1000, 'HELMET': 100, 'ONE_HAND': 120,
        'TWO_HANDS': 120, 'ARMOR': 100, 'BOOTS': 100,
        'RING': 25, 'NECKLACE': 25,
    }
    return weighted_choice(**types_item)


def choice_rarity(group_level: int) -> str:
    rarities = {'COMMON': 100, 'UNCOMMON': 50}
    if group_level >= 50:
        rarities['RARE'] = 25
    if group_level >= 100:
        rarities['EPIC'] = 12.5
    if group_level >= 250:
        rarities['LEGENDARY'] = 6.25
    if group_level >= 500:
        rarities['MYTHIC'] = 3.125

    return weighted_choice(**rarities)


def choice_weapon_material(group_level: int) -> str:
    materials = {}
    level_base = 25
    chance = 100 + (len(WEAPON_BONUS_MATERIAL) * 25)
    for material, multiplier in WEAPON_BONUS_MATERIAL.items():
        level_threshold = level_base * multiplier
        if group_level >= level_threshold or not materials:
            materials[material] = chance
            chance -= 25

    return weighted_choice(**materials)


def choice_armor_material(group_level: int) -> str:
    materials = {}
    level_base = 25
    chance = 100 + (len(ARMOR_BONUS_MATERIAL) * 25)
    for material, multiplier in ARMOR_BONUS_MATERIAL.items():
        level_threshold = level_base * multiplier
        if group_level >= level_threshold or not materials:
            materials[material] = chance
            chance -= 25

    return weighted_choice(**materials)


def choice_accessory_material(group_level: int) -> str:
    materials = {}
    level_base = 50
    chance = 100 + (len(ACCESSORY_BONUS_MATERIAL) * 25)
    for material, multiplier in ACCESSORY_BONUS_MATERIAL.items():
        level_threshold = level_base * multiplier
        if group_level >= level_threshold or not materials:
            materials[material] = chance
            chance -= 25

    return weighted_choice(**materials)


def get_weapon_material(equip_type: str, group_level: int) -> Tuple[str, str]:
    weapon = None
    if equip_type in ['ONE_HAND', 'TWO_HANDS']:
        material = choice_weapon_material(group_level)
        if equip_type == 'ONE_HAND':
            weapon = choice(['SWORD', 'DAGGER', 'WAND', 'SHIELD'])
        elif equip_type == 'TWO_HANDS':
            weapon = choice(['GREAT_SWORD', 'BOW', 'STAFF'])
    elif equip_type in ['HELMET', 'ARMOR', 'BOOTS']:
        material = choice_armor_material(group_level)
    elif equip_type in ['RING', 'NECKLACE']:
        material = choice_accessory_material(group_level)
    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )

    return weapon, material


def get_bonus_penality(equip_type: str, rarity: str, material: str, group_level: int, verbose: bool = False) -> Tuple[int, int]:
    rarity_bonus = BONUS_RARITY[rarity]
    if equip_type in ['TWO_HANDS', 'ARMOR']:
        equip_type_bonus = 2.5
    elif equip_type in ['ONE_HAND']:
        equip_type_bonus = 1
    elif equip_type in ['HELMET', 'BOOTS']:
        equip_type_bonus = 0.5
    elif equip_type in ['RING', 'NECKLACE']:
        equip_type_bonus = 0.25

    if equip_type in ['ONE_HAND', 'TWO_HANDS']:
        material_bonus = WEAPON_BONUS_MATERIAL[material]
    elif equip_type in ['HELMET', 'ARMOR', 'BOOTS']:
        material_bonus = ARMOR_BONUS_MATERIAL[material]
    elif equip_type in ['RING', 'NECKLACE']:
        material_bonus = ACCESSORY_BONUS_MATERIAL[material]

    bonus = int(
        (group_level * equip_type_bonus) +
        (group_level * rarity_bonus) +
        (group_level * material_bonus)
    )
    penality = random_group_level(group_level)
    if verbose:
        print(
            f'Level: {group_level}, '
            f'Equipamento: {equip_type}({equip_type_bonus}), '
            f'Raridade: {rarity}({rarity_bonus}), '
            f'Material: {material}({material_bonus}), '
            f'Bônus: {bonus}, Penalidade: {penality}'
        )

    return bonus, penality


def create_random_consumable(group_level: int):
    item_model = ItemModel()
    rarity = choice_rarity(group_level)
    query = dict(rarity=rarity, _class='Consumable')
    item_list = item_model.get_all(query=query)
    quantity = randint(1, 5)
    item = choice(item_list)
    item = Item(item, quantity)

    return item


def get_attribute_probabilities(weapon: str) -> Dict[str, int]:
    if weapon == 'SWORD':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 3,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 10,
        }
    elif weapon == 'DAGGER':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 7,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    elif weapon == 'WAND':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 2,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 3, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    elif weapon == 'SHIELD':
        attr_bonus_prob = {
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 7, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
    elif weapon == 'GREAT_SWORD':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    elif weapon == 'BOW':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 3,
        }
    elif weapon == 'STAFF':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 3, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    elif weapon == 'HELMET':
        attr_bonus_prob = {
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 7, 'bonus_hit': 1,
            'bonus_evasion': 3,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    elif weapon == 'ARMOR':
        attr_bonus_prob = {
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    elif weapon == 'BOOTS':
        attr_bonus_prob = {
            'bonus_hit_points': 3, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 3, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    elif weapon == 'RING':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    elif weapon == 'NECKLACE':
        attr_bonus_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
        attr_panality_prob = {
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    else:
        raise ValueError(f'"{weapon}" não é um tipo de equipamento válido.')

    return attr_bonus_prob, attr_panality_prob


def get_equipment_weight(equip_type, rarity, material, weapon) -> float:
    weight, _ = get_bonus_penality(equip_type, rarity, material, 5)
    if weapon in ['GREAT_SWORD', 'SHIELD']:
        weight *= 2
    elif equip_type in ['ARMOR']:
        weight *= 3
    elif equip_type in ['RING', 'NECKLACE']:
        weight /= 10

    return weight


def get_equipment_damage_type(weapon: str, rarity: str):
    damage_types = None
    if weapon:
        damage_types = []
        chance = .5
        turns = BONUS_RARITY[rarity] - 1
        damages_list = [
            e.name for e in DamageEnum
            if e not in [DamageEnum.SLASHING, DamageEnum.BLUDGEONING,
                         DamageEnum.HITTING, DamageEnum.PIERCING]
        ]
        if weapon in ['SWORD', 'DAGGER', 'GREAT_SWORD']:
            damage_types = [DamageEnum.SLASHING]
        elif weapon in ['SHIELD', 'STAFF']:
            damage_types = [DamageEnum.BLUDGEONING]
        elif weapon in ['BOW']:
            damage_types = [DamageEnum.PIERCING]
        elif weapon in ['WAND']:
            damage_types = [DamageEnum.MAGIC]
            damages_list.remove(DamageEnum.MAGIC.name)

        if weapon in ['WAND', 'STAFF']:
            turns += 1
            chance = .9

        for _ in range(turns):
            if random() <= chance:
                new_damage = choice(damages_list)
                damages_list.remove(new_damage)
                damage_types.append(new_damage)
                chance /= 2

    return damage_types


def add_secret_stats(equipment_dict: dict, rarity: str, group_level: int):
    secret_stats = defaultdict(int)
    bonus = BONUS_RARITY[rarity] - 2
    bonus = max(bonus, 0) * (group_level // 2)
    attr_probs = {}
    secret_base_stats = [
        'secret_bonus_strength', 'secret_bonus_dexterity',
        'secret_bonus_constitution', 'secret_bonus_intelligence',
        'secret_bonus_wisdom', 'secret_bonus_charisma',
    ]
    secret_mutiplier_base_stats = [
        'secret_multiplier_strength', 'secret_multiplier_dexterity',
        'secret_multiplier_constitution', 'secret_multiplier_intelligence',
        'secret_multiplier_wisdom', 'secret_multiplier_charisma',
    ]
    secret_combat_stats = [
        'secret_bonus_hit_points', 'secret_bonus_initiative',
        'secret_bonus_physical_attack', 'secret_bonus_precision_attack',
        'secret_bonus_magical_attack', 'secret_bonus_physical_defense',
        'secret_bonus_magical_defense', 'secret_bonus_hit',
        'secret_bonus_evasion'
    ]

    # Limita a quantidade de atributos que receberão os bonus.
    for _ in range(len(secret_base_stats) // 2):
        attribute = choice(secret_base_stats)
        attr_probs[attribute] = 100
    for _ in range(len(secret_mutiplier_base_stats) // 2):
        attribute = choice(secret_mutiplier_base_stats)
        attr_probs[attribute] = 1
    for _ in range(len(secret_combat_stats)):
        attribute = choice(secret_combat_stats)
        attr_probs[attribute] = 50

    count_multiplier = 0
    for _ in range(bonus):
        attribute = weighted_choice(**attr_probs)

        if count_multiplier > 3:
            print('Foi atingido o limite de multiplicadores.')
            break
        elif attribute in secret_mutiplier_base_stats:
            secret_stats[attribute] += choice([.1, .25, .5, .75, 1.0])
            count_multiplier += 1
        elif attribute in secret_combat_stats:
            secret_stats[attribute] += randint(1, 10)
            attr_probs[attribute] += 15
        else:
            secret_stats[attribute] += 1
            attr_probs[attribute] += 10

    if 'secret_bonus_hit_points' in secret_stats:
        secret_stats['secret_bonus_hit_points'] *= randint(2, 5)

    if len(secret_stats) > 0:
        secret_stats['identified'] = False

    return secret_stats


def create_random_equipment(equip_type: str, group_level: int) -> Equipment:
    rarity = choice_rarity(group_level)
    weapon, material = get_weapon_material(equip_type, group_level)

    equip_name = weapon if weapon else equip_type
    bonus, penality = get_bonus_penality(
        equip_type, rarity, material, group_level, True
    )
    attr_bonus_prob, attr_panality_prob = get_attribute_probabilities(
        equip_name
    )
    equipment_dict = defaultdict(int)
    for _ in range(bonus):
        attribute = weighted_choice(**attr_bonus_prob)
        equipment_dict[attribute] += 1

    for _ in range(penality):
        attribute = weighted_choice(**attr_panality_prob)
        equipment_dict[attribute] -= 1

    equip_name = equip_name.replace('_', ' ')
    name = f'{rarity.title()} {material.title()} {equip_name.title()}'
    weight = get_equipment_weight(equip_type, rarity, material, weapon)
    damage_types = get_equipment_damage_type(weapon, rarity)
    secret_stats = add_secret_stats(equipment_dict, rarity, group_level)
    equipment_dict.update(secret_stats)
    equipment = Equipment(
        name=name,
        equip_type=equip_type,
        damage_types=damage_types,
        weight=weight,
        requirements={'level': group_level},
        rarity=rarity,
        _id=ObjectId(),
        **equipment_dict
    )
    item = Item(equipment)

    return item


def create_random_item(group_level: int) -> Union[Consumable, Equipment]:
    '''Função que retorna um item escolhido de forma aleatória.'''
    group_level = random_group_level(group_level)
    choiced_item = choice_type_item()
    equipment_types = [e.name for e in EquipmentEnum]
    if choiced_item == 'CONSUMABLE':
        item = create_random_consumable(group_level)
    elif choiced_item in equipment_types:
        item = create_random_equipment(choiced_item, group_level)

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
    # test_count(choice_type_item)
    # test_count(choice_rarity)
    # test_count(choice_weapon_material)
    # test_count(choice_armor_material)
    # test_count(choice_accessory_material)

    # print(create_random_item(100))

    for _ in range(1000):
        create_random_item(1001)
