from datetime import datetime
from typing import Union

from bson import ObjectId

from constant.text import SECTION_HEAD
from function.datetime import datetime_to_string


MAX_NUM_PLAYERS = 3


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
        higher_level: int = 1,
        tier: dict = {},
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
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
        self.created_at = created_at
        self.updated_at = updated_at

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

    def add_tier(self, player_id: Union[int, str], level: int) -> None:
        player_id = str(player_id)
        if player_id in self.tier.keys() or len(self.tier) < MAX_NUM_PLAYERS:
            self.tier[player_id] = level
        else:
            min_key = min(self.tier, key=self.tier.get)
            min_value = self.tier[min_key]
            if level > min_value:
                self.tier.pop(min_key)
                self.tier[player_id] = level

    @property
    def higher_level(self) -> int:
        higher_level = 1
        if self.tier:
            higher_level = sum(self.tier.values()) // len(self.tier)

        return higher_level

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
            f'Nível do Grupo: {self.higher_level}\n'
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
            tier=self.tier,
            higher_level=self.higher_level,
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
