from rpgram.characters import NPCharacter


def create_random_enemy(group_level: int) -> NPCharacter:
    '''Cria inimigos de maneira aleatória.'''
    max_number_enemies = 5
    number_enemies_probs = {
        i+1: j+1
        for i, j in enumerate(range(max_number_enemies, -1, -1))
    }
    