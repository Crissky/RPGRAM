from bson import ObjectId
from collections import defaultdict
from random import choice, random, randint
from typing import Dict, List, Tuple, Union
from repository.mongo import ItemModel
from repository.mongo.populate.tools import weighted_choice
from repository.mongo.populate.item_constants import (
    ALL_EQUIPMENTS_DEFINITIONS,
    ALL_WEAPONS,
    ARMOR_EQUIPMENTS,
    BLUDGEONING_WEAPONS,
    BOOTS_EQUIPMENTS,
    ENCHANTED_WEAPONS,
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
    SLASHING_WEAPONS,
    TATICAL_WEARABLE_EQUIPMENTS,
    TWO_HANDS_EQUIPMENTS,
    VERY_HEAVY_EQUIPMENTS
)

from rpgram.boosters import Equipment
from rpgram.consumables import Consumable
from rpgram import Item
from rpgram.enums import (
    AccessoryMaterialsEnum,
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


# CONSTANTS
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
    RarityEnum.COMMON.name: 1, RarityEnum.UNCOMMON.name: 2,
    RarityEnum.RARE.name: 3, RarityEnum.EPIC.name: 4,
    RarityEnum.LEGENDARY.name: 5, RarityEnum.MYTHIC.name: 6,
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
def random_group_level(level: int) -> int:
    '''Função que retorna um valor inteiro aleatório entre 75% e 125% do 
    level passado. No entando, o menor valor retornado sempre será 1.
    '''
    min_level = max(int(level - 10), 1)
    max_level = int(level + 10)
    new_level = choice(range(min_level, max_level))
    return new_level


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


def choice_total_times(min_times: int = 1, max_times: int = 5) -> int:
    '''Função que retorna um valor inteiro aleatério entre 
    min_times e max_times de maneira poderada, em que os valores mais próximos 
    de min_times tem maior chance de ocorrer.
    Não funciona para um número grande de elementos. 
    Acima de 19 elementos, haverão elementos que terão probabildiade zero de 
    ser escolhido.

    '''
    if min_times == max_times:
        return min_times
    elif min_times > max_times:
        raise ValueError('"min_times" deve ser menor ou igual a "max_times".')

    total_numbers = max_times - min_times + 1
    base_prob = total_numbers * 100 * 2
    numbers_probs = {
        str(n): int(base_prob := base_prob // 1.5)
        for n in range(min_times, max_times+1)
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
    if group_level >= 100:
        rarities[RarityEnum.EPIC.name] = min(epic_probs, 50)
    if group_level >= 250:
        rarities[RarityEnum.LEGENDARY.name] = min(legendary_probs, 50)
    if group_level >= 500:
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
    '''

    materials = {}
    chance = 100 + (len(equipment_materials) * chance_reducer)
    for material, multiplier in equipment_materials.items():
        level_threshold = level_base * (multiplier - 1)
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


def get_equipment_and_material(
    equip_type: str,
    group_level: int
) -> Tuple[str, str]:
    '''Retorna uma tupla com o nome da arma na primeira posição, 
    caso o tipo do equipamento seja de UMA ou de DUAS MÃOS
    ou None caso contrário. 
    Na segunda posição será retornado o material do equipamento
    '''
    weapon = None

    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        material = choice_weapon_material(group_level)
        if equip_type == EquipmentEnum.ONE_HAND.name:
            weapon = choice(list(ONE_HAND_EQUIPMENTS))
        elif equip_type == EquipmentEnum.TWO_HANDS.name:
            weapon = choice(list(TWO_HANDS_EQUIPMENTS))
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        material = choice_armor_material(group_level)
        if equip_type == EquipmentEnum.HELMET.name:
            weapon = choice(list(HELMET_EQUIPMENTS))
        elif equip_type == EquipmentEnum.ARMOR.name:
            weapon = choice(list(ARMOR_EQUIPMENTS))
        elif equip_type == EquipmentEnum.BOOTS.name:
            weapon = choice(list(BOOTS_EQUIPMENTS))
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        material = choice_accessory_material(group_level)
        if equip_type == EquipmentEnum.RING.name:
            weapon = choice(list(RING_EQUIPMENTS))
        elif equip_type == EquipmentEnum.AMULET.name:
            weapon = choice(list(AMULET_EQUIPMENTS))

    else:
        raise ValueError(
            f'Material do equipamento "{equip_type}" não encontrado.'
        )

    return weapon, material


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
    if equip_type in [EquipmentEnum.TWO_HANDS.name, EquipmentEnum.ARMOR.name]:
        equip_type_bonus = 2.5
    elif equip_type in [EquipmentEnum.ONE_HAND.name]:
        equip_type_bonus = 1
    elif equip_type in [EquipmentEnum.HELMET.name, EquipmentEnum.BOOTS.name]:
        equip_type_bonus = 0.5
    elif equip_type in [EquipmentEnum.RING.name, EquipmentEnum.AMULET.name]:
        equip_type_bonus = 0.25

    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        material_bonus = WEAPON_MATERIALS[material]
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        material_bonus = WEARABLE_MATERIALS[material]
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        material_bonus = ACCESSORY_MATERIALS[material]

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


def get_attribute_probabilities(weapon: str) -> Dict[str, int]:
    '''Retorna uma tupla contendo dois dicionários com as probabilidades 
    de distribuição dos bônus e penalidades dos atributos de um equipamento, 
    respectivamente.
    '''
    equipment = ALL_EQUIPMENTS_DEFINITIONS.get(weapon, None)
    if equipment is None:
        raise ValueError(f'"{weapon}" não é um tipo de equipamento válido.')

    attr_bonus_prob = equipment['attr_bonus_prob']
    attr_penality_prob = equipment['attr_penality_prob']

    return attr_bonus_prob, attr_penality_prob


def get_equipment_weight(equip_type, rarity, material, weapon) -> float:
    '''Retorna o peso do equipamento com base no seu bônus e 
    no tipo de equipamento.
    '''
    weight, _ = get_bonus_and_penality(equip_type, rarity, material, 5)
    if weapon in HEAVY_EQUIPMENTS:
        weight *= 2
    elif weapon in VERY_HEAVY_EQUIPMENTS:
        weight *= 3
    elif weapon in LIGHT_EQUIPMENTS:
        weight /= 10

    return weight


def get_equipment_damage_type(weapon: str, rarity: str):
    '''Retorna uma lista com os tipos de dano de uma arma.
    '''
    damage_types = None
    if weapon in ALL_WEAPONS:
        damage_types = []
        chance = .5
        turns = BONUS_RARITY[rarity] - 1
        damages_list = [
            e for e in DamageEnum
            if e not in [DamageEnum.SLASHING, DamageEnum.BLUDGEONING,
                         DamageEnum.HITTING, DamageEnum.PIERCING]
        ]
        if weapon in SLASHING_WEAPONS:
            damage_types = [DamageEnum.SLASHING]
        elif weapon in BLUDGEONING_WEAPONS:
            damage_types = [DamageEnum.BLUDGEONING]
        elif weapon in PIERCING_WEAPONS:
            damage_types = [DamageEnum.PIERCING]
        elif weapon in MAGIC_WEAPONS:
            damage_types = [DamageEnum.MAGIC]
            damages_list.remove(DamageEnum.MAGIC)

        if weapon in ENCHANTED_WEAPONS:
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


def add_secret_stats(rarity: str, group_level: int):
    '''Retorna os atributos bônus do equipamento. 
    Esses atributos estarão disponíveis para o personagem quando 
    o item for identificado.
    Os bônus são selecionado de maneira aleatórios. O total de bônus é baseado 
    na raridade do item em na metade do nível de grupo.
    '''
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


def translate_material_name(
    equip_type: str, weapon: str, material: str,
) -> str:
    if equip_type in WEAPON_EQUIPMENTS_ENUM:
        index = WEAPON_MATERIALS[material] - 1
    elif equip_type in WEARABLE_EQUIPMENTS_ENUM:
        index = WEARABLE_MATERIALS[material] - 1
    elif equip_type in ACCESSORY_EQUIPMENTS_ENUM:
        index = ACCESSORY_MATERIALS[material] - 1

    if weapon in MAGICAL_QUILL_EQUIPMENTS:
        material_name = list(MagicalQuillMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif weapon in MAGICAL_GRIMOIRE_EQUIPMENTS:
        material_name = list(MagicalGrimoireMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    elif weapon in MAGICAL_STONES_EQUIPMENTS:
        material_name = list(MagicalStonesMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif weapon in MAGICAL_WEARABLE_EQUIPMENTS:
        material_name = list(MagicalWearableMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title() + "'s"
    elif weapon in MAGICAL_MASK_EQUIPMENTS:
        material_name = list(MagicalMaskMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    elif weapon in TATICAL_WEARABLE_EQUIPMENTS:
        material_name = list(TacticalWearableMaterialEnum)[index].name
        material_name = material_name.replace("_", " ").title()
    else:
        material_name = material.replace("_", " ").title()

    return material_name


def create_random_equipment(equip_type: str, group_level: int) -> Equipment:
    '''Retorna um equipamento aleatório.
    '''
    rarity = choice_rarity(group_level)
    weapon, material = get_equipment_and_material(equip_type, group_level)

    equip_name = weapon if weapon else equip_type
    print(f'Equipamento: {weapon}', end=' ')
    bonus, penality = get_bonus_and_penality(
        equip_type, rarity, material, group_level, True
    )
    attr_bonus_prob, attr_penality_prob = get_attribute_probabilities(
        equip_name
    )
    equipment_dict = defaultdict(int)
    for _ in range(bonus):
        attribute = weighted_choice(**attr_bonus_prob)
        equipment_dict[attribute] += 1

    for _ in range(penality):
        attribute = weighted_choice(**attr_penality_prob)
        equipment_dict[attribute] -= 1

    weight = get_equipment_weight(equip_type, rarity, material, weapon)
    rarity_name = rarity.replace("_", " ").title()
    material_name = translate_material_name(equip_type, weapon, material)
    equip_name = equip_name.replace('_', ' ').title()
    damage_types = get_equipment_damage_type(weapon, rarity)
    damage_type_name = get_equipment_damage_type_name(damage_types)
    name = (
        f'{rarity_name} '
        f'{material_name} '
        f'{equip_name}'
        f'{damage_type_name}'
    )
    secret_stats = add_secret_stats(rarity, group_level)
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


def create_random_consumable(group_level: int):
    '''Retorna um item consumível aleatório.
    '''
    item_model = ItemModel()
    rarity = choice_rarity(group_level)
    query = dict(rarity=rarity, _class={'$ne':'Equipment'})
    item_list = item_model.get_all(query=query)
    quantity = randint(1, 3)
    item = choice(item_list)
    item = Item(item, quantity)

    return item


def create_random_trap(group_level: int) -> int:
    trap_level = group_level
    trap_degree = randint(10, 20)

    return trap_level * trap_degree


def create_random_item(group_level: int) -> Union[Consumable, Equipment]:
    '''Função que retorna um item escolhido de maneira aleatória.
    '''
    base_level = group_level
    choiced_item = choice_type_item()
    equipment_types = [e.name for e in EquipmentEnum]
    if choiced_item == 'TRAP':
        items = create_random_trap(group_level)
    else:
        times = choice_total_times()
        items = []
        for _ in range(times):
            group_level = random_group_level(base_level)
            choiced_item = choice_type_item(no_trap=True)
            if choiced_item == 'CONSUMABLE':
                item = create_random_consumable(group_level)
            elif choiced_item in equipment_types:
                item = create_random_equipment(choiced_item, group_level)
            else:
                raise ValueError(
                    f'O item "{choiced_item}" não foi encontrado.'
                )
            items.append(item)

    return items


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

    # for _ in range(1000):
    #     items = create_random_item(1001)
    #     if isinstance(items, list):
    #         for item in items:
    #             if isinstance(item.item, Equipment):
    #                 print(f'\t{item.item.name}')
