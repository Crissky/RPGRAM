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

from rpgram.stats.stats_base import BaseStats
from rpgram.stats.stats_combat import CombatStats


class Dice:
    def __init__(
        self,
        character,
        faces: int = 20,
        base_multiplier: float = 0.025,
    ):
        self.__faces = faces
        self.__base_multiplier = base_multiplier
        self.__value = None
        self.__boosted_base_value = None
        self.__character = character
        self.__base_stats = character.base_stats
        self.__combat_stats = character.combat_stats

    def throw(self, rethrow=False) -> int:
        if self.is_throwed and not rethrow:
            return self.__value
        self.__value = randint(1, self.__faces)

        return self.__value

    def __boost_value(self, base_value: int) -> int:
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

        return int(result)

    def get_base_stats(self, attribute_name: str) -> int:
        return self.combat_stats[attribute_name]

    def get_boosted_stats(self, attribute_name: str) -> int:
        combat_stats = self.get_base_stats(attribute_name)

        return self.__boost_value(combat_stats)

    @property
    def value(self) -> int:
        self.throw(rethrow=False)
        return self.__value

    dice_value = value

    @property
    def base_multiplier(self) -> float:
        return self.__base_multiplier

    @property
    def is_critical(self) -> int:
        self.throw(rethrow=False)
        return self.__value == self.__faces and self.__faces > 1

    @property
    def is_critical_fail(self) -> int:
        self.throw(rethrow=False)
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
        self.throw(rethrow=False)
        text = f'🎲: {self.__value}'
        if self.is_critical:
            text += '(Crítico!)'
        if self.is_critical_fail:
            text += '(Falha Crítica!)'
        return text

    @property
    def is_throwed(self) -> bool:
        return bool(self.__value)

    @property
    def base_stats(self) -> BaseStats:
        return self.__base_stats

    @property
    def combat_stats(self) -> CombatStats:
        return self.__combat_stats

    # BASE STATS
    @property
    def base_initiative(self) -> int:
        return self.combat_stats.initiative

    @property
    def base_physical_attack(self) -> int:
        return self.combat_stats.physical_attack

    @property
    def base_precision_attack(self) -> int:
        return self.combat_stats.precision_attack

    @property
    def base_magical_attack(self) -> int:
        return self.combat_stats.magical_attack

    @property
    def base_physical_defense(self) -> int:
        return self.combat_stats.physical_defense

    @property
    def base_magical_defense(self) -> int:
        return self.combat_stats.magical_defense

    @property
    def base_hit(self) -> int:
        return self.combat_stats.hit

    @property
    def base_evasion(self) -> int:
        return self.combat_stats.evasion

    # BOOSTED STATS
    @property
    def boosted_initiative(self) -> int:
        return self.__boost_value(self.base_initiative)

    @property
    def boosted_physical_attack(self) -> int:
        return self.__boost_value(self.base_physical_attack)

    @property
    def boosted_precision_attack(self) -> int:
        return self.__boost_value(self.base_precision_attack)

    @property
    def boosted_magical_attack(self) -> int:
        return self.__boost_value(self.base_magical_attack)

    @property
    def boosted_physical_defense(self) -> int:
        return self.__boost_value(self.base_physical_defense)

    @property
    def boosted_magical_defense(self) -> int:
        return self.__boost_value(self.base_magical_defense)

    @property
    def boosted_hit(self) -> int:
        return self.__boost_value(self.base_hit)

    @property
    def boosted_evasion(self) -> int:
        return self.__boost_value(self.base_evasion)
