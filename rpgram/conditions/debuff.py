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
            description=(
                f'O personagem fica enlouquecido ({BERSERKER}) por 5 turnos, '
                f'Aumentando o multiplicador de Força em (10% x Nível), mas '
                f'podendo atacar aliados ou a si.'
            ),
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 10
        return (1 + power)

    @property
    def function(self) -> str:
        return (
            'report = {};'
            f'report["text"] = "Personagem está enlouquecido ({BERSERKER}).";'
            f'report["action"] = "{BERSERKER}";'
        )


class BleedingCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BLEEDING,
            description='Causa (2% x Nível) de dano a cada turno.',
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'power = self.level * 0.02;'
            'damage = target.combat_stats.hp * power;'
            'report = target.combat_stats.damage_hit_points(damage);'
            'report["text"] = f"{self.full_name} -> " + report["text"];'
            'report["action"] = f"{self.name}";'
        )


class BlindnessCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BLINDNESS,
            description='Reduz o multiplicador de Destreza em (10% x Nível).',
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está cego.";'
            f'report["action"] = "{BLINDNESS}";'
        )


class BurnCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=BURN,
            description=(
                'Reduz o multiplicador de Constituição em (10% x Nível).'
            ),
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def multiplier_constitution(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está com queimaduras.";'
            f'report["action"] = "{BURN}";'
        )


class ConfusionCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=CONFUSION,
            description=(
                'O personagem fica confuso por 5 turnos, '
                'podendo atacar aliados ou a si.'
            ),
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está confuso.";'
            f'report["action"] = "{CONFUSION}";'
        )


class CurseCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=CURSE,
            description=(
                'Reduz os multiplicadores de Inteligência e Sabedoria '
                'em (10% x Nível).'
            ),
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def multiplier_intelligence(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def multiplier_wisdom(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está amaldiçoado.";'
            f'report["action"] = "{CURSE}";'
        )


class ExhaustionCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=EXHAUSTION,
            description=(
                'Reduz os multiplicadores de '
                'Força e Destreza em (10% x Nível).'
            ),
            frequency=TurnEnum.CONTINUOUS,
            turn=-1,
            level=level,
        )

    @property
    def multiplier_strength(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def multiplier_dexterity(self) -> float:
        power = self.level / 10
        return (1 - power)

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está exausto.";'
            f'report["action"] = "{EXHAUSTION}";'
        )


class FrozenCondition(DebuffCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=FROZEN,
            description='O personagem não pode realizar ações por 5 turnos.',
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está congelado.";'
            f'report["action"] = "{FROZEN}";'
        )


class ParalysisCondition(DebuffCondition):

    def __init__(self, turn: int = 3, level: int = 1):
        super().__init__(
            name=PARALYSIS,
            description='O personagem não pode realizar ações por 3 turnos.',
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está paralisado.";'
            f'report["action"] = "{PARALYSIS}";'
        )


class PetrifiedCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=PETRIFIED,
            description='O personagem não pode realizar ações.',
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está petrificado.";'
            f'report["action"] = "{PETRIFIED}";'
        )


class PoisoningCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=POISONING,
            description='O personagem perde vida a cada turno.',
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'power = self.level;'
            'damage = sum([10 + i + i*10//2 for i in range(0, power)]);'
            'report = target.combat_stats.damage_hit_points(damage);'
            'report["text"] = f"{self.full_name} -> " + report["text"];'
            'report["action"] = f"{self.name}";'
        )


class SilenceCondition(DebuffCondition):

    def __init__(self, turn: int = -1, level: int = 1):
        super().__init__(
            name=SILENCE,
            description=(
                'O personagem não pode usar feitiços, magias ou encantamentos.'
            ),
            frequency=TurnEnum.START,
            turn=-1,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está silenciado.";'
            f'report["action"] = "{SILENCE}";'
        )


class StunnedCondition(DebuffCondition):

    def __init__(self, turn: int = 1, level: int = 1):
        super().__init__(
            name=STUNNED,
            description='O personagem não pode realizar ações por 1 turno.',
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def function(self) -> str:
        return (
            'report = {};'
            'report["text"] = "Personagem está atordoado.";'
            f'report["action"] = "{STUNNED}";'
        )


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
