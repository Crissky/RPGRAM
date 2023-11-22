from bson import ObjectId
from datetime import datetime
from typing import List, Union

from constant.text import SECTION_HEAD
from function.datetime import datetime_to_string


class Player:
    def __init__(
        self,
        name: str,
        player_id: int,
        chat_ids: List[int] = [],
        _id: Union[str, ObjectId] = None,
        verbose: bool = False,
        silent: bool = False,
        xp_cooldown: datetime = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.name = name
        self.player_id = player_id
        self.chat_ids = chat_ids
        self.__id = _id
        self.verbose = verbose
        self.silent = silent
        self.xp_cooldown = xp_cooldown
        self.created_at = created_at
        self.updated_at = updated_at

    def add_chat_id(self, chat_id):
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)
        else:
            raise ValueError(f'O chat ID {chat_id} já está na lista.')

    # Getters
    _id = property(lambda self: self.__id)

    def __setitem__(self, key, value):
        key = key.upper()

        if key in ['VERBOSE']:
            value = value.upper()
            if value in ['FALSE', 'NO', '0']:
                value = False
            elif value in ['TRUE', 'YES', '1']:
                value = True
            else:
                raise ValueError(f'Forneça o valor "True" ou "False"')
            self.verbose = value
        elif key in ['SILENT', 'SILENCIOSO']:
            value = value.upper()
            if value in ['FALSE', 'NO', '0']:
                value = False
            elif value in ['TRUE', 'YES', '1']:
                value = True
            else:
                raise ValueError(f'Forneça o valor "True" ou "False"')
            self.silent = value
        else:
            raise KeyError(f'"{key}" não é uma chave válida.')

    def __repr__(self) -> str:
        return (
            f'{SECTION_HEAD.format("Dados do Jogador")}\n\n'
            f'Jogador: {self.name}\n'
            f'ID: {self.__id}\n'
            f'Verbose: {self.verbose}\n'
            f'Silencioso: {self.silent}\n'
            f'Player ID: {self.player_id}\n'
            f'Criado em: {datetime_to_string(self.created_at)}\n'
            f'Atualizado em: {datetime_to_string(self.updated_at)}'
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            player_id=self.player_id,
            chat_ids=self.chat_ids,
            _id=self.__id,
            verbose=self.verbose,
            silent=self.silent,
            xp_cooldown=self.xp_cooldown,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


if __name__ == '__main__':
    player = Player(
        name='Aroldo',
        player_id=2,
        _id='ffffffffffffffffffffffff'
    )
    print('__repr__:\n', player)
    print('to_dict:', player.to_dict())
