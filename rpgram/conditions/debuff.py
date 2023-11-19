from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.enums.condition import (
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
)
from rpgram.enums.turn import TurnEnum


class DebuffCondition(Condition):
    def __init__(
        self,
        name: str,
        description: str,
        frequency: Union[str, TurnEnum],
        turn: int = 1,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=description,
            function=None,
            battle_function=None,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            frequency=super_dict['frequency'],
            turn=super_dict['turn'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


class BleedingCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level * 0.02;'
            'damage = target.combat_stats.hp * power;'
            'report = target.combat_stats.damage_hit_points(damage);'
            f'report["text"] = "{BLEEDING} -> " + report["text"];'
            f'report["action"] = "{BLEEDING}";'
        )


class BlindnessCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level / 10;'
            'self.multiplier_dexterity = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está cego.";'
            f'report["action"] = "{BLINDNESS}";'
        )


class BurnCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level / 10;'
            'self.multiplier_constitution = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está com queimaduras.";'
            f'report["action"] = "{BURN}";'
        )


class ConfusionCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está confuso.";'
            f'report["action"] = "{CONFUSION}";'
        )


class CurseCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level / 10;'
            'self.multiplier_intelligence = 1 - power;'
            'self.multiplier_wisdom = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está amaldiçoado.";'
            f'report["action"] = "{CURSE}";'
        )


class ExhaustionCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level / 10;'
            'self.multiplier_strength = 1 - power;'
            'self.multiplier_dexterity = 1 - power;'
            'report = {};'
            'report["text"] = "Personagem está exausto.";'
            f'report["action"] = "{EXHAUSTION}";'
        )


class FrozenCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está congelado.";'
            f'report["action"] = "{FROZEN}";'
        )


class ParalysisCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está paralisado.";'
            f'report["action"] = "{PARALYSIS}";'
        )


class PetrifiedCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está petrificado.";'
            f'report["action"] = "{PETRIFIED}";'
        )


class PoisoningCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'power = self.level;'
            'damage = sum([10 + i + i*10//2 for i in range(0, power)]);'
            'report = target.combat_stats.damage_hit_points(damage);'
            f'report["text"] = "{POISONING} -> " + report["text"];'
            f'report["action"] = "{POISONING}";'
        )


class SilenceCondition(DebuffCondition):

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está silenciado.";'
            f'report["action"] = "{SILENCE}";'
        )


if __name__ == '__main__':
    print(BleedingCondition(
        name='BleedingCodition',
        description='BleedingCodition Description',
        frequency=TurnEnum.START
    ))
    print(BlindnessCondition(
        name='BlindnessCodition',
        description='BlindnessCodition Description',
        frequency=TurnEnum.START
    ))
    print(BurnCondition(
        name='BurnCodition',
        description='BurnCodition Description',
        frequency=TurnEnum.START
    ))
    print(ConfusionCondition(
        name='ConfusionCodition',
        description='ConfusionCodition Description',
        frequency=TurnEnum.START
    ))
    print(CurseCondition(
        name='CurseCodition',
        description='CurseCodition Description',
        frequency=TurnEnum.START
    ))
    print(ExhaustionCondition(
        name='ExhaustionCodition',
        description='ExhaustionCodition Description',
        frequency=TurnEnum.START
    ))
    print(FrozenCondition(
        name='FrozenCodition',
        description='FrozenCodition Description',
        frequency=TurnEnum.START
    ))
    print(ParalysisCondition(
        name='ParalysisCodition',
        description='ParalysisCodition Description',
        frequency=TurnEnum.START
    ))
    print(PetrifiedCondition(
        name='PetrifiedCodition',
        description='PetrifiedCodition Description',
        frequency=TurnEnum.START
    ))
    print(PoisoningCondition(
        name='PoisoningCodition',
        description='PoisoningCodition Description',
        frequency=TurnEnum.START
    ))
    print(SilenceCondition(
        name='SilenceCodition',
        description='SilenceCodition Description',
        frequency=TurnEnum.START
    ))
