from datetime import datetime
from typing import Union

from bson import ObjectId

from constant.text import SECTION_HEAD
from function.date_time import (
    datetime_to_string
)
from random import randint
from random import randint


MAX_NUM_PLAYERS = 3
MAX_EVENT_POINTS_MULTIPLIER = 100
MAX_EXTRA_EVENT_POINTS = 3.0


class Group:
    def __init__(
        self,
        name: str,
        chat_id: int,
        _id: Union[str, ObjectId] = None,
        verbose: bool = False,
        silent: bool = False,
        spawn_start_time: int = 6,
        spawn_end_time: int = 20,
        multiplier_xp: float = 1.0,
        # multiplicador do bônus de xp pelo nível do Personagem
        character_multiplier_xp: float = 1.0,
        group_level: int = 1,
        tier: dict = {},
        total_players: int = 1,
        current_event_points: int = 0,
        current_extra_event_points: float = 0.0,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.name = name
        self.chat_id = chat_id
        self.__id = _id
        self.verbose = verbose
        self.silent = silent
        self.spawn_start_time = spawn_start_time
        self.spawn_end_time = spawn_end_time
        self.multiplier_xp = float(multiplier_xp)
        self.character_multiplier_xp = float(character_multiplier_xp)
        self.tier = tier
        self.__total_players = total_players
        self.current_event_points = current_event_points
        self.current_extra_event_points = current_extra_event_points
        self.created_at = created_at
        self.updated_at = updated_at

    # Getters
    @property
    def group_level(self) -> int:
        group_level = 1
        if self.tier:
            group_level = sum(self.tier.values()) // len(self.tier)

        return group_level

    @property
    def total_players(self) -> int:
        return max(1, self.__total_players)

    @property
    def max_event_points(self) -> int:
        return self.total_players * MAX_EVENT_POINTS_MULTIPLIER

    @property
    def show_event_points(self) -> str:
        return (
            f'Pontos de Evento: '
            f'{self.current_event_points}/{self.max_event_points}'
        )

    @property
    def show_extra_event_points(self) -> str:
        return (
            f'Pontos de Evento Extra: '
            f'{self.current_extra_event_points}/{MAX_EXTRA_EVENT_POINTS}'
        )

    @property
    def can_trigger_event(self) -> bool:
        return self.current_event_points >= self.max_event_points

    @property
    def can_trigger_extra_event(self) -> bool:
        return self.current_extra_event_points >= 1.0

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
        elif key in ['SPAWN_START_TIME', 'START_TIME']:
            value = int(value)
            if value > 24 or value < 0:
                raise ValueError(f'Forneça um valor entre 0 e 24')
            self.spawn_start_time = value
        elif key in ['SPAWN_END_TIME', 'END_TIME']:
            value = int(value)
            if value > 24 or value < 0:
                raise ValueError(f'Forneça um valor entre 0 e 24')
            elif value < self.spawn_start_time:
                raise ValueError(
                    f'Forneça um valor maior que o start_time: '
                    f'"{self.spawn_start_time}".'
                )
            self.spawn_end_time = value
        elif key in ['MULTIPLIER_XP', 'XP']:
            value = float(value)
            if value < 0.0:
                raise ValueError(f'Forneça um valor maior que zero.')
            self.multiplier_xp = value
        elif key in ['CHAR_MULTIPLIER_XP', 'CHAR_XP']:
            value = float(value)
            if value < 0.0:
                raise ValueError(f'Forneça um valor maior que zero.')
            self.character_multiplier_xp = value
        else:
            raise KeyError(f'"{key}" não é uma chave válida.')

    def add_tier(self, player_id: Union[int, str], level: int):
        player_id = str(player_id)
        if player_id in self.tier.keys() or len(self.tier) < MAX_NUM_PLAYERS:
            self.tier[player_id] = level
        else:
            min_key = min(self.tier, key=self.tier.get)
            min_value = self.tier[min_key]
            if level > min_value:
                self.tier.pop(min_key)
                self.tier[player_id] = level

    def set_total_players(self, total_players: int):
        self.__total_players = total_players

    def add_event_points(self, points: int) -> bool:
        self.current_event_points += abs(int(points))
        self.current_event_points = min(
            self.current_event_points,
            self.max_event_points
        )

        return self.current_event_points >= self.max_event_points

    def add_event_points_from_player(self) -> bool:
        '''Fórmula para valores mínimos e máximos
        min_value = ceil(
            self.max_event_points / ((self.total_players/2)*60/MIN_ADD_MINUTES)
        )
        max_value = ceil(
            self.max_event_points / ((self.total_players/2)*60/MAX_ADD_MINUTES)
        )
        '''

        min_value = 17
        max_value = 34
        points = randint(min_value, max_value)

        return self.add_event_points(points)

    def add_event_points_from_group(self) -> bool:
        points = int(self.max_event_points * 0.17)
        if self.can_trigger_event:
            self.add_extra_event_points(0.50)

        return self.add_event_points(points)

    def reset_event_points(self):
        self.current_event_points = 0

    def add_extra_event_points(self, points: int) -> bool:
        self.current_extra_event_points += abs(points)
        self.current_extra_event_points = round(
            self.current_extra_event_points,
            2
        )
        self.current_extra_event_points = min(
            self.current_extra_event_points,
            MAX_EXTRA_EVENT_POINTS
        )

        return self.current_event_points >= self.max_event_points

    def reset_extra_event_points(self):
        self.current_extra_event_points = 0

    def get_extra_event_points(self) -> int:
        if self.can_trigger_extra_event:
            extra_event_points = int(self.current_extra_event_points)
            self.current_extra_event_points -= extra_event_points
            self.current_extra_event_points = round(
                self.current_extra_event_points,
                2
            )

            return extra_event_points
        else:
            raise ValueError('Não é possível pegar ponto do evento extra.')

    def __repr__(self) -> str:
        return (
            f'{SECTION_HEAD.format("Configuração do Grupo")}\n'
            f'Grupo: {self.name}\n'
            f'Chat ID: {self.chat_id}\n'
            f'Verbose: {self.verbose}\n'
            f'Silencioso: {self.silent}\n'
            f'Hora de Início de Spawn: {self.spawn_start_time:02}h\n'
            f'Hora de Fim de Spawn: {self.spawn_end_time}h\n'
            f'Multiplicador de XP: {self.multiplier_xp:.2f}\n'
            f'Mult. de XP por Nível: '
            f'{self.character_multiplier_xp:.2f}\n'
            f'Nível do Grupo: {self.group_level}\n'
            f'Total de Jogadores: {self.total_players}\n'
            f'{self.show_event_points}\n'
            f'{self.show_extra_event_points}\n'
            f'ID: {self.__id}\n'
            f'Criado em: {datetime_to_string(self.created_at)}\n'
            f'Atualizado em: {datetime_to_string(self.updated_at)}\n'
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            chat_id=self.chat_id,
            _id=self.__id,
            verbose=self.verbose,
            silent=self.silent,
            spawn_start_time=self.spawn_start_time,
            spawn_end_time=self.spawn_end_time,
            multiplier_xp=self.multiplier_xp,
            character_multiplier_xp=self.character_multiplier_xp,
            group_level=self.group_level,
            tier=self.tier,
            total_players=self.total_players,
            current_event_points=self.current_event_points,
            current_extra_event_points=self.current_extra_event_points,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


if __name__ == "__main__":
    group_config = Group(
        name='Grupo Teste',
        chat_id=1234,
        _id='ffffffffffffffffffffffff'
    )
    print('__repr__:\n', group_config)
    print('to_dict:', group_config.to_dict())
