from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import Consumable


class ConsumableModel(Model):
    _class = property(lambda self: Consumable)
    collection = property(lambda self: CollectionEnum.CONSUMABLES.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    consumable_model = ConsumableModel()
    potion = Consumable(
        name='TESTE POÇÃO',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100',
        _id='ffffffffffffffffffffffff'
    )
    consumable_model.save(potion)
    potion2 = consumable_model.get('ffffffffffffffffffffffff')
    print('potion2', potion2)
    potion3 = consumable_model.get('TESTE POÇÃO')
    print('potion3', potion3)
