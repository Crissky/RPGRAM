from random import randint
from typing import List, Tuple, Union

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
from rpgram.enums.damage import DamageEnum


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

    @property
    def base_damage(self) -> int:
        return self.__base_damage

    @property
    def min_damage(self) -> int:
        '''Retorna o dano mínimo obtido pelo multiplicador do dano. 
        Sendo 1 o menor valor possível.
        '''

        return max(
            int(self.base_damage * self.__damage_multipliers[0]),
            1
        )

    @property
    def max_damage(self) -> int:
        '''Retorna o dano máximo obtido pelo multiplicador do dano. 
        Sendo 2 o menor valor possível.
        '''

        return max(
            int(self.base_damage * self.__damage_multipliers[1]),
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
    def damage(self) -> int:
        '''Retorna o dano obtido aleatóriamente entre o min_damage e o 
        max_damage.
        '''

        return randint(self.min_damage, self.max_damage)

    @property
    def damage_text(self):
        '''Retorna texto com o nome do dano e o range do dano.'''

        return f'{self.damage_name}: {self.min_damage}-{self.max_damage}'

    @property
    def __damage_multipliers(self) -> Tuple[float, float]:
        '''Retorna os multiplicadores do dano mínimo e máximo.'''

        if self.damage_type == DamageEnum.HITTING:
            min_multiplier = 0.15
            max_multiplier = 0.35
        elif self.damage_type == DamageEnum.SLASHING:
            min_multiplier = 0.30
            max_multiplier = 0.60
        elif self.damage_type == DamageEnum.PIERCING:
            min_multiplier = 0.20
            max_multiplier = 0.40
        elif self.damage_type == DamageEnum.MAGIC:
            min_multiplier = 0.10
            max_multiplier = 0.22
        elif self.damage_type == DamageEnum.BLESSING:
            min_multiplier = -0.25
            max_multiplier = -0.50
        elif self.damage_type == DamageEnum.DIVINE:
            min_multiplier = 0.77
            max_multiplier = 1.54
        elif self.damage_type == DamageEnum.LIGHT:
            min_multiplier = 0.50
            max_multiplier = 0.99
        elif self.damage_type == DamageEnum.DARK:
            min_multiplier = 0.42
            max_multiplier = 0.84
        elif self.damage_type == DamageEnum.FIRE:
            min_multiplier = 0.18
            max_multiplier = 1.00
        elif self.damage_type == DamageEnum.WATER:
            min_multiplier = 0.23
            max_multiplier = 0.46
        elif self.damage_type == DamageEnum.COLD:
            min_multiplier = 0.16
            max_multiplier = 0.33
        elif self.damage_type == DamageEnum.LIGHTNING:
            min_multiplier = 0.37
            max_multiplier = 0.74
        elif self.damage_type == DamageEnum.WIND:
            min_multiplier = 0.22
            max_multiplier = 0.41
        elif self.damage_type == DamageEnum.ROCK:
            min_multiplier = 0.25
            max_multiplier = 0.50
        elif self.damage_type == DamageEnum.GROUND:
            min_multiplier = 0.09
            max_multiplier = 0.65
        elif self.damage_type == DamageEnum.ACID:
            min_multiplier = 0.32
            max_multiplier = 0.64
        elif self.damage_type == DamageEnum.POISON:
            min_multiplier = 0.36
            max_multiplier = 0.71
        elif self.damage_type == DamageEnum.CHAOS:
            min_multiplier = 0.06
            max_multiplier = 1.32

        return min_multiplier, max_multiplier

    @property
    def condition_list(self) -> List[dict]:
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

    status = status_list = condition_list
    text = damage_text

    def __str__(self):
        return self.damage_text

    def __repr__(self):
        return f'<{self.damage_text}>'


if __name__ == '__main__':
    spec_dmg = SpecialDamage(1, DamageEnum.HITTING)
    print(spec_dmg)
