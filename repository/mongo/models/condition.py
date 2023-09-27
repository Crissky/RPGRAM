from repository.mongo import Model
from repository.mongo.collection_enum import CollectionEnum
from rpgram import Condition


class ConditionModel(Model):
    _class = property(lambda self: Condition)
    collection = property(lambda self: CollectionEnum.CONDITION.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    ...
