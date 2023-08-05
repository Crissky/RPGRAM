from random import choices


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
    }
    return weighted_choice(**rarities)


if __name__ == '__main__':
    items = []
    for i in range(1000):
        items.append(choice_rarity())
    print(
        f"common: {items.count('common')}",
        f"uncommon: {items.count('uncommon')}",
        f"rare: {items.count('rare')}",
        f"epic: {items.count('epic')}",
        f"legendary: {items.count('legendary')}",
    )
