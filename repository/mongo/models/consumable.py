from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import Consumable


class ConsumableModel(Model):
    _class = property(lambda self: Consumable)
    collection = property(lambda self: CollectionEnum.CONSUMABLES.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    consumable_model = ConsumableModel()
