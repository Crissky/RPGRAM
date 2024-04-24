from bson import ObjectId
from collections import defaultdict
from random import choice, random, randint
from typing import Dict, Iterable, List, Tuple, Union
from repository.mongo import ItemModel
from repository.mongo.populate.tools import random_group_level, weighted_choice
from repository.mongo.populate.item_constants import (
    ALL_EQUIPMENTS_DEFINITIONS,
    ALL_WEAPONS,
    ARMOR_EQUIPMENTS,
    BLUDGEONING_WEAPONS,
    BOOTS_EQUIPMENTS,
    COIN_EQUIPMENTS,
    ENCHANTED_WEAPONS,
    KAJIYA_EQUIPMENTS,
    MAGICAL_GRIMOIRE_EQUIPMENTS,
    HEAVY_EQUIPMENTS,
    HELMET_EQUIPMENTS,
    LIGHT_EQUIPMENTS,
    MAGIC_WEAPONS,
    AMULET_EQUIPMENTS,
    MAGICAL_STONES_EQUIPMENTS,
    MAGICAL_WEARABLE_EQUIPMENTS,
    MAGICAL_MASK_EQUIPMENTS,
    ONE_HAND_EQUIPMENTS,
    PIERCING_WEAPONS,
    MAGICAL_QUILL_EQUIPMENTS,
    RING_EQUIPMENTS,
    SEISHIN_WEARBLE_EQUIPMENTS,
    SLASHING_WEAPONS,
    TATICAL_WEARABLE_EQUIPMENTS,
    TWO_HANDS_EQUIPMENTS,
    VERY_HEAVY_EQUIPMENTS,
    STR_REQUIREMENTS,
    DEX_REQUIREMENTS,
    CON_REQUIREMENTS,
    INT_REQUIREMENTS,
    WIS_REQUIREMENTS,
    CHA_REQUIREMENTS,
    ALL_MAGICAL_EQUIPMENTS,
    ALL_TATICAL_EQUIPMENTS,
)

from rpgram.boosters import Equipment
from rpgram.consumables import Consumable
from rpgram import Item
from rpgram.enums import (
    AccessoryMaterialsEnum,
    CoinMaterialsEnum,
    DamageEnum,
    EquipmentEnum,
    MagicalGrimoireMaterialEnum,
    MagicalStonesMaterialEnum,
    MagicalWearableMaterialEnum,
    MagicalMaskMaterialEnum,
    MagicalQuillMaterialEnum,
    RarityEnum,
    WeaponMaterialEnum,
    WearableMaterialEnum,
    TacticalWearableMaterialEnum
)
from rpgram.enums.material import KajiyaMaterialEnum, SeishinWearbleMaterialEnum


# CONSTANTS
MIN_CONSUMABLE_QUANTITY = 1
MAX_CONSUMABLE_QUANTITY = 5
EQUIPS_NO_REDUCE_SECRET_STATS = [
    EquipmentEnum.TWO_HANDS.name,
    EquipmentEnum.ARMOR.name
]


WEAPON_EQUIPMENTS_ENUM = [
    EquipmentEnum.ONE_HAND.name, EquipmentEnum.TWO_HANDS.name
]
WEARABLE_EQUIPMENTS_ENUM = [
    EquipmentEnum.HELMET.name,
    EquipmentEnum.ARMOR.name,
    EquipmentEnum.BOOTS.name
]
ACCESSORY_EQUIPMENTS_ENUM = [
    EquipmentEnum.RING.name, EquipmentEnum.AMULET.name
]
BONUS_RARITY = {
    rarity.name: multiplier+1
    for multiplier, rarity in enumerate(RarityEnum)
}
WEAPON_MATERIALS = {
    material.name: multiplier+1
    for multiplier, material in enumerate(WeaponMaterialEnum)
}
WEARABLE_MATERIALS = {
    material.name: multiplier+1
    for multiplier, material in enumerate(WearableMaterialEnum)
}
ACCESSORY_MATERIALS = {
    material.name: multiplier+1
    for multiplier, material in enumerate(AccessoryMaterialsEnum)
}


# FUNCTIONS
def choice_type_item(no_trap: bool = False) -> str:
    '''Função que retorna um tipo de item aleatório.
    O tipo do item é retornado com base em sua propabilidade.
    '''
    types_item = {
        'CONSUMABLE': 800, 'TRAP': 150,
        EquipmentEnum.HELMET.name: 100,
        EquipmentEnum.ONE_HAND.name: 150, EquipmentEnum.TWO_HANDS.name: 150,
        EquipmentEnum.ARMOR.name: 100, EquipmentEnum.BOOTS.name: 100,
        EquipmentEnum.RING.name: 50, EquipmentEnum.AMULET.name: 50,
    }

    if no_trap:
        types_item.pop('TRAP')

    return weighted_choice(**types_item)


def choice_equip_type() -> str:
    '''Função que retorna um tipo de equipamento aleatório.
    O tipo do equipamento é retornado com base em sua propabilidade.
    '''

    types_item = {
        EquipmentEnum.HELMET.name: 100,
        EquipmentEnum.ONE_HAND.name: 100, EquipmentEnum.TWO_HANDS.name: 100,
        EquipmentEnum.ARMOR.name: 100, EquipmentEnum.BOOTS.name: 100,
        EquipmentEnum.RING.name: 100, EquipmentEnum.AMULET.name: 100,
    }

    return weighted_choice(**types_item)


def choice_total_items(min_items: int = 1, max_items: int = 5) -> int:
    '''Função que retorna um valor inteiro aleatério entre 
    min_times e max_times de maneira poderada, em que os valores mais próximos 
    de min_times tem maior chance de ocorrer.
    Não funciona para um número grande de elementos. 
    Acima de 19 elementos, haverão elementos que terão probabildiade zero de 
    ser escolhido.

    '''
    if min_items == max_items:
        return min_items
    elif min_items > max_items:
        raise ValueError('"min_times" deve ser menor ou igual a "max_times".')

    total_numbers = max_items - min_items + 1
    base_prob = total_numbers * 100 * 2
    numbers_probs = {
        str(n): int(base_prob := base_prob // 1.5)
        for n in range(min_items, max_items+1)
    }

    return int(weighted_choice(**numbers_probs))


def choice_rarity(group_level: int) -> str:
    '''Retorna uma raridade de maneira aleatória.
    A raridade é retornada com base em sua propabilidade e no nível do grupo.
    Um nível de grupo maior libera mais tipos de raridades.
    As raridades opcionais (que estão nos IFs) aumentam a sua probabilidade de 
    acordo com o nível do grupo com um valor máximo de 50, recebendo um bônus 
    entre 1/100 à 1/5 do nível de grupo.
    '''
    rare_probs = 25 + (group_level // randint(20, 100))
    epic_probs = 12.5 + (group_level // randint(20, 100))
    legendary_probs = 6.25 + (group_level // randint(20, 100))
    mythic_probs = 3.125 + (group_level // randint(20, 100))
    rarities = {RarityEnum.COMMON.name: 100, RarityEnum.UNCOMMON.name: 50}
    if group_level >= 50:
        rarities[RarityEnum.RARE.name] = min(rare_probs, 50)
    if group_level >= 500:
        rarities[RarityEnum.EPIC.name] = min(epic_probs, 50)
    if group_level >= 1250:
        rarities[RarityEnum.LEGENDARY.name] = min(legendary_probs, 50)
    if group_level >= 2000:
        rarities[RarityEnum.MYTHIC.name] = min(mythic_probs, 50)

    return weighted_choice(**rarities)


def choice_material(
    group_level: int,
    equipment_materials: dict,
    level_base: int = 25,
    chance_reducer: int = 25,
    total_materials: int = 3,
) -> str:
    '''Retorna um material de um equipamento de maneira aleatória.
    Quanto maior o nível de grupo, maior a diversidade de materiais.
    Um novo material entrará na lista de escolha (materials) 
    a cada "level_base" pontos de nível de grupo.

    Args:
        "group_level": Nível do Grupo
        "equipment_materials": Dicionário contendo os materiais dos equipamentos 
            como chave e o multiplicador como valor.
        "level_base": Nível base para a ocorrência de novos materiais além do 
            primeiro.
        "chance_reducer": Redutor de propabilidade dos materiais mais raros.
        "total_materials": Número máximo de materiais mais raros que ficarão 
            na lista para serem escolhidos.

    level_base: 25      level_base: 50
    M:1, LV: 0          M:1, LV:0
    M:2, LV: 25         M:2, LV:50
    M:3, LV: 100        M:3, LV:200
    M:4, LV: 225        M:4, LV:450
    M:5, LV: 400        M:5, LV:800
    M:6, LV: 625        M:6, LV:1250
    M:7, LV: 900        M:7, LV:1800
    M:8, LV: 1225       M:8, LV:2450
    M:9, LV: 1600       M:9, LV:3200
    '''

    materials = {}
    chance = 100 + (len(equipment_materials) * chance_reducer)
    for material, multiplier in equipment_materials.items():
        level_threshold = level_base * ((multiplier - 1) ** 2)
        if group_level >= level_threshold or not materials:
            materials[material] = chance
            chance -= chance_reducer

    if len(materials) > total_materials:
        materials = dict([materials.popitem() for _ in range(total_materials)])

    return weighted_choice(**materials)


def choice_weapon_material(group_level: int) -> str:
    '''Retorna um material de arma de maneira aleatória.
    Quanto maior o nível de grupo, maior a diversidade de materiais.
    Um novo material entrará na lista de escolha (materials) 
    a cada 25 pontos de nível de grupo.
    '''

    return choice_material(
        group_level=group_level,
        equipment_materials=WEAPON_MATERIALS,
        level_base=25,
        chance_reducer=25
    )


def choice_armor_material(group_level: int) -> str:
    '''Retorna um material de armadura de maneira aleatória.
    Quanto maior o nível de grupo, maior a diversidade de materiais.
    Um novo material entrará na lista de escolha (materials) 
    a cada 25 pontos de nível de grupo.
    '''

    return choice_material(
        group_level=group_level,
        equipment_materials=WEARABLE_MATERIALS,
        level_base=25,
        chance_reducer=25
    )


def choice_accessory_material(group_level: int) -> str:
    '''Retorna um material de acessórios de maneira aleatória.
    Quanto maior o nível de grupo, maior a diversidade de materiais.
    Um novo material entrará na lista de escolha (materials) 
    a cada 50 pontos de nível de grupo.
    '''

    return choice_material(
        group_level=group_level,
        equipment_materials=ACCESSORY_MATERIALS,
        level_base=50,
        chance_reducer=25
    )


def get_equip_class_and_material(
    equip_type: str,
    group_level: int
) -> Tuple[str, str]:
    '''Retorna uma tupla com a classe do equipamento na primeira posição e o 
    material do equipamento na segunda posição.
    '''

    equip_class = None

    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        material = choice_weapon_material(group_level)
        if equip_type == EquipmentEnum.ONE_HAND.name:
            equip_class = choice(list(ONE_HAND_EQUIPMENTS))
        elif equip_type == EquipmentEnum.TWO_HANDS.name:
            equip_class = choice(list(TWO_HANDS_EQUIPMENTS))
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        material = choice_armor_material(group_level)
        if equip_type == EquipmentEnum.HELMET.name:
            equip_class = choice(list(HELMET_EQUIPMENTS))
        elif equip_type == EquipmentEnum.ARMOR.name:
            equip_class = choice(list(ARMOR_EQUIPMENTS))
        elif equip_type == EquipmentEnum.BOOTS.name:
            equip_class = choice(list(BOOTS_EQUIPMENTS))
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        material = choice_accessory_material(group_level)
        if equip_type == EquipmentEnum.RING.name:
            equip_class = choice(list(RING_EQUIPMENTS))
        elif equip_type == EquipmentEnum.AMULET.name:
            equip_class = choice(list(AMULET_EQUIPMENTS))
    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )

    return equip_class, material


def get_material_level(equip_type: str, material: str) -> int:
    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        material_bonus = WEAPON_MATERIALS[material]
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        material_bonus = WEARABLE_MATERIALS[material]
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        material_bonus = ACCESSORY_MATERIALS[material]
    else:
        raise ValueError(
            f'Não foi possível definir o Nível do Material, pois o '
            f'tipo de equipamento "{equip_type}" não foi encontrado.'
        )

    return material_bonus


def check_equipment_type(equip_type: str, equip_class: str):
    error_message = (
        f'Classe de Equipamento "{equip_class}" não encontrada para '
        f'o tipo de equipamento "{equip_type}".'
    )

    if equip_type == EquipmentEnum.ONE_HAND.name:
        if equip_class not in ONE_HAND_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.TWO_HANDS.name:
        if equip_class not in TWO_HANDS_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.HELMET.name:
        if equip_class not in HELMET_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.ARMOR.name:
        if equip_class not in ARMOR_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.BOOTS.name:
        if equip_class not in BOOTS_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.RING.name:
        if equip_class not in RING_EQUIPMENTS:
            raise ValueError(error_message)
    elif equip_type == EquipmentEnum.AMULET.name:
        if equip_class not in AMULET_EQUIPMENTS:
            raise ValueError(error_message)
    else:
        raise ValueError(
            f'Tipo de Equipamento "{equip_type}" não encontrado.'
        )


def get_bonus_and_penality(
    equip_type: str,
    rarity: str,
    material: str,
    group_level: int,
    verbose: bool = False
) -> Tuple[int, int]:
    '''Retorna um tupla com os valores totais de BÔNUS e PENALIDADE 
    do equipamento. Os bônus são escolhidos com base do tipo de equipamento, 
    raridade, material level e nível de grupo. A penalidade é escolhida 
    somente com base no nível de grupo.
    '''
    rarity_bonus = BONUS_RARITY[rarity]
    if equip_type in [EquipmentEnum.TWO_HANDS.name]:
        equip_type_bonus = 3.75
    elif equip_type in [EquipmentEnum.ONE_HAND.name]:
        equip_type_bonus = 1.50
    elif equip_type in [EquipmentEnum.ARMOR.name]:
        equip_type_bonus = 2.50
    elif equip_type in [EquipmentEnum.HELMET.name, EquipmentEnum.BOOTS.name]:
        equip_type_bonus = 0.50
    elif equip_type in [EquipmentEnum.RING.name, EquipmentEnum.AMULET.name]:
        equip_type_bonus = 0.25

    two_hand_multiplier = (
        2
        if equip_type == EquipmentEnum.TWO_HANDS.name
        else 1
    )

    material_bonus = get_material_level(equip_type, material)

    bonus_multiplier = (equip_type_bonus + rarity_bonus + material_bonus)
    penality_multiplier = bonus_multiplier // 3
    bonus = int(
        group_level * bonus_multiplier * two_hand_multiplier
    )
    penality = int(random_group_level(group_level) * penality_multiplier)
    if verbose:
        print(
            f'Level: {group_level}, '
            f'Equipamento: {equip_type}({equip_type_bonus}), '
            f'Raridade: {rarity}({rarity_bonus}), '
            f'Material: {material}({material_bonus}), '
            f'Bônus: {bonus}, Penalidade: {penality}'
        )

    return bonus, penality


def get_attribute_probabilities(equip_class: str) -> Dict[str, int]:
    '''Retorna uma tupla contendo dois dicionários com as probabilidades 
    de distribuição dos bônus e penalidades dos atributos de um equipamento, 
    respectivamente.
    '''
    equipment = ALL_EQUIPMENTS_DEFINITIONS.get(equip_class, None)
    if equipment is None:
        raise ValueError(
            f'"{equip_class}" não é um tipo de equipamento válido.')

    attr_bonus_prob = equipment['attr_bonus_prob']
    attr_penality_prob = equipment['attr_penality_prob']

    return attr_bonus_prob, attr_penality_prob


def get_equipment_weight(
    equip_type: str,
    rarity: str,
    material: str,
    equip_class: str
) -> float:
    '''Retorna o peso do equipamento com base no seu bônus e 
    no tipo de equipamento.
    '''

    weight, _ = get_bonus_and_penality(equip_type, rarity, material, 5)
    if equip_class in HEAVY_EQUIPMENTS:
        weight *= 2
    elif equip_class in VERY_HEAVY_EQUIPMENTS:
        weight *= 3
    elif equip_class in LIGHT_EQUIPMENTS:
        weight /= 10

    return weight


def get_equipment_damage_type(
    equip_class: str,
    rarity: str
) -> List[DamageEnum]:
    '''Retorna uma lista com os tipos de dano de uma arma.
    '''

    damage_types = None
    if equip_class in ALL_WEAPONS:
        damage_types = []
        chance = .5
        turns = BONUS_RARITY[rarity] - 1
        damages_list = [
            e for e in DamageEnum
            if e not in [DamageEnum.SLASHING, DamageEnum.BLUDGEONING,
                         DamageEnum.HITTING, DamageEnum.PIERCING]
        ]
        if equip_class in SLASHING_WEAPONS:
            damage_types = [DamageEnum.SLASHING]
        elif equip_class in BLUDGEONING_WEAPONS:
            damage_types = [DamageEnum.BLUDGEONING]
        elif equip_class in PIERCING_WEAPONS:
            damage_types = [DamageEnum.PIERCING]
        elif equip_class in MAGIC_WEAPONS:
            damage_types = [DamageEnum.MAGIC]
            damages_list.remove(DamageEnum.MAGIC)

        if equip_class in ENCHANTED_WEAPONS:
            turns += 1
            chance = .9

        for _ in range(turns):
            if random() <= chance:
                new_damage = choice(damages_list)
                damages_list.remove(new_damage)
                damage_types.append(new_damage)
                chance /= 2

    return damage_types


def get_equipment_damage_type_name(damage_types: List[DamageEnum]) -> str:
    '''Retorna os nomes dos tipos de dano de uma arma. para ser usado
    como parte do nome do equipamento.
    '''
    text = ''
    if isinstance(damage_types, list):
        damage_list = sorted([
            e.name.title()
            for e in damage_types
            if e not in [DamageEnum.SLASHING, DamageEnum.BLUDGEONING,
                         DamageEnum.HITTING, DamageEnum.PIERCING]
        ])
        if damage_list:
            priority_damage_enums = [
                DamageEnum.MAGIC, DamageEnum.BLESSING, DamageEnum.DIVINE
            ]
            for damage_enum in priority_damage_enums:
                damage_enum = damage_enum.name.title()
                if damage_enum in damage_list:
                    damage_list.remove(damage_enum)
                    damage_list.insert(0, damage_enum)
            text = f' of {" and ".join(damage_list)}'

    return text


def get_requirements(
    group_level: int,
    equip_class: str,
    equip_type: str,
    material: str,
    rarity: str,
) -> Dict[str, int]:
    '''Retorna um dicionário com os requisitos necessários para 
    equiapar o equipamento.
    '''

    requirements = defaultdict(int)
    requirements['level'] = group_level
    material_bonus = get_material_level(equip_type, material)
    rarity_bonus = BONUS_RARITY[rarity]
    percent_bonus = 1 + ((material_bonus + rarity_bonus) / 10)

    if equip_type in [EquipmentEnum.ARMOR.name]:
        equip_group_lvl = group_level // 2
    elif equip_type in [EquipmentEnum.TWO_HANDS.name]:
        equip_group_lvl = group_level // 2.5
    elif equip_type in [EquipmentEnum.ONE_HAND.name]:
        equip_group_lvl = group_level // 3
    elif equip_type in [EquipmentEnum.HELMET.name, EquipmentEnum.BOOTS.name]:
        equip_group_lvl = group_level // 3
    elif equip_type in [EquipmentEnum.RING.name, EquipmentEnum.AMULET.name]:
        equip_group_lvl = group_level // 4

    if equip_class in STR_REQUIREMENTS:
        requirements['FOR'] += random_group_level(equip_group_lvl)
    if equip_class in DEX_REQUIREMENTS:
        requirements['DES'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl) / 2
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in CON_REQUIREMENTS:
        requirements['CON'] += random_group_level(equip_group_lvl)

        # requirements['FOR'] -= random_group_level(equip_group_lvl) / 2
        requirements['DES'] -= random_group_level(equip_group_lvl) / 2
        requirements['INT'] -= random_group_level(equip_group_lvl) / 2
        requirements['SAB'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in INT_REQUIREMENTS:
        requirements['INT'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl)
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in WIS_REQUIREMENTS:
        requirements['SAB'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl)
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in CHA_REQUIREMENTS:
        requirements['CAR'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl)
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2

    if equip_class in ALL_MAGICAL_EQUIPMENTS:
        requirements['INT'] += random_group_level(equip_group_lvl)
        requirements['SAB'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl)
        requirements['CON'] -= random_group_level(equip_group_lvl)
    if equip_class in ALL_TATICAL_EQUIPMENTS:
        requirements['DES'] += random_group_level(equip_group_lvl)

        requirements['FOR'] -= random_group_level(equip_group_lvl) / 2
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2

    if equip_class in LIGHT_EQUIPMENTS:
        requirements['FOR'] -= random_group_level(equip_group_lvl) / 2
        requirements['CON'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in HEAVY_EQUIPMENTS:
        requirements['FOR'] += random_group_level(equip_group_lvl)

        requirements['INT'] -= random_group_level(equip_group_lvl) / 2
        requirements['SAB'] -= random_group_level(equip_group_lvl) / 2
    if equip_class in VERY_HEAVY_EQUIPMENTS:
        requirements['CON'] += random_group_level(equip_group_lvl)

        requirements['INT'] -= random_group_level(equip_group_lvl) / 2
        requirements['SAB'] -= random_group_level(equip_group_lvl) / 2

    for attribute in requirements.keys():
        if attribute == 'level':
            continue
        requirements[attribute] = int(requirements[attribute] * percent_bonus)

    requirements
    requirements = {
        attribute: value
        for attribute, value in requirements.items()
        if value > 0
    }

    return requirements


def add_secret_stats(
    rarity: str,
    group_level: int,
    equip_type: str
) -> Dict[str, int]:
    '''Retorna os atributos bônus do equipamento. 
    Esses atributos estarão disponíveis para o personagem quando 
    o item for identificado.
    Os bônus são selecionado de maneira aleatórios. O total de bônus é baseado 
    na raridade do item em na metade do nível de grupo.
    '''

    secret_stats = defaultdict(int)
    bonus = BONUS_RARITY[rarity] - 2
    level_divisor = 0.80 if equip_type in EQUIPS_NO_REDUCE_SECRET_STATS else 2
    bonus = max(bonus, 0) * (group_level // level_divisor)
    bonus = int(bonus)
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
        secret_stats['secret_bonus_hit_points'] *= randint(5, 10)

    if len(secret_stats) > 0:
        secret_stats['identified'] = False

    return secret_stats


def translate_material_name(
    equip_type: str,
    equip_class: str,
    material: str,
) -> str:
    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        index = WEAPON_MATERIALS[material] - 1
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        index = WEARABLE_MATERIALS[material] - 1
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        index = ACCESSORY_MATERIALS[material] - 1

    if equip_class in MAGICAL_QUILL_EQUIPMENTS:
        material_name = list(MagicalQuillMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif equip_class in MAGICAL_GRIMOIRE_EQUIPMENTS:
        material_name = list(MagicalGrimoireMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    elif equip_class in MAGICAL_STONES_EQUIPMENTS:
        material_name = list(MagicalStonesMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif equip_class in MAGICAL_WEARABLE_EQUIPMENTS:
        material_name = list(MagicalWearableMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    elif equip_class in MAGICAL_MASK_EQUIPMENTS:
        material_name = list(MagicalMaskMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif equip_class in TATICAL_WEARABLE_EQUIPMENTS:
        material_name = list(TacticalWearableMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif equip_class in COIN_EQUIPMENTS:
        material_name = list(CoinMaterialsEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif equip_class in SEISHIN_WEARBLE_EQUIPMENTS:
        material_name = list(SeishinWearbleMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    elif equip_class in KAJIYA_EQUIPMENTS:
        material_name = list(KajiyaMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    else:
        material_name = material.replace("_", " ").title()

    return material_name


def create_random_equipment(
    equip_type: str,
    group_level: int,
    rarity: Union[RarityEnum, str] = None,
    equip_class: str = None,
    material: str = None,
    random_level: bool = False,
    save_in_database: bool = False,
) -> Item:
    '''Retorna um equipamento aleatório.
    '''

    if equip_type is None:
        equip_type = choice_equip_type()

    if isinstance(rarity, RarityEnum):
        rarity = rarity.name
    elif rarity not in RarityEnum.__members__:
        rarity = choice_rarity(group_level)

    if random_level:
        group_level = random_group_level(group_level)

    _equip_class, _material = get_equip_class_and_material(
        equip_type,
        group_level
    )
    equip_class = equip_class if equip_class else _equip_class
    material = material if material else _material
    material_level = get_material_level(
        equip_type=equip_type,
        material=material
    )

    check_equipment_type(equip_type, equip_class)

    equip_name = equip_class if equip_class else equip_type
    print(f'Equipamento: {equip_class}', end=' ')
    bonus, penality = get_bonus_and_penality(
        equip_type, rarity, material, group_level, True
    )
    attr_bonus_prob, attr_penality_prob = get_attribute_probabilities(
        equip_name
    )
    requirements = get_requirements(
        group_level=group_level,
        equip_class=equip_class,
        equip_type=equip_type,
        material=material,
        rarity=rarity,
    )
    equipment_dict = defaultdict(int)
    for _ in range(bonus):
        attribute = weighted_choice(**attr_bonus_prob)
        equipment_dict[attribute] += 1

    for _ in range(penality):
        attribute = weighted_choice(**attr_penality_prob)
        equipment_dict[attribute] -= 1

    if 'bonus_hit_points' in equipment_dict:
        if equipment_dict['bonus_hit_points'] > 0:
            equipment_dict['bonus_hit_points'] *= randint(2, 5)

    weight = get_equipment_weight(equip_type, rarity, material, equip_class)
    material_name = translate_material_name(equip_type, equip_class, material)
    damage_types = get_equipment_damage_type(equip_class, rarity)
    damage_type_name = get_equipment_damage_type_name(damage_types)
    name = (
        f'{rarity} '
        f'{material_name} '
        f'{equip_name}'
        f'{damage_type_name}'
    ).replace("_", " ").title().replace("'S", "'s")
    secret_stats = add_secret_stats(rarity, group_level, equip_type)
    equipment_dict.update(secret_stats)
    equipment = Equipment(
        name=name,
        equip_type=equip_type,
        damage_types=damage_types,
        weight=weight,
        requirements=requirements,
        rarity=rarity,
        material_level=material_level,
        _id=ObjectId(),
        **equipment_dict
    )
    item = Item(equipment)

    if save_in_database is True:
        item_model = ItemModel()
        item_model.save(equipment)

    return item


def create_random_consumable(
    group_level: int,
    ignore_list: List[Consumable] = [],
    min_consumable_quantity: int = MIN_CONSUMABLE_QUANTITY,
    max_consumable_quantity: int = MAX_CONSUMABLE_QUANTITY,
    random_level: bool = False,
    total_items: int = None,
) -> Union[Item, Iterable[Item]]:
    '''Retorna um itens consumíveis aleatórios.
    '''

    if total_items is None:
        return choice_consumable(
            group_level=group_level,
            ignore_list=ignore_list,
            min_consumable_quantity=min_consumable_quantity,
            max_consumable_quantity=max_consumable_quantity,
            random_level=random_level,
        )
    else:
        items_dict = {}
        return (
            choice_consumable(
                group_level=group_level,
                ignore_list=ignore_list,
                min_consumable_quantity=min_consumable_quantity,
                max_consumable_quantity=max_consumable_quantity,
                random_level=random_level,
                items_dict=items_dict,
            )
            for _ in range(total_items)
        )


def choice_consumable(
    group_level: int,
    ignore_list: List[Consumable] = [],
    min_consumable_quantity: int = MIN_CONSUMABLE_QUANTITY,
    max_consumable_quantity: int = MAX_CONSUMABLE_QUANTITY,
    random_level: bool = False,
    items_dict: dict = {},
) -> Item:
    '''Retorna um item consumível para a função create_random_consumable()
    Arg: items_dict é usando para evitar de baixar novamente a lista de itens 
    obtidas de uma chamada de anterior. Isso deixa a função muito mais rápida 
    para loop longos.
    '''

    if random_level:
        group_level = random_group_level(group_level)

    rarity = choice_rarity(group_level)
    if rarity not in items_dict:
        item_model = ItemModel()
        ignore_list = [
            i.__name__
            for i in ignore_list
            if issubclass(i, Consumable)
        ]
        query = dict(
            rarity=rarity,
            _class={'$nin': [Equipment.__name__, *ignore_list]}
        )
        items_dict[rarity] = item_model.get_all(query=query)

    item_list = items_dict[rarity]
    quantity = randint(min_consumable_quantity, max_consumable_quantity)
    item = choice(item_list)
    item = Item(item, quantity)

    return item


def create_random_trap(group_level: int) -> int:
    trap_level = group_level
    trap_degree = randint(10, 20)

    return trap_level * trap_degree


def create_random_item(
    group_level: int,
    min_items: int = 1,
    max_items: int = 5,
    no_trap: bool = False,
    save_in_database: bool = True,
) -> Union[int, Iterable[Union[Consumable, Equipment]]]:
    '''Função que retorna um item escolhido de maneira aleatória.
    '''

    def random_item_generator(group_level: int) -> Item:
        equipment_types = [e.name for e in EquipmentEnum]
        choiced_item = choice_type_item(no_trap=True)
        if choiced_item == 'CONSUMABLE':
            item = create_random_consumable(group_level, random_level=True)
        elif choiced_item in equipment_types:
            item = create_random_equipment(
                choiced_item,
                group_level,
                random_level=True,
                save_in_database=save_in_database,
            )
        else:
            raise ValueError(
                f'O item "{choiced_item}" não foi encontrado.'
            )
        return item

    choiced_item_or_trap = choice_type_item(no_trap=no_trap)
    if choiced_item_or_trap == 'TRAP':
        trap_level = create_random_trap(group_level)
        return trap_level
    else:
        total_items = choice_total_items(min_items, max_items)
        return (random_item_generator(group_level) for _ in range(total_items))


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

    random_items = create_random_item(
        group_level=1001,
        min_items=1000,
        max_items=1000,
        no_trap=True,
        save_in_database=False,
    )
    print(f'random_items type(): {type(random_items)}')
    print(isinstance(random_items, Iterable))
    for item in random_items:
        pass

    # print(
    #     create_random_equipment(
    #         EquipmentEnum.ONE_HAND.name,
    #         100,
    #         # RarityEnum.RARE,
    #         weapon='SWORD',
    #         material=WeaponMaterialEnum.STEEL.name
    #     ).get_all_sheets(verbose=True)
    # )

    # for _ in range(1000):
    #     items = create_random_item(1001)
    #     if isinstance(items, list):
    #         for item in items:
    #             if isinstance(item.item, Equipment):
    #                 print(f'\t{item.item.name}')
