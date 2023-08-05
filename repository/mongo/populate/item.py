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


def choice_rarity():
    items = {
        'common': 100,
        'uncommon': 50,
        'rare': 25,
        'epic': 12.5,
        'legendary': 6.25,
    }
    return weighted_choice(**items)


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
