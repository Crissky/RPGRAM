from datetime import datetime
from random import uniform
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.consumable import Consumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum
from rpgram.enums.trocado import TrocadoEnum


PROFICIENCY_ELIXIR_POWER = 25
RARE_PROFICIENCY_ELIXIR_POWER = 50
EPIC_PROFICIENCY_ELIXIR_POWER = 100
LEGENDARY_PROFICIENCY_ELIXIR_POWER = 250
MYTHIC_PROFICIENCY_ELIXIR_POWER = 500


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


class TentConsumable(Consumable):
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
        report = {'text': f'{target.name} começou a desansar na barraca.'}

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
        return EmojiEnum.TENT_CONSUMABLE.value

    @property
    def price(self) -> int:
        base_value = 5000
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


class TrocadoPouchConsumable(Consumable):
    def __init__(
        self,
        name: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=None,
            weight=weight,
            rarity=rarity,
            usable=False,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def function(self, target) -> dict:
        report = target.add_trocado(self.price)

        return report

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            weight=super_dict['weight'],
            rarity=super_dict['rarity'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )

    @property
    def description(self) -> str:
        rarity = self.rarity.value.lower()
        return (
            f'Um monedero{EmojiEnum.TROCADO_POUCH.value} {rarity} contendo '
            f'{self.price}{EmojiEnum.TROCADO.value}.'
        )

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.TROCADO_POUCH.value

    @property
    def price(self) -> int:
        base_value = 100
        trocado_multiplier = self.weight
        price = base_value * trocado_multiplier

        return int(price)

    @property
    def sell_price(self) -> int:
        return self.price


class GemstoneConsumable(Consumable):
    def __init__(
        self,
        name: str,
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=None,
            weight=weight,
            rarity=rarity,
            usable=False,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def function(self, target) -> dict:
        report = target.add_trocado(self.price)

        return report

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            weight=super_dict['weight'],
            rarity=super_dict['rarity'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )

    @property
    def description(self) -> str:
        rarity = self.rarity.value.lower()
        return (
            f'{self.name} é uma pedra preciosa {rarity} que pode '
            f'ser vendida para garantir uns '
            f'{TrocadoEnum.TROCADOS.value}{EmojiEnum.TROCADO.value}.'
        )

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.GEMSTONE.value

    @property
    def price(self) -> int:
        base_value = 2500 * uniform(0.95, 1.05)
        trocado_multiplier = self.weight
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value * trocado_multiplier * (rarity_multiplier ** 2)

        return int(price)

    @property
    def sell_price(self) -> int:
        return self.price


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
    trocado_purse_consumable = TrocadoPouchConsumable(
        name=f'{TrocadoEnum.TROCADO.value} Purse Consumable',
        weight=0.1,
    )
    gemstone_consumable = GemstoneConsumable(
        name='Gemstone Consumable',
        weight=0.1,
    )

    print(identifying_consumable)
    print(identifying_consumable.to_dict())
    print(xp_consumable)
    print(xp_consumable.to_dict())
    print(trocado_purse_consumable)
    print(trocado_purse_consumable.to_dict())
    print(gemstone_consumable)
    print(gemstone_consumable.to_dict())
