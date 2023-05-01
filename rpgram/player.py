from bson import ObjectId
from datetime import datetime
from typing import Union


class Player:
    def __init__(
        self, _id: Union[str, ObjectId], player_id: str, name: str,
        created_at: datetime = datetime.now()
    ) -> None:
        self._id = _id
        self.player_id = player_id
        self.name = name
        self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f'Player(id={self._id}, player_id={self.player_id}, '
            f'name={self.name}, created_at={self.created_at})'
        )
    
    def to_dict(self) -> dict:
        return dict(
            _id=self._id,
            player_id=self.player_id,
            name=self.name,
            created_at=self.created_at
        )


if __name__ == '__main__':
    player = Player('ID1', 'TEL2', 'Aroldo', datetime.now())
    print('to_dict:', player.to_dict())
    print('__repr__:', player)
