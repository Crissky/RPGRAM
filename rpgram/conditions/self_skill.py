from datetime import datetime
from typing import TYPE_CHECKING, Union

from bson import ObjectId

from rpgram.conditions.condition import Condition
from rpgram.constants.text import PHYSICAL_DEFENSE_FULL
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.turn import TurnEnum


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class SelfSkillCondition(Condition):

    def __init__(
        self,
        name: str,
        character: 'BaseCharacter',
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
        self.character = character


class RobustBlockCondition(SelfSkillCondition):

    def __init__(
        self,
        character: 'BaseCharacter',
        turn: int = 5,
        level: int = 1
    ):
        super().__init__(
            name='Bloqueio Robusto',
            character=character,
            frequency=TurnEnum.START,
            turn=turn,
            level=level,
        )

    @property
    def description(self) -> str:
        return (
            f'Postura defensiva que aumenta a {PHYSICAL_DEFENSE_FULL} '
            f'em {self.bonus_physical_defense} pontos '
            f'(5%{EmojiEnum.CONSTITUTION.value} x Nível) '
            f'por 5 turnos.'
        )

    @property
    def bonus_physical_defense(self) -> int:
        power = 1 + (self.level / 20)
        bonus_physical_defense = self.character.bs.constitution * power

        return int(bonus_physical_defense)

    def function(self, target: 'BaseCharacter') -> dict:
        report = {'text': ''}
        report['action'] = self.name

        return report

    def battle_function(self, target: 'BaseCharacter') -> dict:
        return self.function(target)

if __name__ == '__main__':
    from rpgram.constants.test import BASE_CHARACTER
    rbc = RobustBlockCondition(BASE_CHARACTER)
    print(rbc)
