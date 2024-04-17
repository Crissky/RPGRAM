'''
Dice multiplier percent base (0.025)
01: 1.025
02: 1.05
03: 1.075
04: 1.10
05: 1.125
06: 1.15
07: 1.175
08: 1.20
09: 1.225
10: 1.25
11: 1.275
12: 1.30
13: 1.325
14: 1.35
15: 1.375
16: 1.40
17: 1.425
18: 1.45
19: 1.475
20: 1.50
'''

from random import randint


class Dice:
    def __init__(self, faces: int = 20, base_multiplier: float = 0.025):
        self.__faces = faces
        self.__base_multiplier = base_multiplier
        self.__value = None
        self.__boosted_value = None

    def throw(self, rethrow=False) -> int:
        if self.is_throwed and not rethrow:
            return self.__value
        self.__value = randint(1, self.__faces)
        return self.__value

    def check_throw(self):
        if not self.__value:
            raise ValueError('O dado não foi lançado. Use o método throw.')

    def boost_value(self, base_value: int) -> int:
        '''Retorna o valor boostado conforme o resultado do dado.
        '''

        self.throw(rethrow=False)
        multiplier = (1 + (self.value * self.base_multiplier))
        boosted_value = base_value * multiplier
        added_value = base_value + self.value
        result = max(boosted_value, added_value)

        if self.is_critical:
            result = result * self.critical_multiplier
        elif self.is_critical_fail:
            result = result / self.critical_multiplier

        self.__boosted_value = int(result)

        return self.__boosted_value

    @property
    def value(self) -> int:
        self.check_throw()
        return self.__value

    @property
    def base_multiplier(self) -> float:
        return self.__base_multiplier

    @property
    def boosted_value(self) -> int:
        if self.__boosted_value is None:
            raise ValueError(
                'Valor não foi boostado, use o método boost_value.'
            )

        return self.__boosted_value

    @property
    def is_critical(self) -> int:
        self.check_throw()
        return self.__value == self.__faces and self.__value > 1

    @property
    def is_critical_fail(self) -> int:
        self.check_throw()
        return self.__value == 1 and self.__faces > 1

    @property
    def critical_multiplier(self) -> float:
        multiplier = 1.00
        if self.__faces <= 5:
            multiplier = 1.25
        elif self.__faces <= 10:
            multiplier = 1.50
        elif self.__faces <= 15:
            multiplier = 1.75
        elif self.__faces > 15:
            multiplier = 2.00

        return multiplier

    @property
    def text(self) -> str:
        self.check_throw()
        text = f'🎲: {self.__value}'
        if self.is_critical:
            text += '(Crítico!)'
        if self.is_critical_fail:
            text += '(Falha Crítica!)'
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
    print(dice.boost_value(100))
