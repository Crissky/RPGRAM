from repository.mongo import Model
from repository.mongo import CollectionEnum
from repository.mongo.models.item import ItemModel
from rpgram import Bag


class BagModel(Model):
    _class = property(lambda self: Bag)
    collection = property(lambda self: CollectionEnum.BAGS.value)
    populate_fields = property(
        lambda self: {
            'items': {
                'id_key': 'items_ids',
                'model': ItemModel()
            }
        }
    )


if __name__ == '__main__':
    from rpgram import Consumable
    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100',
        _id='888888888888888888888888'
    )
    bag = Bag(
        items=[potion],
        player_id='ffffffffffffffffffffffff',
        _id='ffffffffffffffffffffffff'
    )
    bag_model = BagModel()
    bag_model.save(bag)
    bag2 = bag_model.get('ffffffffffffffffffffffff')
    print(f'bag2: {bag2}')
