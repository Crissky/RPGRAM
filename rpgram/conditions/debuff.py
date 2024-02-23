from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.enums.debuff import (
    BERSERKER,
    BLEEDING,
    BLINDNESS,
    BURN,
    CONFUSION,
    CURSE,
    EXHAUSTION,
    FROZEN,
    PARALYSIS,
    PETRIFIED,
    POISONING,
    SILENCE,
    STUNNED,
)
from rpgram.enums.debuff import IMMOBILIZED_DEBUFFS_NAMES
from rpgram.enums.turn import TurnEnum


class DebuffCondition(Condition):

    def __init__(
        self,
        name: str,
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


class BerserkerCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=BERSERKER,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'O personagem fica enlouquecido ({BERSERKER}) por 5 turnos, '
            f'Aumentando o multiplicador de Força em '
            f'"{self.multiplier_strength:.2f}x" (10% x Nível), mas '
            f'podendo atacar aliados ou a si.'
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 10
        return (1 + power)

    def function(self, target) -> dict:
        report = {}
        report['text'] = f'Personagem está enlouquecido ({BERSERKER}).'
        report['action'] = f'{BERSERKER}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class BleedingCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BLEEDING,
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def power(self):
        return self.level * 0.02

    @property
    def description(self) -> str:
        return (
            f'Causa {self.power * 100}% do HP (2% x Nível) '
            f'como dano a cada turno.'
        )

    def function(self, target) -> dict:
        power = self.power
        damage = target.combat_stats.hp * power
        report = target.combat_stats.damage_hit_points(damage)
        report['text'] = f'{self.full_name} -> ' + report['text']
        report['action'] = f'{self.name}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class BlindnessCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BLINDNESS,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            'Reduz o multiplicador de Destreza em '
            f'"{self.multiplier_dexterity - 1:.2f}x" (10% x Nível).'
        )

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 10
        return (1 - power)

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está cego.'
        report['action'] = f'{BLINDNESS}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class BurnCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BURN,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Reduz o multiplicador de Constituição em '
            f'"{self.multiplier_constitution - 1:.2f}x" (10% x Nível).'
        )

    @property
    def multiplier_constitution(self) -> float:
        power = self.level / 10
        return (1 - power)

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está com queimaduras.'
        report['action'] = f'{BURN}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class ConfusionCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=CONFUSION,
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

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está confuso.'
        report['action'] = f'{CONFUSION}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class CurseCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=CURSE,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Reduz os multiplicadores de Inteligência e Sabedoria em '
            f'"{self.multiplier_intelligence - 1:.2f}x" e '
            f'"{self.multiplier_wisdom - 1:.2f}x" (10% x Nível).'
        )

    @property
    def multiplier_intelligence(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def multiplier_wisdom(self) -> float:
        power = self.level / 10
        return (1 - power)

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está amaldiçoado.'
        report['action'] = f'{CURSE}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class ExhaustionCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=EXHAUSTION,
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
            f'(10% x Nível).'
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 10
        return (1 - power)

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está exausto.'
        report['action'] = f'{EXHAUSTION}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class FrozenCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=FROZEN,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está congelado.'
        report['action'] = f'{FROZEN}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class ParalysisCondition(DebuffCondition):

    def __init__(self, turn: int = 3, level: int = 1):
        super().__init__(
            name=PARALYSIS,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turnos.'

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está paralisado.'
        report['action'] = f'{PARALYSIS}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class PetrifiedCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=PETRIFIED,
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return 'O personagem não pode realizar ações.'

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está petrificado.'
        report['action'] = f'{PETRIFIED}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class PoisoningCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=POISONING,
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

    def function(self, target) -> dict:
        report = target.combat_stats.damage_hit_points(self.damage)
        report['text'] = f'{self.full_name} -> ' + report['text']
        report['action'] = f'{self.name}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class SilenceCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=SILENCE,
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def description(self) -> str:
        return 'O personagem não pode usar feitiços, magias ou encantamentos.'

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está silenciado.'
        report['action'] = f'{SILENCE}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class StunnedCondition(DebuffCondition):

    def __init__(self, turn: int = 1, level: int = 1):
        super().__init__(
            name=STUNNED,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return f'O personagem não pode realizar ações por {self.turn} turno.'

    def function(self, target) -> dict:
        report = {}
        report['text'] = 'Personagem está atordoado.'
        report['action'] = f'{STUNNED}'

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)


class Debuffs:
    __list = [
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
        StunnedCondition,
    ]

    def __iter__(self):
        for condition_class in self.__list:
            yield condition_class()


DEBUFFS = Debuffs()
if __name__ == '__main__':
    print(BerserkerCondition())
    print(BleedingCondition())
    print(BlindnessCondition())
    print(BurnCondition())
    print(ConfusionCondition())
    print(CurseCondition())
    print(ExhaustionCondition())
    print(FrozenCondition())
    print(ParalysisCondition())
    print(PetrifiedCondition())
    print(PoisoningCondition())
    print(SilenceCondition())
    print(StunnedCondition() in IMMOBILIZED_DEBUFFS_NAMES)
    print('BerserkerCondition(level=10).multiplier_strength:',
          BerserkerCondition(level=10).multiplier_strength)
