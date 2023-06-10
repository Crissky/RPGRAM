import random


class Dice:
    def __init__(self, faces: int = 20) -> None:
        self.__faces = faces
        self.__value = None

    def throw(self):
        self.__value = random.randint(1, self.__faces)
        return self.__value

    @property
    def value(self):
        if not self.__value:
            raise ValueError('O dado não foi lançado. Use o método throw.')
        return self.__value

    @property
    def is_critical(self):
        if not self.__value:
            raise ValueError('O dado não foi lançado. Use o método throw.')
        return self.__value == self.__faces
