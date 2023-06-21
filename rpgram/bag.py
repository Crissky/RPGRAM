from typing import List, Union

from bson import ObjectId

from rpgram.boosters import Equipment
from rpgram import Consumable

Items_Types = Union[Equipment, Consumable]


class Bag:
    def __init__(
        self, items: List[Items_Types],
        _id: Union[str, ObjectId] = None,
    ):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__items = items
        self.__id = _id

    def get(self, item: Items_Types = None, slot: int = None) -> Items_Types:
        if item:
            return self.__items[self.__items.index(item)]
        elif slot:
            return self.__items[slot]

    def add(self, item: Items_Types):
        self.__items.append(item)

    def remove(self, item: Items_Types = None, slot: int = None):
        if slot:
            self.__items.pop(slot)
        elif slot:
            self.__items.remove(item)

    def to_dict(self):
        return dict(
            items=[item._id for item in self.__items],
            id=self.__id
        )

    @property
    def weight(self):
        return sum([item.weight for item in self.__items])
