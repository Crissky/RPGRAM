from datetime import datetime
from enum import Enum
from bson import ObjectId
from typing import TYPE_CHECKING, Iterable, Union

from rpgram.conditions.condition import Condition
from rpgram.enums.debuff import (
    DebuffEnum,
)
from rpgram.enums.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class DebuffCondition(Condition):

    def __init__(
        self,
        name: Enum,
        frequency: Union[str, TurnEnum],
        turn: int = 1,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            report['text'] = (
                f'{self.full_name}: Personagem está {self.trans_name}.'
            )

        return report


class BerserkerCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=DebuffEnum.BERSERKER,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'O personagem fica enlouquecido ({self.name}) por '
            f'{self.turn} turnos, aumentando o multiplicador de Força em '
            f'"{self.multiplier_strength:.2f}x" (5% x Nível), mas '
            f'pode atacar aliados ou a si.'
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 20
        return round(1 + power, 2)


class BleedingCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.BLEEDING,
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )
        self.__power_constant = 0.0020

    @property
    def power(self):
        power = self.level * self.__power_constant
        power = min(power, 0.50)

        return power

    @property
    def description(self) -> str:
        return (
            f'Causa {(self.power * 100):.2f}% do HP '
            f'({self.__power_constant * 100:.2f}% x Nível) '
            f'como dano a cada turno.'
        )

    def function(self, target: 'BaseCharacter') -> dict:
        power = self.power
        damage = target.combat_stats.hp * power
        report = target.combat_stats.damage_hit_points(
            value=damage,
            ignore_barrier=True,
        )

        report['text'] = f'{self.full_name}: ' + report['text']
        report['action'] = f'{self.name}'

        return report


class BlindnessCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.BLINDNESS,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            'Reduz o multiplicador de Destreza em '
            f'"{self.multiplier_dexterity - 1:.2f}x" (5% x Nível).'
        )

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)


class BurnCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.BURN,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Reduz o multiplicador de Constituição em '
            f'"{self.multiplier_constitution - 1:.2f}x" (5% x Nível).'
        )

    @property
    def multiplier_constitution(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)


class ConfusionCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=DebuffEnum.CONFUSION,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'O personagem fica confuso por {self.turn} turno(s), '
            f'podendo atacar aliados ou a si.'
        )


class CrystallizedCondition(DebuffCondition):

    def __init__(self, turn: int = 7, level: int = 1):
        super().__init__(
            name=DebuffEnum.CRYSTALLIZED,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'


class CurseCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.CURSE,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Reduz os multiplicadores de Inteligência e Sabedoria em '
            f'"{self.multiplier_intelligence - 1:.2f}x" e '
            f'"{self.multiplier_wisdom - 1:.2f}x" (5% x Nível).'
        )

    @property
    def multiplier_intelligence(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)

    @property
    def multiplier_wisdom(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)


class ExhaustionCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.EXHAUSTION,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Reduz os multiplicadores de Força e Destreza em '
            f'"{self.multiplier_strength - 1:.2f}x" e '
            f'"{self.multiplier_dexterity - 1:.2f}x" '
            f'(5% x Nível).'
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)


class FearingCondition(DebuffCondition):

    def __init__(self, turn: int = 2, level: int = 1):
        super().__init__(
            name=DebuffEnum.FEARING,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'O personagem não pode realizar ações por {self.turn} turnos '
            f'e tem seu multiplicador de Constituição reduzido em '
            f'"{self.multiplier_constitution - 1:.2f}x" e de Sabedoria em '
            f'"{self.multiplier_wisdom - 1:.2f}x" (5% x Nível).'
        )

    @property
    def multiplier_constitution(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)

    @property
    def multiplier_wisdom(self) -> float:
        power = self.level / 20
        return round(1 - power, 2)


class FrozenCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=DebuffEnum.FROZEN,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'


class ImprisonedCondition(DebuffCondition):

    def __init__(self, turn: int = 2, level: int = 1):
        super().__init__(
            name=DebuffEnum.IMPRISONED,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'


class ParalysisCondition(DebuffCondition):

    def __init__(self, turn: int = 3, level: int = 1):
        super().__init__(
            name=DebuffEnum.PARALYSIS,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'


class PetrifiedCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.PETRIFIED,
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return 'O personagem não pode realizar ações.'


class PoisoningCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.POISONING,
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem perde {self.damage} pontos de vida a cada turno.'

    @property
    def damage(self):
        power = self.level
        damage = sum([10 + i + i*10//2 for i in range(0, power)])
        return damage

    def function(self, target: 'BaseCharacter') -> dict:
        damage = self.damage
        report = target.combat_stats.damage_hit_points(
            value=damage,
            ignore_barrier=True,
        )
        report['text'] = f'{self.full_name}: ' + report['text']
        report['action'] = f'{self.name}'

        return report


class SilenceCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=DebuffEnum.SILENCE,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return 'O personagem não pode usar feitiços, magias ou encantamentos.'


class StunnedCondition(DebuffCondition):

    def __init__(self, turn: int = 1, level: int = 1):
        super().__init__(
            name=DebuffEnum.STUNNED,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turno.'


class Debuffs:
    __list = [
        BerserkerCondition,
        BleedingCondition,
        BlindnessCondition,
        BurnCondition,
        ConfusionCondition,
        CrystallizedCondition,
        CurseCondition,
        ExhaustionCondition,
        FearingCondition,
        FrozenCondition,
        ImprisonedCondition,
        ParalysisCondition,
        PetrifiedCondition,
        PoisoningCondition,
        SilenceCondition,
        StunnedCondition,
    ]

    def __iter__(self) -> Iterable[DebuffCondition]:
        for condition_class in self.__list:
            yield condition_class()


DEBUFFS: Iterable[DebuffCondition] = Debuffs()


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory
    from rpgram.constants.test import BASE_CHARACTER

    for condition in Debuffs():
        print(condition)

    print(StunnedCondition() in IMMOBILIZED_DEBUFFS_NAMES)
    print('BerserkerCondition(level=10).multiplier_strength:',
          BerserkerCondition(level=10).multiplier_strength)

    for debuff in Debuffs():
        condition = debuff
        print(condition.to_dict())
        _dict = {**condition.to_dict()}
        assert condition_factory(**_dict) == condition

    for condition in Debuffs():
        print(condition.function(BASE_CHARACTER)['text'])
