from datetime import datetime, time
from typing import Union

from bson import ObjectId

from functions.datetime import datetime_to_string


class GroupConfiguration:
    def __init__(
        self,
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
            f'◇── Configuração do Grupo ──◇\n'
            f'Chat ID: {self.chat_id}\n'
            f'Verbose: {self.verbose}\n'
            f'Hora de Início de Spawn: {self.spawn_start_time:02}h\n'
            f'Hora de Fim de Spawn: {self.spawn_end_time}h\n'
            f'ID: {self._id}\n'
            f'Multiplicador Geral de XP: {self.multiplier_xp}\n'
            f'Multiplicador de XP do Jogador: {self.player_multiplier_xp}\n'
            f'created_at: {datetime_to_string(self.created_at)}\n'
            f'updated_at: {datetime_to_string(self.updated_at)}\n'
        )

    def to_dict(self) -> dict:
        return dict(
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
        1234
    )
    print('to_dict:', group_config.to_dict())
    print('__repr__:\n', group_config)
