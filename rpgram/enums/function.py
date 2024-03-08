from enum import Enum


def get_enum_index(enum_instance: Enum):
    ''' Retorna o índice de um elemento de qualquer classe Enum considerando
    a ordem de instância.
    '''

    if not isinstance(enum_instance, Enum):
        raise TypeError('"enum_instance" precisa ser uma instancia de Enum.')

    enum_list = list(enum_instance.__class__)
    index = enum_list.index(enum_instance)

    return index
