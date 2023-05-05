from datetime import datetime, time
from typing import Union

from bson import ObjectId


class GroupConfiguration:
    def __init__(
        self,
        chat_id: int,
        verbose: bool = False,
        spawn_start_time: int = 6,
        spawn_end_time: int = 20,
        _id: Union[str, ObjectId] = None,
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
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return (
            f'GroupConfiguration(chat_id="{self.chat_id}" '
            f'verbose={self.verbose} '
            f'spawn_start_time={self.spawn_start_time} '
            f'spawn_end_time={self.spawn_end_time} '
            f'_id="{self._id}" '
            f'created_at="{self.created_at}" '
            f'updated_at="{self.updated_at}")'
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
    print('__repr__:', group_config)
