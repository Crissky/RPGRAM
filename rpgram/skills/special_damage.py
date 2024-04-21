from random import randint
from typing import List, Tuple, Union

from rpgram.enums.damage import DamageEnum
from rpgram.enums.debuff import DebuffEnum


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
        return int(self.base_damage * self.__damage_multipliers[0])

    @property
    def max_damage(self) -> int:
        return int(self.base_damage * self.__damage_multipliers[1])

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
    def status_list(self) -> List[dict]:
        '''Retorna uma lista de status (Dict[status, ratio]) com o 
        percentual de chance (ratio) de causar o status.
        '''

        status_list = []
        if self.damage_type == DamageEnum.HITTING:
            status_list.extend([
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.SLASHING:
            status_list.extend([
                dict(status=DebuffEnum.BLEEDING, ratio=0.25),
            ])
        elif self.damage_type == DamageEnum.PIERCING:
            status_list.extend([
                dict(status=DebuffEnum.BLEEDING, ratio=0.10),
                dict(status=DebuffEnum.BLEEDING, ratio=0.10),
                dict(status=DebuffEnum.BLEEDING, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.MAGIC:
            status_list.extend([
                dict(status=DebuffEnum.BLINDNESS, ratio=0.05),
                dict(status=DebuffEnum.BURN, ratio=0.05),
                dict(status=DebuffEnum.CONFUSION, ratio=0.05),
                dict(status=DebuffEnum.EXHAUSTION, ratio=0.05),
                dict(status=DebuffEnum.FROZEN, ratio=0.05),
                dict(status=DebuffEnum.PARALYSIS, ratio=0.05),
                dict(status=DebuffEnum.PETRIFIED, ratio=0.05),
                dict(status=DebuffEnum.POISONING, ratio=0.05),
                dict(status=DebuffEnum.SILENCE, ratio=0.05),
                dict(status=DebuffEnum.STUNNED, ratio=0.05),
            ])
        elif self.damage_type == DamageEnum.BLESSING:
            status_list.extend([
                dict(status=DebuffEnum.SILENCE, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.DIVINE:
            status_list.extend([
                dict(status=DebuffEnum.BERSERKER, ratio=0.10),
                dict(status=DebuffEnum.BLEEDING, ratio=0.10),
                dict(status=DebuffEnum.BLINDNESS, ratio=0.10),
                dict(status=DebuffEnum.BURN, ratio=0.10),
                dict(status=DebuffEnum.CONFUSION, ratio=0.10),
                dict(status=DebuffEnum.CURSE, ratio=0.10),
                dict(status=DebuffEnum.EXHAUSTION, ratio=0.10),
                dict(status=DebuffEnum.FROZEN, ratio=0.10),
                dict(status=DebuffEnum.PARALYSIS, ratio=0.10),
                dict(status=DebuffEnum.PETRIFIED, ratio=0.10),
                dict(status=DebuffEnum.POISONING, ratio=0.10),
                dict(status=DebuffEnum.SILENCE, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.LIGHT:
            status_list.extend([
                dict(status=DebuffEnum.BLINDNESS, ratio=0.10),
                dict(status=DebuffEnum.CONFUSION, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.DARK:
            status_list.extend([
                dict(status=DebuffEnum.BLINDNESS, ratio=0.10),
                dict(status=DebuffEnum.CONFUSION, ratio=0.10),
                dict(status=DebuffEnum.CURSE, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.FIRE:
            status_list.extend([
                dict(status=DebuffEnum.BURN, ratio=0.10),
                dict(status=DebuffEnum.BURN, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.WATER:
            status_list.extend([
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.COLD:
            status_list.extend([
                dict(status=DebuffEnum.FROZEN, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.LIGHTNING:
            status_list.extend([
                dict(status=DebuffEnum.PARALYSIS, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.WIND:
            status_list.extend([
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
                dict(status=DebuffEnum.BLEEDING, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.ROCK:
            status_list.extend([
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.GROUND:
            status_list.extend([
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
                dict(status=DebuffEnum.STUNNED, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.ACID:
            status_list.extend([
                dict(status=DebuffEnum.BURN, ratio=0.10),
                dict(status=DebuffEnum.POISONING, ratio=0.10),
            ])
        elif self.damage_type == DamageEnum.POISON:
            status_list.extend([
                dict(status=DebuffEnum.POISONING, ratio=0.15),
                dict(status=DebuffEnum.POISONING, ratio=0.15),
            ])
        elif self.damage_type == DamageEnum.CHAOS:
            status_list.extend([
                dict(status=DebuffEnum.CURSE, ratio=0.10),
                dict(status=DebuffEnum.CURSE, ratio=0.10),
                dict(status=DebuffEnum.CURSE, ratio=0.10),
            ])

        return status_list * self.__status_multiplier

    status = status_list
    text = damage_text

    def __str__(self):
        return self.damage_text

    def __repr__(self):
        return f'<{self.damage_text}>'


if __name__ == '__main__':
    spec_dmg = SpecialDamage(10, 20, DamageEnum.HITTING)
    print(spec_dmg)
