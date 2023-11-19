from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.enums.turn import TurnEnum


class HealingCondition(Condition):
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
        super().__init__(
            name=name,
            description=description,
            function=None,
            battle_function=None,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power

    @property
    def function(self) -> str:
        return (
            'remaining_heal = abs(self.power * self.turn);'
            'report = target.combat_stats.cure_hit_points(remaining_heal);'
            'self.last_turn()'
        )

    @property
    def battle_function(self) -> str:
        return (
            'report = target.combat_stats.cure_hit_points(self.power)'
        )

    def to_dict(self) -> dict:
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            power=self.power,
            frequency=super_dict['frequency'],
            turn=super_dict['turn'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


if __name__ == '__main__':
    healing_condition = HealingCondition(
        name='Heal Condition',
        description='Heal Condition Description',
        power=10,
        frequency=TurnEnum.START,
    )

    print(healing_condition)
    print(healing_condition.to_dict())
