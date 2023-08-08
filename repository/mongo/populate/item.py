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
    for i in range(1000):
        items.append(choice_armor_material())
    print(
        f"cloth: {items.count('cloth')}",
        f"leather: {items.count('leather')}",
        f"iron: {items.count('iron')}",
        f"steel: {items.count('steel')}",
        f"runite: {items.count('runite')}",
        f"mithril: {items.count('mithril')}",
        f"adamantium: {items.count('adamantium')}",
    )
