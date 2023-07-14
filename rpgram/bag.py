from datetime import datetime
from typing import List, Union

from bson import ObjectId

from rpgram.boosters import Equipment
from rpgram import Consumable, Item


ItemTypes = Union[Consumable, Equipment, Item]


class Bag:
    def __init__(
        self, items: List[Item],
        player_id: int,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__items = [self.pack_item(item) for item in items]
        self.__player_id = player_id
        self.__id = _id
        self.__created_at = created_at
        self.__updated_at = updated_at

    def pack_item(item: ItemTypes) -> Item:
        if isinstance(item, (Consumable, Equipment)):
            item = Item(item)
        if isinstance(item, Item):
            return item
        raise TypeError(f'Tipo esperado "{ItemTypes}", obtido "{type(item)}"')

    def get_item(self, item: ItemTypes = None, slot: int = None) -> ItemTypes:
        if item and item in self.__items:
            return self.__items[self.__items.index(item)]
        elif slot:
            return self.__items[slot]

    def add(self, item: ItemTypes) -> None:
        item = self.pack_item(item)
        bag_item = self.get_item(item)
        if bag_item:
            bag_item.quantity += item.quantity
        else:
            self.__items.append(item)

    def remove(
        self,
        item: ItemTypes = None,
        slot: int = None,
        quantity: int = 1
    ):
        item = self.pack_item(item)
        bag_item = self.get_item(item, slot)
        if bag_item:
            bag_item.quantity -= quantity
        else:
            raise ValueError('Item não encontrado no Inventário.')

        if bag_item.quantity <= 0:
            self.__items.remove(bag_item)

    def to_dict(self):
        return dict(
            items=[item.to_dict() for item in self.__items],
            player_id=self.__player_id,
            _id=self.__id,
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    # Getters
    @property
    def weight(self):
        return sum([item.item.weight for item in self.__items])
