from typing import Union

from bson import ObjectId


class Consumable:
    def __init__(
        self,
        name: str,
        description: str,
        quantity: int,
        weight: float,
        function: str,
        _id: Union[str, ObjectId] = None,
    ) -> None:
        self.__name = name
        self.__description = description
        self.__quantity = quantity
        self.__weight = weight
        self.__function = function
        self.__id = _id

    def use(self, target):
        self.__quantity -= 1
        result = eval(self.__function)
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

    # Getters
    name = property(lambda self: self.__name)
    description = property(lambda self: self.__description)
    quantity = property(lambda self: self.__quantity)
    weight = property(lambda self: self.__weight * self.__quantity)
    function = property(lambda self: self.__function)
