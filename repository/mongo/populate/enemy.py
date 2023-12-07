from repository.mongo.populate.tools import random_group_level, weighted_choice
from rpgram.characters import NPCharacter
from rpgram.enums import EnemyStarsEnum


def get_total_enemy(max_number_enemies: int = 5):
    '''Retorna o número total de inimigos que serão criados'''
    number_enemies_probs = {
        f'{i+1}': j
        for i, j in enumerate(range(max_number_enemies, 0, -1))
    }
    return weighted_choice(**number_enemies_probs)


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


def create_random_enemy(
    group_level: int,
    no_boss: bool = False
) -> NPCharacter:
    '''Cria inimigos de maneira aleatória.'''
    total_enemy = get_total_enemy()
    for _ in range(total_enemy):
        enemy_level = random_group_level(group_level)
        enemy_stars = choice_enemy_star(no_boss=no_boss)
        if EnemyStarsEnum.BOSS.name == enemy_stars:
            no_boss = True


if __name__ == '__main__':
    from collections import Counter
    items = []
    for i in range(1000):
        items.append(choice_enemy_star())
    result = Counter(items)
    for item in result.most_common():
        print(f'{item[0]}: {item[1]},', end=' ')
    print()
