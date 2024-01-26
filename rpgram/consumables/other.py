from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum


PROFICIENCY_ELIXIR_POWER = 10
RARE_PROFICIENCY_ELIXIR_POWER = 25
EPIC_PROFICIENCY_ELIXIR_POWER = 50
LEGENDARY_PROFICIENCY_ELIXIR_POWER = 100
MYTHIC_PROFICIENCY_ELIXIR_POWER = 250


class IdentifyingConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.RARE,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=description,
            weight=weight,
            rarity=rarity,
            usable=False,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def function(self, target) -> dict:
        report = target.identify()

        return report

    def battle_function(self) -> dict:
        report = {"text": f"{self.name} não pode ser usado em batalha."}

        return report

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

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.IDENTIFY_CONSUMABLE.value

    @property
    def price(self) -> int:
        base_value = 500
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value * rarity_multiplier

        return int(price)


class XPConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.RARE,
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
        report = target.base_stats.add_xp(self.power)

        return report

    def battle_function(self, target) -> dict:
        report = target.base_stats.add_xp(self.power)

        return report

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
    def price(self) -> int:
        base_value = (100 + self.power) * 2
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value * rarity_multiplier

        return int(price)


if __name__ == '__main__':
    identifying_consumable = IdentifyingConsumable(
        name='Identifying Consumable',
        description='Identifying Description',
        weight=1.0,
    )
    xp_consumable = XPConsumable(
        name='XP Consumable',
        description='XP Description',
        power=100,
        weight=1.0,
    )

    print(identifying_consumable)
    print(identifying_consumable.to_dict())
    print(xp_consumable)
    print(xp_consumable.to_dict())
