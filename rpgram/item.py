from typing import Union

from rpgram.boosters import Equipment
from rpgram import Consumable

ItemsTypes = Union[Equipment, Consumable]


class Item:
    def __init__(self, item: ItemsTypes, quantity: int = 1):
        self.item = item
        self.__quantity = quantity

    @property
    def name(self):
        return self.item.name

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        quantity = self.__quantity
        self.__quantity = value
        if self.__quantity < 0:
            error_quantity = self.__quantity
            self.__quantity = quantity
            raise ValueError(
                f'Item não pode ter um valor negativo ({error_quantity}).'
            )

    def to_dict(self):
        return dict(
            item=self.item._id,
            quantity=self.quantity
        )

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.item == other.item
        return self.item == other
