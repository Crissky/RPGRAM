'''
Este módulo representa as condições positivas e negativas dos personagens.
'''

from datetime import datetime
from typing import Union

from bson import ObjectId

from constant.text import TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.stats_booster import StatsBooster
from rpgram.enums.turn import TurnEnum


class Condition(StatsBooster):
    def __init__(
        self,
        name: str,
        description: str,
        function: str,
        battle_function: str,
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
        self.__function = function
        self.__battle_function = battle_function
        self.__frequency = frequency
        self.__turn = turn
        self.__level = level

        self.activate_continuous()

    def activate_continuous(self):
        if self.__frequency == TurnEnum.CONTINUOUS:
            self.activate(None)

    def activate(self, target):
        local = {'target': target, 'self': self}
        exec(self.function, None, local)
        report = local['report']
        if self.__turn not in [-1, 0]:
            self.__turn -= 1
        return report

    def battle_activate(self, target):
        if self.battle_function:
            local = {'target': target, 'self': self}
            exec(self.battle_function, None, local)
            report = local['report']
            if self.__turn not in [-1, 0]:
                self.__turn -= 1
        else:
            self.activate(target)
        return report

    def __call__(self, target):
        return self.activate(target)

    def add_level(self):
        self.__level += 1

        return self

    def remove_level(self):
        self.__level -= 1
        if self.__level < 1:
            return None
        return self

    def set_turn(self, turn: int):
        if turn == 0 or turn < -1:
            raise ValueError('turn deve ser maior que zero ou -1.')
        self.__turn = turn

    def last_turn(self):
        self.__turn = 1

    def to_dict(self):
        return dict(
            name=self.__name,
            description=self.__description,
            function=self.function,
            battle_function=self.battle_function,
            frequency=self.__frequency.name,
            turn=self.__turn,
            _id=self._id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Condição*: {self.__name}\n'

        if verbose:
            text += (
                f'*Descrição*: {self.__description}\n'
                f'*Função*: {self.function}\n'
                f'*Função em Batalha*: {self.battle_function}\n'
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
            if self._id is not None and other._id is not None:
                return self._id == other._id
        elif isinstance(other, str):
            return self.name.upper() == other.upper()
        return False

    # Getters
    name = property(lambda self: self.__name)
    full_name = property(lambda self: f'{self.name}{self.level}')
    description = property(lambda self: self.__description)
    function = property(lambda self: self.__function)
    battle_function = property(lambda self: self.__battle_function)
    frequency = property(lambda self: self.__frequency)
    turn = property(lambda self: self.__turn)
    level = property(lambda self: self.__level)


if __name__ == '__main__':
    poison = Condition(
        name='Veneno',
        description='Causa 10 de dano por hora.',
        function='target.cs.damage_hit_points(10)',
        battle_function='target.cs.damage_hit_points(10)',
        frequency='START',
    )

    print(poison)
    print(poison.to_dict())