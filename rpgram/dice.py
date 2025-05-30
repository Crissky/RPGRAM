'''
Dice multiplier percent base (0.025, 0.035)
01: 1.025, 1.035
02: 1.050, 1.070
03: 1.075, 1.105
04: 1.100, 1.140
05: 1.125, 1.175
06: 1.150, 1.210
07: 1.175, 1.245
08: 1.200, 1.280
09: 1.225, 1.315
10: 1.250, 1.350
11: 1.275, 1.385
12: 1.300, 1.420
13: 1.325, 1.455
14: 1.350, 1.490
15: 1.375, 1.525
16: 1.400, 1.560
17: 1.425, 1.595
18: 1.450, 1.630
19: 1.475, 1.665
20: 1.500, 1.700
'''

from random import randint
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter
    from rpgram.skills.skill_base import BaseSkill
    from rpgram.stats.stats_base import BaseStats
    from rpgram.stats.stats_combat import CombatStats


class Dice:
    def __init__(
        self,
        character: 'BaseCharacter',
        skill: 'BaseSkill' = None,
        faces: int = 20,
        base_multiplier: float = None,
    ):
        self.__value = None
        self.__character = character
        self.__skill = skill
        self.__base_stats = character.base_stats
        self.__combat_stats = character.combat_stats
        self.__faces = faces

        if not isinstance(base_multiplier, float):
            base_multiplier = 0.025
        if not isinstance(base_multiplier, float) and self.is_player:
            base_multiplier = 0.030

        self.__base_multiplier = base_multiplier

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
    def character(self) -> 'BaseCharacter':
        return self.__character
    char = character

    @property
    def base_stats(self) -> 'BaseStats':
        return self.__base_stats

    @property
    def combat_stats(self) -> 'CombatStats':
        return self.__combat_stats

    @property
    def skill(self) -> 'BaseSkill':
        return self.__skill

    @property
    def rate_hit_points(self) -> float:
        return self.combat_stats.rate_hit_points
    rate_hp = rate_hit_points

    @property
    def irate_hit_points(self) -> float:
        return self.combat_stats.irate_hit_points
    irate_hp = irate_hit_points

    @property
    def is_enemy(self) -> bool:
        return self.character.is_enemy

    @property
    def is_player(self) -> bool:
        return self.character.is_player

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
        if self.skill is not None:
            return self.skill.hit
        return self.combat_stats.hit

    @property
    def base_evasion(self) -> int:
        return self.combat_stats.evasion

    @property
    def base_power(self) -> int:
        return self.skill.power

    base_skill_power = base_power

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

    @property
    def boosted_power(self) -> int:
        return self.__boost_value(self.base_power)

    boosted_skill_power = boosted_power

    def __repr__(self) -> str:
        skill_name = ''
        if self.skill:
            skill_name = f'skill={self.skill.name}'

        return f'Dice(value={self.value}, char={self.char.name}, {skill_name})'


if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    from rpgram.skills.basic_attack import PhysicalAttackSkill
    phy_atk = PhysicalAttackSkill(char=BASE_CHARACTER)

    dice = Dice(character=BASE_CHARACTER, skill=phy_atk, faces=20)
    dice.throw()
    print(dice)
    print(dice.value)
    print(dice.text)
    print(dice.throw())
    print(dice.throw())
    print(dice.throw(rethrow=True))
    print('BASE PHYSICAL ATTACK:', dice.base_physical_attack)
    print('BOOSTED PHYSICAL ATTACK:', dice.boosted_physical_attack)
    print('BASE SKILL POWER:', dice.base_power)
    print('BOOSTED SKILL POWER:', dice.boosted_power)
