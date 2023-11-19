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
        condition_target: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        usable: bool = True,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=description,
            weight=weight,
            function=None,
            battle_function=None,
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.condition_target = condition_target

    @property
    def function(self) -> str:
        return (
            f'report = target.status.remove_condition(self.condition_target)'
        )

    @property
    def battle_function(self) -> None:
        return None

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            weight=super_dict['weight'],
            condition_target=self.condition_target,
            rarity=super_dict['rarity'],
            usable=super_dict['usable'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


if __name__ == '__main__':
    cure_consumable = CureConsumable(
        name='Cure Consumable',
        description='Cure Description',
        condition_target='Poison',
        weight=1.0,
    )

    print(cure_consumable)
    print(cure_consumable.to_dict())