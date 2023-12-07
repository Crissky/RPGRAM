from random import choices
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
