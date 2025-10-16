from typing import List
from random import choice, randint, random

from bson import ObjectId

from repository.mongo.models.classe import ClasseModel
from repository.mongo.models.race import RaceModel
from repository.mongo.populate.enemy_constants import (
    ARCHETYPES_EQUIPMENTS,
    NAMES,
    RACES_ALIGNMENT
)
from repository.mongo.populate.item import create_random_equipment
from repository.mongo.populate.tools import random_group_level, weighted_choice
from rpgram import Equips
from rpgram.boosters import Classe, Race
from rpgram.characters import NPCharacter
from rpgram.enums import AlignmentEnum, EnemyStarsEnum, EquipmentEnum
from rpgram.errors import RequirementError


def get_total_enemy(
    min_number_enemies: int = 1,
    max_number_enemies: int = 5
) -> int:
    '''Retorna o número total de inimigos que serão criados'''

    min_number_enemies -= 1
    if min_number_enemies == max_number_enemies:
        return min_number_enemies
    elif min_number_enemies > max_number_enemies:
        raise ValueError(
            'min_number_enemies deve ser menor que max_number_enemies'
        )

    probs_and_num_enemies = enumerate(range(
        max_number_enemies, min_number_enemies, -1
    ))
    number_enemies_probs = {
        f'{num_enemies}': probs + 1
        for probs, num_enemies in probs_and_num_enemies
    }
    return int(weighted_choice(**number_enemies_probs))


def random_enemy_level(enemy_level: int) -> int:
    '''Retorna um inteiro entre 90% e 100% do enemy_level.'''
    min_enemy_level = max(int(enemy_level * 0.9), 1)

    return randint(min_enemy_level, enemy_level)


def choice_enemy_name() -> str:
    '''Retorna um nome aleatório para o inimigo'''
    first_name = choice(NAMES)
    last_name = choice(NAMES)
    return f'{first_name} {last_name}'.strip()


def choice_enemy_star(no_boss: bool = False) -> str:
    '''Função que retorna um tipo de item aleatório.
    O tipo do item é retornado com base em sua propabilidade.
    '''
    enemy_stars = {
        EnemyStarsEnum.ONE.name: 1000,
        EnemyStarsEnum.TWO.name: 900,
        EnemyStarsEnum.THREE.name: 800,
        EnemyStarsEnum.FOUR.name: 700,
        EnemyStarsEnum.FIVE.name: 600,
        EnemyStarsEnum.SUB_BOSS.name: 300,
        EnemyStarsEnum.BOSS.name: 100,
    }

    if no_boss:
        enemy_stars.pop('SUB_BOSS')
        enemy_stars.pop('BOSS')

    return weighted_choice(**enemy_stars)


def choice_enemy_class_name() -> str:
    '''Retorna o nome aleatório de uma classe.'''
    classe_model = ClasseModel()
    classe_list = classe_model.get_all(fields=['name'])
    return choice(classe_list)


def choice_enemy_race_name() -> str:
    '''Retorna o nome aleatório de uma raça.'''
    race_model = RaceModel()
    race_list = race_model.get_all(fields=['name'])
    return choice(race_list)


def get_enemy_alignment(enemy_race: Race) -> AlignmentEnum:
    return choice(RACES_ALIGNMENT[enemy_race.name])


def get_enemy_equips(
    enemy_id: ObjectId,
    enemy_level: int,
    enemy_class_name: str
) -> Equips:
    ''''Retorna os equipamentos do inimigo baseado no arquétipo da classe.'''
    archetype_equipments = ARCHETYPES_EQUIPMENTS[enemy_class_name]
    hand = choice([EquipmentEnum.ONE_HAND, EquipmentEnum.TWO_HANDS])
    hand_list = archetype_equipments[hand.name]
    helmet_list = archetype_equipments[EquipmentEnum.HELMET.name]
    armor_list = archetype_equipments[EquipmentEnum.ARMOR.name]
    boots_list = archetype_equipments[EquipmentEnum.BOOTS.name]
    ring_list = archetype_equipments[EquipmentEnum.RING.name]
    amulet_list = archetype_equipments[EquipmentEnum.AMULET.name]

    equips_dict = {}
    equips_dict['left_hand'] = create_random_equipment(
        equip_type=hand.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(hand_list),
    ).item
    equips_dict['right_hand'] = None
    if hand == EquipmentEnum.ONE_HAND:
        equips_dict['right_hand'] = create_random_equipment(
            equip_type=hand.name,
            group_level=random_enemy_level(enemy_level),
            equip_class=choice(hand_list),
        ).item
    equips_dict['helmet'] = create_random_equipment(
        equip_type=EquipmentEnum.HELMET.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(helmet_list),
    ).item
    equips_dict['armor'] = create_random_equipment(
        equip_type=EquipmentEnum.ARMOR.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(armor_list),
    ).item
    equips_dict['boots'] = create_random_equipment(
        equip_type=EquipmentEnum.BOOTS.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(boots_list),
    ).item
    equips_dict['ring'] = create_random_equipment(
        equip_type=EquipmentEnum.RING.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(ring_list),
    ).item
    equips_dict['amulet'] = create_random_equipment(
        equip_type=EquipmentEnum.AMULET.name,
        group_level=random_enemy_level(enemy_level),
        equip_class=choice(amulet_list),
    ).item

    for equipment in equips_dict.values():
        if equipment and equipment.identifiable:
            equipment.identify()

    return Equips(
        player_id=enemy_id,
        **equips_dict,
    )


def create_enemy(
    enemy_level: int,
    enemy_name: str,
    enemy_stars: str,
    enemy_class_name: str,
    enemy_race_name: str,
) -> NPCharacter:
    classe_model = ClasseModel()
    race_model = RaceModel()
    enemy_class: Classe = classe_model.get(enemy_class_name)
    enemy_race: Race = race_model.get(enemy_race_name)
    enemy_alignment = get_enemy_alignment(enemy_race)
    enemy_id = ObjectId()
    equips = get_enemy_equips(enemy_id, enemy_level, enemy_class_name)
    enemy = NPCharacter(
        char_name=enemy_name,
        classe=enemy_class,
        race=enemy_race,
        alignment=enemy_alignment,
        equips=equips,
        level=enemy_level,
        stars=enemy_stars,
        enemy_id=enemy_id,
    )

    return enemy


def distribute_stats(enemy_char: NPCharacter) -> NPCharacter:
    base_stats_probs = {
        'FOR': enemy_char.base_stats.multiplier_strength ** 2,
        'DES': enemy_char.base_stats.multiplier_dexterity ** 2,
        'CON': enemy_char.base_stats.multiplier_constitution ** 2,
        'INT': enemy_char.base_stats.multiplier_intelligence ** 2,
        'SAB': enemy_char.base_stats.multiplier_wisdom ** 2,
        'CAR': enemy_char.base_stats.multiplier_charisma ** 2,
    }
    base_stats_list = list(base_stats_probs.keys())
    total_base_stats = len(base_stats_list)
    partial_base_stats_points = int(enemy_char.base_stats.points * 0.40)

    # Distribui os pontos de forma parcial e uniforme
    for i in range(partial_base_stats_points):
        stats_name = base_stats_list[i % total_base_stats]
        enemy_char.base_stats[stats_name] = 1

    # Distribui os pontos de forma ponderada
    for _ in range(enemy_char.base_stats.points):
        stats_name = weighted_choice(**base_stats_probs)
        enemy_char.base_stats[stats_name] = 1

    return enemy_char


def learn_skills(enemy_char: NPCharacter) -> NPCharacter:
    skill_list = enemy_char.skill_tree.learnable_skill_list
    for skill_class in skill_list:
        try:
            enemy_char.skill_tree.learn_skill(skill_class)
        except RequirementError as error:
            print(
                f'O inimigo [{enemy_char.full_name}] '
                'não pode aprender a habilidade '
                f'{skill_class.NAME}(RANK{skill_class.RANK}) '
                'porque:',
                error
            )

    return enemy_char


def distribute_skill_points(enemy_char: NPCharacter) -> NPCharacter:
    skill_points = enemy_char.skill_tree.current_skill_points
    skill_list = enemy_char.skill_tree.skill_list
    total_skills = len(skill_list)

    if enemy_char.skill_tree.have_skill_points and skill_list:
        for index in range(skill_points):
            skill = skill_list[index % total_skills]
            enemy_char.skill_tree.upgrade_skill(skill)

    return enemy_char


def add_buffs(enemy_list: List[NPCharacter]) -> List[NPCharacter]:
    for enemy in enemy_list:
        skill_list = enemy.skill_tree.get_buff_skill_list()
        for skill in skill_list:
            # print(f'SKILL NAME: {skill.name}[{skill.skill_type}]')
            if skill.is_self_target_skill:
                skill.function()
            else:
                for e in enemy_list:
                    if random() >= 0.60:
                        skill.function(e)

    return enemy_list


def create_random_enemies(
    group_level: int,
    no_boss: bool = False,
    num_min_enemies: int = 1,
    num_max_enemies: int = 5,
) -> List[NPCharacter]:
    '''Cria inimigos de maneira aleatória.'''

    total_enemy = get_total_enemy(num_min_enemies, num_max_enemies)
    enemy_list = []
    for _ in range(total_enemy):
        enemy_level = random_group_level(group_level)
        enemy_name = choice_enemy_name()
        enemy_stars = choice_enemy_star(no_boss=no_boss)
        enemy_class_name = choice_enemy_class_name()
        enemy_race_name = choice_enemy_race_name()
        enemy_char = create_enemy(
            enemy_level=enemy_level,
            enemy_name=enemy_name,
            enemy_stars=enemy_stars,
            enemy_class_name=enemy_class_name,
            enemy_race_name=enemy_race_name,
        )
        enemy_char = distribute_stats(enemy_char)
        enemy_char = learn_skills(enemy_char)
        enemy_char = distribute_skill_points(enemy_char)
        enemy_list.append(enemy_char)

        if enemy_char.is_any_boss:
            no_boss = True

    enemy_list = add_buffs(enemy_list)

    return enemy_list


if __name__ == '__main__':
    from collections import Counter
    items = []
    for i in range(1000):
        items.append(choice_enemy_star())
    result = Counter(items)
    for item in result.most_common():
        print(f'{item[0]}: {item[1]},', end=' ')
    print()
    enemy_list = create_random_enemies(
        group_level=100,
        num_min_enemies=90,
        num_max_enemies=100,
    )
    for enemy in enemy_list:
        print(enemy.get_all_sheets(verbose=False))
        print(enemy.to_dict())
        print(enemy.skill_tree)
