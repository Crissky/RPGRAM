from datetime import datetime
from typing import Union

from bson import ObjectId

from rpgram.conditions.condition import Condition
from rpgram.enums.turn import TurnEnum


class BuffCondition(Condition):

    def __init__(
        self,
        name: str,
        frequency: Union[str, TurnEnum],
        turn: int = 1,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
