from random import choice, choices
from typing import Hashable


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
