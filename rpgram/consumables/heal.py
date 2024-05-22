from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum
from rpgram.constants.stats.stats_combat import FULL_HEAL_VALUE


MINOR_HEALING_POTION_POWER = 100
LIGHT_HEALING_POTION_POWER = 500
HEALING_POTION_POWER = 1_000
GREATER_HEALING_POTION_POWER = 5_000
RARE_HEALING_POTION_POWER = 10_000
EPIC_HEALING_POTION_POWER = 50_000
LEGENDARY_HEALING_POTION_POWER = 100_000
MYTHIC_HEALING_POTION_POWER = FULL_HEAL_VALUE

MINOR_REVIVE_POWER = 1
REVIVE_POWER = 1000


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
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power
        self.condition = condition

    def function(self, target) -> dict:
        report = target.combat_stats.cure_hit_points(self.power)

        return report

    def battle_function(self, target) -> dict:
        report = target.status.add_condition(self.condition)

        return report

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

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.HEALING_CONSUMABLE.value

    @property
    def price(self) -> int:
        if self.power == MYTHIC_HEALING_POTION_POWER:
            base_value = LEGENDARY_HEALING_POTION_POWER * 2
        else:
            base_value = self.power / 20

        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value + (rarity_multiplier * 10)

        return int(price)


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
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power

    def function(self, target) -> dict:
        report = target.combat_stats.revive(self.power)

        return report

    def battle_function(self, target) -> dict:
        return self.function(target=target)

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

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.REVIVE_CONSUMABLE.value

    @property
    def price(self) -> int:
        base_value = (100 + self.power) * 2
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value * rarity_multiplier

        return int(price)


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
