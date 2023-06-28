from typing import List, Union

from bson import ObjectId

from rpgram.boosters import Equipment
from rpgram import Consumable, Item


ItemTypes = Union[Consumable, Equipment, Item]


class Bag:
    def __init__(
        self, items: List[Item],
        _id: Union[str, ObjectId] = None,
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__items = [self.make_item(item) for item in items]
        self.__id = _id

    def make_item(item: ItemTypes) -> Item:
        if isinstance(item, (Consumable, Equipment)):
            item = Item(item)
        if isinstance(item, Item):
            return item
        raise TypeError(f'Tipo esperado "{ItemTypes}", obtido "{type(item)}"')

    def get_item(self, item: ItemTypes = None, slot: int = None) -> ItemTypes:
        if item:
            return self.__items[self.__items.index(item)]
        elif slot:
            return self.__items[slot]

    def add(self, item: ItemTypes):
        item = self.make_item(item)
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
        item = self.make_item(item)
        bag_item = self.get_item(item, slot)
        if bag_item:
            bag_item.quantity -= quantity
        else:
            raise ValueError('Item não encontrado no Inventário.')

        if bag_item.quantity == 0:
            self.__items.remove(bag_item)

    def to_dict(self):
        return dict(
            items=[item._id for item in self.__items],
            id=self.__id
        )

    @property
    def weight(self):
        return sum([item.item.weight for item in self.__items])
