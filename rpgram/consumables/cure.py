from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.rarity import RarityEnum


class CureConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        condition_name: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        usable: bool = True,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        function = (
            f'report = target.status.remove_condition(self.condition_name)'
        )
        battle_function = None
        super().__init__(
            name=name,
            description=description,
            weight=weight,
            condition=None,
            function=function,
            battle_function=battle_function,
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.condition_name = condition_name
    
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
    print(CureConsumable(
        name='Cure Consumable',
        description='Cure Description',
        condition_name='Poison',
        weight=1.0,
    ))