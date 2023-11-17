from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.enums.turn import TurnEnum


class HealingCodition(Condition):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        frequency: Union[str, TurnEnum],
        turn: int = 1,
        level: int = 1,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        function = (
            'remaining_heal = self.power * self.turn;'
            'report = target.combat_stats.cure_hit_points(remaining_heal);'
            'self.last_turn()'
        )
        battle_function = (
            'report = target.combat_stats.cure_hit_points(self.power)'
        )
        super().__init__(
            name=name,
            description=description,
            function=function,
            battle_function=battle_function,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power


if __name__ == '__main__':
    print(HealingCodition(
        name='Heal Condition',
        description='Heal Condition Description',
        power=10,
        frequency=TurnEnum.START,
    ))
