''' Módulo com as Condições do tipo de Target diferente de SELF
    Essas Condições usam o power fornecido no momendo da instância
'''


from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Union

from bson import ObjectId
from rpgram.conditions.buff import BuffCondition
from rpgram.constants.text import (
    MAGICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT
)
from rpgram.enums.skill import WarriorSkillEnum
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class TargetSkillBuffCondition(BuffCondition):

    def __init__(
        self,
        name: Enum,
        frequency: Union[str, TurnEnum],
        power: int,
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
        self._power = int(power)

    @property
    def power(self) -> int:
        power_multiplier = 1 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self._power * power_multiplier)

    def to_dict(self) -> dict:
        _dict = {'power': self._power}
        _dict.update(super().to_dict())

        return _dict


class WarBannerCondition(TargetSkillBuffCondition):

    def __init__(
        self,
        power: int,
        turn: int = 10,
        level: int = 1,
    ):
        super().__init__(
            name=WarriorSkillEnum.WAR_BANNER,
            frequency=TurnEnum.START,
            power=power,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'*Marca do Senhor da Guerra* que aumenta o '
            f'*{PHYSICAL_ATTACK_EMOJI_TEXT}*, '
            f'*{PRECISION_ATTACK_EMOJI_TEXT}* e '
            f'*{MAGICAL_ATTACK_EMOJI_TEXT}* em {self.power} pontos.'
        )

    @property
    def bonus_physical_attack(self) -> int:
        return self.power

    @property
    def bonus_precision_attack(self) -> int:
        return self.power

    @property
    def bonus_magical_attack(self) -> int:
        return self.power

    @property
    def emoji(self) -> str:
        return '🚩'

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': '', 'action': self.name}
        if self.turn != 1:
            text = (
                f'*{self.full_name}*: '
                f'*{target.name}* permanece com a *Marca do Senhor da Guerra*.'
            )
            report['text'] = text

        return report


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory

    condition = WarBannerCondition(100)
    print(condition)
    print(condition.to_dict())
    assert condition_factory(**condition.to_dict()) == condition
