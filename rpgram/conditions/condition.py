'''
Este módulo representa as condições positivas e negativas dos personagens.
'''

from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Union

from bson import ObjectId

from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.stats_booster import StatsBooster
from rpgram.enums.consumable import HealingConsumableEmojiEnum
from rpgram.enums.debuff import DebuffEmojiEnum
from rpgram.enums.turn import TurnEnum

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


class Condition(StatsBooster):
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
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        if isinstance(frequency, str):
            frequency = TurnEnum[frequency]
        if not isinstance(frequency, TurnEnum):
            raise TypeError(
                f'frequency deve ser do tipo TurnEnum. '
                f'Tipo: {type(frequency)}.'
            )

        self.__enum_name: Enum = name
        self.__frequency = frequency
        self.__turn = turn
        self.__level = level

    @abstractmethod
    def function(self, target: 'BaseCharacter') -> dict:
        ...

    def activate(self, target: 'BaseCharacter') -> dict:
        report = self.function(target)
        report['condition_name'] = self.name
        if self.__turn not in [-1, 0]:
            self.__turn -= 1

        return report

    def __call__(self, target: 'BaseCharacter') -> dict:
        return self.activate(target)

    def add_level(self, value: int = 1):
        self.__level += abs(value)

        return self

    def remove_level(self, value: int = 1):
        self.__level -= abs(value)
        if self.__level < 1:
            return None
        return self

    def set_turn(self, turn: int):
        if turn == 0 or turn < -1:
            raise ValueError('turn deve ser maior que zero ou -1.')
        self.__turn = turn

    def last_turn(self):
        self.__turn = 1

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Condição*: {self.emoji_name}\n'

        if verbose:
            text += (
                f'*Descrição*: {self.description}\n'
                f'*Frequência*: {self.frequency.value}\n'
                f'*Turno*: {self.turn}\n'
                f'*Nível*: {self.level}\n'
            )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def __eq__(self, other):
        if isinstance(other, Condition):
            return all((
                self.__class__.__name__ == other.__class__.__name__,
                self.name == other.name
            ))
        elif isinstance(other, str):
            return any((
                self.name.upper() == other.upper(),
                self.__enum_name.name.upper() == other.upper(),
                self.__enum_name.value.upper() == other.upper(),
            ))
        elif isinstance(other, Enum):
            return self.__enum_name == other
        return False

    def __lt__(self, other):
        if isinstance(other, Condition):
            return self.name < other.name
        else:
            return self.name < other

    def __hash__(self) -> int:
        return hash(self.name)

    def to_dict(self) -> dict:
        return {
            'name': self.__enum_name.name,
            'turn': self.turn,
            'level': self.level,
        }

    # Getters
    enum_name: Enum = property(lambda self: self.__enum_name)
    emoji_name: str = property(lambda self: f'{self.emoji}{self.name}')
    full_name: str = property(lambda self: f'{self.emoji_name}{self.level}')
    frequency: TurnEnum = property(lambda self: self.__frequency)
    turn: int = property(lambda self: self.__turn)
    level: int = property(lambda self: self.__level)

    @property
    def true_name(self) -> str:
        return self.__enum_name.name
    
    @property
    def name(self) -> str:
        return self.true_name.replace('_', ' ').title().replace('ççç', "'")

    @property
    def description(self) -> str:
        return 'Descrição padrão.'

    @property
    def emoji_members_list(self) -> list:
        return [
            DebuffEmojiEnum.__members__,
            HealingConsumableEmojiEnum.__members__,
        ]

    @property
    def emoji(self) -> str:
        name_upper = self.name.upper()
        for emoji_members in self.emoji_members_list:
            if name_upper in emoji_members:
                return emoji_members[name_upper].value
        return ''


if __name__ == '__main__':
    from rpgram.enums.debuff import DebuffEnum

    poison = Condition(
        name=DebuffEnum.POISONING,
        frequency='START',
    )

    print('poison.name:', poison.name)
    print('poison.emoji_name:', poison.emoji_name)
    print('poison.full_name:', poison.full_name)
    print('POISON\n', poison)
    print('POISON DICT\n', poison.to_dict())
