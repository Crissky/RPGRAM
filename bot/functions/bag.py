
from typing import Union
from bot.constants.bag import ITEMS_PER_PAGE
from repository.mongo import BagModel, ItemModel
from rpgram import Item
from rpgram.consumables import Consumable, IdentifyingConsumable
from rpgram.boosters import Equipment


IDENTIFYING_LENS = 'Identifying Lens'


def get_item_by_position(user_id: int, page: int, item_pos: int) -> Item:
    '''Retorna um Item da Bag pela posição'''
    bag_model = BagModel()
    item_index = (ITEMS_PER_PAGE * page) + item_pos
    player_bag = bag_model.get(
        query={'player_id': user_id},
        fields={'items_ids': {'$slice': [item_index, 1]}},
        partial=False
    )
    item = player_bag[0]
    return item


def get_item_by_name(item_name: str) -> Union[Consumable, Equipment]:
    '''Retorna um item pelo nome'''
    item_model = ItemModel()
    item = item_model.get(query={'name': item_name})

    return item


def get_identifying_lens() -> IdentifyingConsumable:
    '''Retorna "Identifying Lens"'''
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
    id_lens = get_identifying_lens()
    print(type(id_lens))
    print(id_lens)
