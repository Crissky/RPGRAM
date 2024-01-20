'''
Este módulo representa as condições positivas e negativas dos personagens.
'''

from abc import abstractmethod
from datetime import datetime
from typing import Union

from bson import ObjectId

from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.stats_booster import StatsBooster
from rpgram.enums.consumable import HealingConsumableEmojiEnum
from rpgram.enums.debuff import DebuffEmojiEnum
from rpgram.enums.turn import TurnEnum


class Condition(StatsBooster):
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

        self.__name = name
        self.__description = description
        self.__frequency = frequency
        self.__turn = turn
        self.__level = level

    def activate(self, target) -> dict:
        report = self.function(target)
        if self.__turn not in [-1, 0]:
            self.__turn -= 1

        return report

    def battle_activate(self, target) -> dict:
        report = self.battle_function(target)
        if self.__turn not in [-1, 0]:
            self.__turn -= 1

        return report

    def __call__(self, target) -> dict:
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
        text = f'*Condição*: {self.__name}\n'

        if verbose:
            text += (
                f'*Descrição*: {self.__description}\n'
                f'*Frequência*: {self.__frequency.value}\n'
                f'*Turno*: {self.__turn}\n'
                f'*Nível*: {self.__level}\n'
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
                self.__class__ == other.__class__,
                self.name == other.name
            ))
        elif isinstance(other, str):
            return self.name.upper() == other.upper()
        return False

    # Getters
    name = property(lambda self: self.__name)
    full_name = property(lambda self: f'{self.emoji}{self.name}{self.level}')
    description = property(lambda self: self.__description)
    frequency = property(lambda self: self.__frequency)
    turn = property(lambda self: self.__turn)
    level = property(lambda self: self.__level)

    @abstractmethod
    def function(self, target) -> dict:
        ...

    @abstractmethod
    def battle_function(self, target) -> dict:
        ...

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
    poison = Condition(
        name='Veneno',
        description='Causa 10 de dano por hora.',
        frequency='START',
    )

    # print('POISON\n', poison)
    print('POISON DICT\n', poison.to_dict())
