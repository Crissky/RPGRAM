from datetime import datetime
from bson import ObjectId
from typing import Union


class Player:
    def __init__(
        self,
        name: str,
        player_id: str,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.player_id = player_id
        self.name = name
        self._id = _id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return (
            f'Player(name={self.name}, '
            f'id={self._id}, player_id={self.player_id}, '
            f'created_at={self.created_at}, updated_at={self.updated_at})'
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            player_id=self.player_id,
            _id=self._id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


if __name__ == '__main__':
    player = Player('Aroldo', 'TEL2', '98765432101234567890ffff')
    print('to_dict:', player.to_dict())
    print('__repr__:', player)
