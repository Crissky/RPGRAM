from bson import ObjectId
from datetime import datetime
from typing import List, Union

from constant.text import SECTION_HEAD
from function.date_time import datetime_to_string
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.trocado import TrocadoEnum


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
        trocado: int = 0,
        current_action_points: int = 0,
        max_action_points: int = 3,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        self.__chat_ids = []
        if isinstance(_id, str):
            _id = ObjectId(_id)
        if isinstance(chat_ids, int):
            chat_ids = [int(chat_ids)]

        for chat_id in chat_ids:
            self.add_chat_id(chat_id)

        self.name = name
        self.player_id = player_id
        self.__id = _id
        self.verbose = verbose
        self.silent = silent
        self.xp_cooldown = xp_cooldown
        self.__trocado = trocado
        self.__current_action_points = current_action_points
        self.__max_action_points = max_action_points
        self.created_at = created_at
        self.updated_at = updated_at

    def add_chat_id(self, chat_id):
        if chat_id not in self.__chat_ids:
            self.__chat_ids.append(chat_id)
        else:
            raise ValueError(f'O chat ID {chat_id} já está na lista.')

    def add_trocado(self, value: int) -> dict:
        value = int(value)
        if value <= 0:
            raise ValueError(
                f'O valor "{value}" não pode ser menor ou igual a zero.'
            )

        self.__trocado += value
        report = {
            'value': value,
            'total': self.__trocado,
            'text': (
                f'Você faturou {value}{EmojiEnum.TROCADO.value} e agora está '
                f'com {self.__trocado}{EmojiEnum.TROCADO.value}.'
            ),
        }

        return report

    def sub_trocado(self, value: int) -> dict:
        value = int(value)
        if value <= 0:
            raise ValueError(
                f'O valor "{value}" não pode ser menor ou igual a zero.'
            )
        if value > self.__trocado:
            raise ValueError(
                f'O valor "{value}" para subtrair é maior que o valor total '
                f'({self.__trocado}) de trocados que o jogador {self.name} '
                f'possui.'
            )

        sub_total = self.__trocado - value
        self.__trocado = max(sub_total, 0)
        report = {
            'value': value,
            'total': self.__trocado,
            'text': (
                f'Você perdeu {value}{EmojiEnum.TROCADO.value} e agora está '
                f'com {self.__trocado}{EmojiEnum.TROCADO.value}.'
            ),
        }

        return report

    def add_action_points(self, value: int = 1) -> dict:
        value = abs(value)
        if value <= 0:
            raise ValueError(
                f'O valor "{value}" não pode ser menor ou igual a zero.'
            )

        current_value = self.__max_action_points - self.__current_action_points
        current_value = min(current_value, value)
        self.__current_action_points += current_value
        self.__current_action_points = min(
            self.__current_action_points, self.__max_action_points
        )
        report = {
            'value': value,
            'current_value': current_value,
            'text': (
                f'Adicionado(s) {current_value} ponto(s) de ação.\n'
                f'{self.current_action_points_text}'
            )
        }

        return report

    def sub_action_points(self, value: int = 1) -> dict:
        value = abs(value)
        if value <= 0:
            raise ValueError(
                f'O valor "{value}" não pode ser menor ou igual a zero.'
            )

        current_value = self.__current_action_points - value
        current_value = max(current_value, 0)
        self.__current_action_points = current_value
        report = {
            'value': value,
            'current_value': current_value,
            'text': (
                f'Removido(s) {value} ponto(s) de ação.\n'
                f'{self.current_action_points_text}'
            )
        }

        return report

    # Getters
    _id = property(lambda self: self.__id)
    trocado = property(lambda self: self.__trocado)

    @property
    def trocado_text(self) -> str:
        return f'{self.__trocado}{EmojiEnum.TROCADO.value}'

    @property
    def current_action_points_text(self) -> str:
        return (
            f'Pontos de Ação: '
            f'{self.__current_action_points}/{self.__max_action_points}'
        )

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
            f'{TrocadoEnum.TROCADO.value}: {self.trocado_text}\n'
            f'ID: {self.__id}\n'
            f'Player ID: {self.player_id}\n'
            f'Verbose: {self.verbose}\n'
            f'Silencioso: {self.silent}\n'
            f'{self.current_action_points_text}\n'
            f'Criado em: {datetime_to_string(self.created_at)}\n'
            f'Atualizado em: {datetime_to_string(self.updated_at)}'
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            player_id=self.player_id,
            chat_ids=self.__chat_ids,
            _id=self.__id,
            verbose=self.verbose,
            silent=self.silent,
            xp_cooldown=self.xp_cooldown,
            trocado=self.__trocado,
            current_action_points=self.__current_action_points,
            max_action_points=self.__max_action_points,
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
