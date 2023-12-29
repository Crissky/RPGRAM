from random import randint


class Dice:
    def __init__(self, faces: int = 20) -> None:
        self.__faces = faces
        self.__value = None

    def throw(self, rethrow=False) -> int:
        if self.is_throwed and not rethrow:
            return self.__value
        self.__value = randint(1, self.__faces)
        return self.__value

    def check_throw(self):
        if not self.__value:
            raise ValueError('O dado não foi lançado. Use o método throw.')

    @property
    def value(self) -> int:
        self.check_throw()
        return self.__value

    @property
    def is_critical(self) -> int:
        self.check_throw()
        return self.__value == self.__faces and self.__value > 1

    @property
    def text(self) -> str:
        self.check_throw()
        text = f'🎲: {self.__value}'
        if self.is_critical:
            text += '(Crítico!)'
        return text

    @property
    def is_throwed(self) -> bool:
        return bool(self.__value)


if __name__ == '__main__':
    dice = Dice()
    dice.throw()
    print(dice.value)
    print(dice.text)
    print(dice.throw())
    print(dice.throw())
    print(dice.throw(rethrow=True))
