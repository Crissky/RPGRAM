from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.rarity import RarityEnum


class IdentifyingConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
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
            usable=False,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    @property
    def function(self) -> str:
        return f'report = target.identify()'

    @property
    def battle_function(self) -> str:
        return (
            'report = {"text": f"{self.name} não pode ser usado em batalha."}'
        )

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            weight=super_dict['weight'],
            rarity=super_dict['rarity'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


if __name__ == '__main__':
    identifying_consumable = IdentifyingConsumable(
        name='Identifying Consumable',
        description='Identifying Description',
        weight=1.0,
    )

    print(identifying_consumable)
    print(identifying_consumable.to_dict())