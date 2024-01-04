from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.rarity import RarityEnum
from rpgram.stats.stats_combat import FULL_HEAL_VALUE


MINOR_HEALING_POTION_POWER = 50
LIGHT_HEALING_POTION_POWER = 100
HEALING_POTION_POWER = 200
GREATER_HEALING_POTION_POWER = 500
RARE_HEALING_POTION_POWER = 1000
EPIC_HEALING_POTION_POWER = 2500
LEGENDARY_HEALING_POTION_POWER = 5000
MYTHIC_HEALING_POTION_POWER = FULL_HEAL_VALUE

MINOR_REVIVE_POWER = 1


class HealingConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        weight: float,
        condition: Condition,
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
        self.power = power
        self.condition = condition

    @property
    def function(self) -> str:
        return ('report = target.combat_stats.cure_hit_points(self.power)')

    @property
    def battle_function(self) -> str:
        return (
            'report = target.status.add_condition(self.condition)'
        )

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            power=self.power,
            weight=super_dict['weight'],
            condition_name=self.condition.name if self.condition else None,
            rarity=super_dict['rarity'],
            usable=super_dict['usable'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


class ReviveConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
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
        self.power = power

    @property
    def function(self) -> str:
        return ('report = target.combat_stats.revive(self.power)')

    @property
    def battle_function(self) -> str:
        return None

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            power=self.power,
            weight=super_dict['weight'],
            rarity=super_dict['rarity'],
            usable=super_dict['usable'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


if __name__ == '__main__':
    healing_consumable = HealingConsumable(
        name='Heal Consumable',
        description='Heal Consumable',
        power=10,
        weight=1.0,
        condition=None,
    )

    print(healing_consumable)
    print(healing_consumable.to_dict())
