from datetime import datetime


class Player:
    def __init__(
        self, _id: str, telegram_id: str, name: str,
        created_at: datetime = datetime.now()
    ) -> None:
        self._id = _id
        self.telegram_id = telegram_id
        self.name = name
        self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f'Player(id={self._id}, telegram_id={self.telegram_id}, '
            f'name={self.name}, created_at={self.created_at})'
        )


if __name__ == '__main__':
    player = Player('ID1', 'TEL2', 'Aroldo', datetime.now())
    print('__dict__:', player.__dict__)
    print('__repr__:', player)
