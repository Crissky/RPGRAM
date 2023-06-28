from typing import Union

from bson import ObjectId


class Consumable:
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        function: str,
        _id: Union[str, ObjectId] = None,
    ) -> None:
        self.__name = name
        self.__description = description
        self.__weight = weight
        self.__function = function
        self.__id = _id

    def use(self, target):
        result = exec(self.__function)
        return result

    def to_dict(self):
        return dict(
            name=self.__name,
            description=self.__description,
            quantity=self.__quantity,
            weight=self.__weight,
            function=self.__function,
            _id=self.__id,
        )

    def __eq__(self, other):
        if isinstance(other, Consumable):
            return self._id == other._id
        return False

    # Getters
    _id = property(lambda self: self.__id)
    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)
    weight = property(lambda self: self.__weight * self.__quantity)
    function = property(lambda self: self.__function)
