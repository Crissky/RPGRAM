
from repository.mongo import BagModel, ItemModel
from rpgram import Item


IDENTIFYING_LENS = 'Identifying Lens'


def get_item_by_name(item_name: str) -> Item:
    item_model = ItemModel()
    item = item_model.get(query={'name': item_name})

    return item


def get_identifying_lens() -> Item:
    return get_item_by_name(IDENTIFYING_LENS)


def get_id_item_by_name(item_name: str) -> dict:
    item_model = ItemModel()
    item_dict = item_model.get(
        query={'name': item_name},
        fields=['_id', 'name'],
    )

    return item_dict


def exists_in_bag(item_name: str, user_id: int) -> bool:
    bag_model = BagModel()
    item_dict = get_id_item_by_name(item_name)
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
    return exists_in_bag(IDENTIFYING_LENS, user_id)


def sub_item_by_name(item_name: str, user_id: int):
    if not exists_in_bag(item_name, user_id):
        raise ValueError(f'Item "{item_name}" não está no inventário.')

    bag_model = BagModel()
    item = get_item_by_name(item_name)
    item_id = item._id
    query = {'player_id': user_id, 'items_ids._id': item_id}
    fields = {'items_ids.$': 1}
    bag_dict = bag_model.get(query=query, fields=fields)
    item_quantity = bag_dict['items_ids'][0]['quantity']
    item.quantity = item_quantity
    bag_model.sub(item, user_id)


def sub_identifying_lens(user_id: int) -> bool:
    return sub_item_by_name(IDENTIFYING_LENS, user_id)


if __name__ == '__main__':
    sub_identifying_lens(370221845)
