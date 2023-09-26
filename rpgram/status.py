from datetime import datetime
from typing import List, Union

from bson import ObjectId
from constant.text import TEXT_SEPARATOR_2
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram import Condition


class Status:

    def __init__(
        self,
        player_id: int,
        conditions: List[Condition],
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__player_id = player_id
        self.__conditions = conditions
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = ''
        if not self.__conditions:
            text = 'Normal'
        elif verbose:
            text += f'{TEXT_SEPARATOR_2}\n'.join(
                f'*Nome*: {condition.name}\n'
                f'*Descrição*: {condition.description}\n'
                for condition in self.__conditions
            )
        else:
            text += '/'.join(
                condition.name
                for condition in self.__conditions
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
        return (
            'Status: ' +
            self.get_sheet(verbose=verbose, markdown=markdown)
        )

    # Getters
    conditions = property(lambda self: self.__conditions)
    _id = property(lambda self: self.__id)


if __name__ == '__main__':
    status = Status(
        player_id='1',
        conditions=[],
    )
    print(status.get_sheet())
    print(status.get_sheet(verbose=True))
    print(status.get_all_sheets())
    print(status.get_all_sheets(verbose=True))
    status = Status(
        player_id='1',
        conditions=[
            Condition(
                name='Poison',
                description='Veneno venenoso',
                function='Normal',
                battle_function='Normal',
            ),
            Condition(
                name='Burn',
                description='Tá pegando fogo',
                function='Normal',
                battle_function='Normal',
            ),
        ],
    )
    print(status.get_sheet())
    print(status.get_sheet(verbose=True))
    print(status.get_all_sheets())
    print(status.get_all_sheets(verbose=True))
