from datetime import datetime
from typing import Union

from bson import ObjectId
from constant.text import TEXT_DELIMITER

from function.text import escape_basic_markdown_v2, remove_bold, remove_code


class Condition:
    def __init__(
        self,
        name: str,
        description: str,
        function: str,
        battle_function: str,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__name = name
        self.__description = description
        self.__function = function
        self.__battle_function = battle_function
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

    def activate(self, target):
        result = exec(self.__function)
        return result

    def battle_activate(self, target):
        result = exec(self.__battle_function)
        return result

    def to_dict(self):
        return dict(
            name=self.__name,
            description=self.__description,
            function=self.__function,
            battle_function=self.__battle_function,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def __call__(self, target):
        return self.activate(target)

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = f'*Condição*: {self.__name}\n'

        if verbose:
            text += (
                f'*Descrição*: {self.__description}\n'
                f'*Função*: {self.__function}\n'
                f'*Função em Batalha*: {self.__battle_function}\n'
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
            return self._id == other._id
        return False

    # Getters
    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)
    function = property(lambda self: self.__function)
    battle_function = property(lambda self: self.__battle_function)
    _id = property(lambda self: self.__id)


if __name__ == '__main__':
    poison = Condition(
        name='Veneno',
        description='Causa 10 de dano por hora.',
        function='target.cs.hp = -10',
        battle_function='target.cs.hp = -10',
    )

    print(poison)
