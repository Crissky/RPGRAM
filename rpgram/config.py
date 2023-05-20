from datetime import datetime
from typing import Union

from bson import ObjectId

from constants.text import SECTION_HEAD
from functions.datetime import datetime_to_string


class GroupConfiguration:
    def __init__(
        self,
        name: str,
        chat_id: int,
        _id: Union[str, ObjectId] = None,
        verbose: bool = False,
        spawn_start_time: int = 6,
        spawn_end_time: int = 20,
        multiplier_xp: float = 1.0,
        player_multiplier_xp: float = 1.0,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.name = name
        self.chat_id = chat_id
        self.verbose = verbose
        self.spawn_start_time = spawn_start_time
        self.spawn_end_time = spawn_end_time
        self._id = _id
        self.multiplier_xp = float(multiplier_xp)
        self.player_multiplier_xp = float(player_multiplier_xp)
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return (
            SECTION_HEAD.format('Configuração do Grupo') +
            f'Grupo: {self.name}\n'
            f'Chat ID: {self.chat_id}\n'
            f'Verbose: {self.verbose}\n'
            f'Hora de Início de Spawn: {self.spawn_start_time:02}h\n'
            f'Hora de Fim de Spawn: {self.spawn_end_time}h\n'
            f'ID: {self._id}\n'
            f'Multiplicador Geral de XP: {self.multiplier_xp:.2f}\n'
            f'Mult. de XP por Nível: '
            f'{self.player_multiplier_xp:.2f}\n'
            f'Criado em: {datetime_to_string(self.created_at)}\n'
            f'Atualizado em: {datetime_to_string(self.updated_at)}\n'
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            chat_id=self.chat_id,
            verbose=self.verbose,
            spawn_start_time=self.spawn_start_time,
            spawn_end_time=self.spawn_end_time,
            _id=self._id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


if __name__ == "__main__":
    group_config = GroupConfiguration(
        name='Grupo Teste',
        chat_id=1234,
        _id='ffffffffffffffffffffffff'
    )
    print('__repr__:\n', group_config)
    print('to_dict:', group_config.to_dict())
