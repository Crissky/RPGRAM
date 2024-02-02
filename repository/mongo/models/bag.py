from typing import Any
from repository.mongo import Model
from repository.mongo import CollectionEnum
from repository.mongo.models.item import ItemModel
from rpgram import Bag, Item


class BagModel(Model):
    def add(self, item: Item, player_id: int, quantity: int = None) -> Any:
        query = {'player_id': player_id, 'items_ids._id': item._id}
        exists = bool(self.database.count(self.collection, query, limit=1))
        quantity = item.quantity if quantity is None else quantity

        if quantity <= 0:
            raise ValueError(
                f'Quantidade inválida. Não pode adicionar uma quantidade '
                f'menor ou igual a zero. Quantidade: {quantity}.'
            )

        if exists:  # incrementa se existir na bag
            result = self.database.update(
                collection=self.collection,
                query=query,
                data={
                    '$inc': {
                        'items_ids.$.quantity': quantity
                    }
                }
            )
        else:  # adicione se não existir na bag
            result = self.database.update(
                collection=self.collection,
                query={'player_id': player_id},
                data={
                    '$push': {
                        'items_ids': {
                            '_id': item._id,
                            'quantity': quantity
                        }
                    }
                }
            )

        return result

    def sub(self, item: Item, player_id: int, quantity: int = -1) -> Any:
        quantity = -abs(int(quantity))
        query = {'player_id': player_id, 'items_ids._id': item._id}
        exists = bool(self.database.count(self.collection, query, limit=1))

        if quantity >= 0:
            raise ValueError(
                f'Quantidade inválida. A quantidade deve ser um valor menor '
                f'que zero. Quantidade: {quantity}.'
            )
        if exists:  # decrementa se existir na bag
            result1 = self.database.update(
                collection=self.collection,
                query=query,
                data={
                    '$inc': {
                        'items_ids.$.quantity': quantity
                    }
                }
            )
            # Remove todos os items com quantidade menor ou igual a zero
            result2 = self.database.update(
                collection=self.collection,
                query={'player_id': player_id},
                data={
                    '$pull': {
                        'items_ids': {
                            'quantity': {'$lte': 0}
                        }
                    }
                }
            )
        else:
            raise ValueError(
                f'Item não encontrado no bag. Não foi possível decrementar '
                f'a quantidade {quantity}.'
            )

        return result1, result2

    _class = property(lambda self: Bag)
    collection = property(lambda self: CollectionEnum.BAGS.value)
    populate_fields = property(
        lambda self: {
            'items': {
                'id_key': 'items_ids',
                'model': ItemModel(),
                'subclass': Item
            }
        }
    )


if __name__ == '__main__':
    from rpgram.consumables import Consumable
    potion = Consumable(
        name='Potion',
        description='Cura 100 de HP.',
        weight=0.1,
        function='target.combat_stats.hp = 100',
        _id='888888888888888888888888'
    )
    bag = Bag(
        items=[potion, potion, potion],
        player_id='ffffffffffffffffffffffff',
        _id='ffffffffffffffffffffffff'
    )
    print(f'bag:\n{bag}')
    bag_model = BagModel()
    bag_model.save(bag)
    bag2 = bag_model.get('ffffffffffffffffffffffff')
    print(f'bag2:\n{bag2}')
