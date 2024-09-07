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


def get_enum_by_index(enum_class: Enum, index: int):
    ''' Retorna o elemento de uma classe Enum a partir de um índice.
    '''

    if not issubclass(enum_class, Enum):
        raise TypeError('"enum_class" precisa ser uma instancia de Enum.')

    if not isinstance(index, int):
        raise TypeError('"index" precisa ser um inteiro.')

    enum_list = list(enum_class)
    enum_name = enum_list[index]

    return enum_name


if __name__ == '__main__':
    class TestEnum(Enum):
        A = 1
        B = 2
        C = 3
        D = 4

    print(get_enum_index(TestEnum.C))
    print(get_enum_by_index(TestEnum, 1))
    print(get_enum_by_index(TestEnum, get_enum_index(TestEnum.C)))