from random import randint
from typing import Dict, List, Tuple, Union

from rpgram.conditions.debuff import (
    BerserkerCondition,
    BleedingCondition,
    BlindnessCondition,
    BurnCondition,
    ConfusionCondition,
    CurseCondition,
    ExhaustionCondition,
    FrozenCondition,
    ParalysisCondition,
    PetrifiedCondition,
    PoisoningCondition,
    SilenceCondition,
    StunnedCondition
)
from rpgram.enums.damage import DamageEmojiEnum, DamageEnum


class SpecialDamage:
    def __init__(
        self,
        base_damage: int,
        damage_type: Union[str, DamageEnum],
        status_multiplier: int = 1,
    ):
        if isinstance(damage_type, str):
            damage_type = DamageEnum[damage_type]
        if not isinstance(damage_type, DamageEnum):
            raise ValueError(
                f'damage_type precisa ser uma string ou DamageEnum. '
                f'"{type(damage_type)}" não é válido.'
            )
        if status_multiplier < 1:
            raise ValueError(
                f'status_multiplier precisa ser maior que zero. '
                f'"{status_multiplier}".'
            )

        self.__base_damage = int(base_damage)
        self.__damage_type = damage_type
        self.__status_multiplier = int(status_multiplier)
        self.__damage = None

    def roll_damage(self, reroll: bool = False) -> int:
        if self.__damage is None or reroll is True:
            self.__damage = randint(self.min_damage, self.max_damage)

        return self.__damage

    # Getters
    @property
    def base_damage(self) -> int:
        return self.__base_damage

    @property
    def min_damage(self) -> int:
        '''Retorna o dano mínimo obtido pelo multiplicador do dano. 
        Sendo 1 o menor valor possível.
        '''

        return max(
            int(self.base_damage * self.__damage_multipliers['min']),
            1
        )

    @property
    def max_damage(self) -> int:
        '''Retorna o dano máximo obtido pelo multiplicador do dano. 
        Sendo 2 o menor valor possível.
        '''

        return max(
            int(self.base_damage * self.__damage_multipliers['max']),
            2
        )

    @property
    def damage_type(self) -> DamageEnum:
        return self.__damage_type

    @property
    def damage_name(self) -> str:
        '''Retorna o nome do type dano.'''

        return self.__damage_type.value

    @property
    def damage_emoji(self) -> str:
        '''Retorna o emoji do type dano.'''

        return DamageEmojiEnum[self.__damage_type.name].value

    @property
    def damage(self) -> int:
        '''Retorna o dano obtido aleatóriamente entre o min_damage e o 
        max_damage.
        '''

        return self.roll_damage()

    @property
    def damage_text(self) -> str:
        '''Retorna o texto com o nome do dano e o dano.'''

        return f'{self.damage_name}: {self.damage}'

    @property
    def damage_emoji_text(self) -> str:
        '''Retorna o texto com o emoji do dano e o dano.'''

        return f'{self.damage_emoji}({self.damage})'

    @property
    def damage_full_text(self) -> str:
        '''Retorna o emoji, o nome do dano e o dano'''

        return f'{self.damage_emoji}{self.damage_text}'

    @property
    def damage_help_text(self) -> str:
        '''Retorna texto com o nome do dano e o range do dano.'''

        return f'{self.damage_name}: {self.min_damage}-{self.max_damage}'

    @property
    def __damage_multipliers(self) -> Dict[str, float]:
        '''Retorna os multiplicadores do dano mínimo e máximo.'''

        if self.damage_type == DamageEnum.HITTING:
            min_multiplier = 0.35
            max_multiplier = 0.55
        elif self.damage_type == DamageEnum.SLASHING:
            min_multiplier = 0.50
            max_multiplier = 0.80
        elif self.damage_type == DamageEnum.PIERCING:
            min_multiplier = 0.40
            max_multiplier = 0.60
        elif self.damage_type == DamageEnum.MAGIC:
            min_multiplier = 0.30
            max_multiplier = 0.42
        elif self.damage_type == DamageEnum.BLESSING:
            min_multiplier = -0.45
            max_multiplier = -0.70
        elif self.damage_type == DamageEnum.DIVINE:
            min_multiplier = 0.97
            max_multiplier = 1.74
        elif self.damage_type == DamageEnum.LIGHT:
            min_multiplier = 0.70
            max_multiplier = 1.19
        elif self.damage_type == DamageEnum.DARK:
            min_multiplier = 0.62
            max_multiplier = 1.04
        elif self.damage_type == DamageEnum.FIRE:
            min_multiplier = 0.18
            max_multiplier = 1.40
        elif self.damage_type == DamageEnum.WATER:
            min_multiplier = 0.43
            max_multiplier = 0.66
        elif self.damage_type == DamageEnum.COLD:
            min_multiplier = 0.36
            max_multiplier = 0.53
        elif self.damage_type == DamageEnum.LIGHTNING:
            min_multiplier = 0.57
            max_multiplier = 0.94
        elif self.damage_type == DamageEnum.WIND:
            min_multiplier = 0.42
            max_multiplier = 0.61
        elif self.damage_type == DamageEnum.ROCK:
            min_multiplier = 0.45
            max_multiplier = 0.70
        elif self.damage_type == DamageEnum.GROUND:
            min_multiplier = 0.09
            max_multiplier = 1.05
        elif self.damage_type == DamageEnum.ACID:
            min_multiplier = 0.52
            max_multiplier = 0.84
        elif self.damage_type == DamageEnum.POISON:
            min_multiplier = 0.56
            max_multiplier = 0.91
        elif self.damage_type == DamageEnum.CHAOS:
            min_multiplier = 0.06
            max_multiplier = 1.72

        return {'min': min_multiplier, 'max': max_multiplier}

    @property
    def condition_ratio_list(self) -> List[dict]:
        '''Retorna uma lista de dicionários, condition_ratio 
        (Dict[condition, ratio]), com o percentual de chance (ratio: float)
        de causar a condition(Condition).
        '''

        condition_list = []
        if self.damage_type == DamageEnum.HITTING:
            condition_list.extend([
                dict(condition=StunnedCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.SLASHING:
            condition_list.extend([
                dict(condition=BleedingCondition, ratio=0.25),
            ])
        elif self.damage_type == DamageEnum.PIERCING:
            condition_list.extend([
                dict(condition=BleedingCondition, ratio=0.10),
                dict(condition=BleedingCondition, ratio=0.10),
                dict(condition=BleedingCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.MAGIC:
            condition_list.extend([
                dict(condition=BlindnessCondition, ratio=0.05),
                dict(condition=BurnCondition, ratio=0.05),
                dict(condition=ConfusionCondition, ratio=0.05),
                dict(condition=ExhaustionCondition, ratio=0.05),
                dict(condition=FrozenCondition, ratio=0.05),
                dict(condition=ParalysisCondition, ratio=0.05),
                dict(condition=PetrifiedCondition, ratio=0.05),
                dict(condition=PoisoningCondition, ratio=0.05),
                dict(condition=SilenceCondition, ratio=0.05),
                dict(condition=StunnedCondition, ratio=0.05),
            ])
        elif self.damage_type == DamageEnum.BLESSING:
            condition_list.extend([
                dict(condition=SilenceCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.DIVINE:
            condition_list.extend([
                dict(condition=BerserkerCondition, ratio=0.10),
                dict(condition=BleedingCondition, ratio=0.10),
                dict(condition=BlindnessCondition, ratio=0.10),
                dict(condition=BurnCondition, ratio=0.10),
                dict(condition=ConfusionCondition, ratio=0.10),
                dict(condition=CurseCondition, ratio=0.10),
                dict(condition=ExhaustionCondition, ratio=0.10),
                dict(condition=FrozenCondition, ratio=0.10),
                dict(condition=ParalysisCondition, ratio=0.10),
                dict(condition=PetrifiedCondition, ratio=0.10),
                dict(condition=PoisoningCondition, ratio=0.10),
                dict(condition=SilenceCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.LIGHT:
            condition_list.extend([
                dict(condition=BlindnessCondition, ratio=0.10),
                dict(condition=ConfusionCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.DARK:
            condition_list.extend([
                dict(condition=BlindnessCondition, ratio=0.10),
                dict(condition=ConfusionCondition, ratio=0.10),
                dict(condition=CurseCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.FIRE:
            condition_list.extend([
                dict(condition=BurnCondition, ratio=0.10),
                dict(condition=BurnCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.WATER:
            condition_list.extend([
                dict(condition=StunnedCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.COLD:
            condition_list.extend([
                dict(condition=FrozenCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.LIGHTNING:
            condition_list.extend([
                dict(condition=ParalysisCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.WIND:
            condition_list.extend([
                dict(condition=StunnedCondition, ratio=0.10),
                dict(condition=BleedingCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.ROCK:
            condition_list.extend([
                dict(condition=StunnedCondition, ratio=0.10),
                dict(condition=StunnedCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.GROUND:
            condition_list.extend([
                dict(condition=StunnedCondition, ratio=0.10),
                dict(condition=StunnedCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.ACID:
            condition_list.extend([
                dict(condition=BurnCondition, ratio=0.10),
                dict(condition=PoisoningCondition, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.POISON:
            condition_list.extend([
                dict(condition=PoisoningCondition, ratio=0.15),
                dict(condition=PoisoningCondition, ratio=0.15),
            ])
        elif self.damage_type == DamageEnum.CHAOS:
            condition_list.extend([
                dict(condition=CurseCondition, ratio=0.10),
                dict(condition=CurseCondition, ratio=0.10),
                dict(condition=CurseCondition, ratio=0.10),
            ])

        return condition_list * self.__status_multiplier

    status = status_list = condition_list = condition_ratio_list
    text = damage_help_text
    full_text = damage_full_text

    def __str__(self):
        return self.damage_help_text

    def __repr__(self):
        return f'<{self.damage_help_text}>'


if __name__ == '__main__':
    spec_dmg = SpecialDamage(100, DamageEnum.HITTING)
    print(spec_dmg)
    print(spec_dmg.damage)
    print(spec_dmg.damage_text)
    print(spec_dmg.damage_emoji_text)
    print(spec_dmg.damage_full_text)
    spec_dmg.roll_damage(True)
    print(spec_dmg.damage)
    print(spec_dmg.damage_text)
    print(spec_dmg.damage_emoji_text)
    print(spec_dmg.damage_full_text)
