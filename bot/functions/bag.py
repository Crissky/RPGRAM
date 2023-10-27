
from repository.mongo import BagModel, ItemModel


def exists_in_bag(item_name: str, user_id: int) -> bool:
    item_model = ItemModel()
    bag_model = BagModel()
    item_dict = item_model.get(
        query={'name': item_name},
        fields=['_id', 'name'],
    )
    item_id = item_dict['_id']
    query = {
        'player_id': user_id,
        'items_ids': {
            '$elemMatch': {'_id': item_id}
        }
    }
    item_in_bag = bag_model.get(query=query, fields=['_id'])

    return bool(item_in_bag)


def have_identifying_lens(user_id: int) -> bool:
    return exists_in_bag('Identifying Lens', user_id)
