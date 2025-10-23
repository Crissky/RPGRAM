from random import choice, choices, randint
from typing import Hashable

from rpgram.enums import RarityEnum


def weighted_choice(**items) -> Hashable:
    '''Função que retorna um item escolhido de maneira aleatória.
    O item tem chance de ser selecionado baseado em sua probabilidade.
    O parâmetro items deve ser um kwargs, em que a chave é o item
    e o valor a propabilidade de ser escolhido.
    '''
    population = list(items.keys())
    weights = items.values()
    return choices(population, weights=weights)[0]


def random_group_level(level: int) -> int:
    '''Função que retorna um valor inteiro aleatório entre 75% e 125% do
    level passado. No entando, o menor valor retornado sempre será 1.
    '''
    min_level = max(int(level - 10), 1)
    max_level = int(level + 10)
    new_level = choice(range(min_level, max_level))
    return new_level


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
