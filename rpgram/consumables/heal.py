from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.rarity import RarityEnum


class HealingConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        weight: float,
        condition: Condition = None,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        usable: bool = True,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        function = ('report = target.combat_stats.cure_hit_points(self.power)')
        battle_function = (
            'report = target.status.add_condition(self.condition)'
        )
        super().__init__(
            name=name,
            description=description,
            weight=weight,
            condition=condition,
            function=function,
            battle_function=battle_function,
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            power=self.power,
            weight=super_dict['weight'],
            condition_name=super_dict['condition_name'],
            rarity=super_dict['rarity'],
            usable=super_dict['usable'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )

if __name__ == '__main__':
    print(HealingConsumable(
        name='Heal Consumable',
        description='Heal Consumable',
        power=10,
        weight=1.0,
    ))