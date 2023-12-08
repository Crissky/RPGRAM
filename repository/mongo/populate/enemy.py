from typing import List
from repository.mongo.models.classe import ClasseModel
from repository.mongo.models.race import RaceModel
from repository.mongo.populate.enemy_constants import NAMES
from repository.mongo.populate.tools import random_group_level, weighted_choice
from rpgram.characters import NPCharacter
from rpgram.enums import EnemyStarsEnum
from random import choice


POINTS_MULTIPLIER = {
    EnemyStarsEnum.ONE.name: 2,
    EnemyStarsEnum.TWO.name: 3,
    EnemyStarsEnum.THREE.name: 5,
    EnemyStarsEnum.FOUR.name: 7,
    EnemyStarsEnum.FIVE.name: 11,
    EnemyStarsEnum.BOSS.name: 28,
}


def get_total_enemy(max_number_enemies: int = 5) -> int:
    '''Retorna o número total de inimigos que serão criados'''
    number_enemies_probs = {
        f'{i+1}': j
        for i, j in enumerate(range(max_number_enemies, 0, -1))
    }
    return int(weighted_choice(**number_enemies_probs))


def choice_enemy_name() -> str:
    '''Retorna um nome aleatório para o inimigo'''
    first_name = choice(NAMES)
    last_name = choice(NAMES)
    return f'{first_name} {last_name}'.strip()


def choice_enemy_star(no_boss: bool = False) -> str:
    '''Função que retorna um tipo de item aleatório.
    O tipo do item é retornado com base em sua propabilidade.
    '''
    types_item = {
        EnemyStarsEnum.ONE.name: 1000,
        EnemyStarsEnum.TWO.name: 900,
        EnemyStarsEnum.THREE.name: 800,
        EnemyStarsEnum.FOUR.name: 700,
        EnemyStarsEnum.FIVE.name: 600,
        EnemyStarsEnum.BOSS.name: 100,
    }

    if no_boss:
        types_item.pop('TRAP')

    return weighted_choice(**types_item)


def choice_enemy_class_name() -> str:
    classe_model = ClasseModel()
    classe_list = classe_model.get_all(fields=['name'])
    return choice(classe_list)


def choice_enemy_race_name() -> str:
    race_model = RaceModel()
    race_list = race_model.get_all(fields=['name'])
    return choice(race_list)


def create_enemy(
    enemy_level: int,
    enemy_name: str,
    enemy_stars: str,
    enemy_class_name: str,
    enemy_race_name: str,
) -> NPCharacter:
    classe_model = ClasseModel()
    race_model = RaceModel()
    enemy_points_multiplier = POINTS_MULTIPLIER[enemy_stars]
    enemy_class = classe_model.get(enemy_class_name)
    enemy_race = race_model.get(enemy_race_name)
    enemy = NPCharacter(
        char_name=enemy_name,
        classe=enemy_class,
        race=enemy_race,
        level=enemy_level,
        points_multiplier=enemy_points_multiplier
    )

    return enemy


def create_random_enemy(
    group_level: int,
    no_boss: bool = False
) -> List[NPCharacter]:
    '''Cria inimigos de maneira aleatória.'''
    total_enemy = get_total_enemy()
    enemy_list = []
    for _ in range(total_enemy):
        enemy_level = random_group_level(group_level)
        enemy_name = choice_enemy_name()
        enemy_stars = choice_enemy_star(no_boss=no_boss)
        enemy_class_name = choice_enemy_class_name()
        enemy_race_name = choice_enemy_race_name()
        enemy_list.append(
            create_enemy(
                enemy_level=enemy_level,
                enemy_name=enemy_name,
                enemy_stars=enemy_stars,
                enemy_class_name=enemy_class_name,
                enemy_race_name=enemy_race_name,
            )
        )
        if EnemyStarsEnum.BOSS.name == enemy_stars:
            no_boss = True

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
    print(choice_enemy_class_name())
    print(choice_enemy_race_name())
    print(create_random_enemy(10))
