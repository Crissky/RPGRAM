from bson import ObjectId
from random import randint, randrange
from typing import List, Union

from bot.constants.bag import ITEMS_PER_PAGE
from repository.mongo import BagModel, ItemModel
from rpgram import Item
from rpgram.consumables import Consumable, IdentifyingConsumable
from rpgram.boosters import Equipment


IDENTIFYING_LENS = 'Identifying Lens'
LIMIT_ITEM_IN_BAG = 100


def get_item_by_position(user_id: int, page: int, item_pos: int) -> Item:
    '''Retorna um Item da Bag pela posição.
    '''

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
    '''Retorna um item pelo nome.
    '''

    item_model = ItemModel()
    item = item_model.get(query={'name': item_name})

    return item


def get_identifying_lens() -> IdentifyingConsumable:
    '''Retorna "Identifying Lens".
    '''

    return get_item_by_name(IDENTIFYING_LENS)


def get_id_item_by_name(item_name: str) -> dict:
    '''Retorna um dicionário com o _id e o name do item.
    '''

    item_model = ItemModel()
    item_dict = item_model.get(
        query={'name': item_name},
        fields=['_id', 'name'],
    )

    return item_dict


def exists_in_bag(
    user_id: int,
    item_id: str = None,
    item_name: str = None
) -> bool:
    '''Verifica se um item está na bag. Retornando True caso esteja e False 
    caso contrário.
    '''

    if item_id is None and item_name is None:
        raise ValueError('É necessário passar um item_id ou item_name.')
    elif item_id and item_name:
        raise ValueError(
            'É necessário passar um item_id ou item_name, não ambos.'
        )

    if item_name:
        item_dict = get_id_item_by_name(item_name)
        if item_dict:
            item_id = item_dict['_id']
        else:
            raise ValueError(f'Item "{item_name}" não existe no banco.')
    elif isinstance(item_id, str):
        item_id = ObjectId(item_id)

    bag_model = BagModel()
    query = {
        'player_id': user_id,
        'items_ids': {
            '$elemMatch': {'_id': item_id}
        }
    }
    item_in_bag = bag_model.get(query=query, fields=['_id'])

    return bool(item_in_bag)


def have_identifying_lens(user_id: int) -> bool:
    '''Verifica se o jogador possui um "Identifying Lens" na bolsa.
    Retorna True caso tenha e False caso contrário.
    '''

    return exists_in_bag(user_id, item_name=IDENTIFYING_LENS)


def sub_item_by_name(item_name: str, user_id: int):
    '''Subtrai um item da bag pelo nome.
    '''

    if not exists_in_bag(user_id, item_name=item_name):
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
    '''Subtrai um "Identifying Lens" da bag.
    '''

    return sub_item_by_name(IDENTIFYING_LENS, user_id)


def drop_random_items_from_bag(user_id: int) -> List[Item]:
    '''Subtrai itens aleatórios da Bag e retorna uma lista do itens subtraidos.
    '''

    bag_model = BagModel()
    item_model = ItemModel()
    drop_items = []
    query = {'player_id': user_id}
    items_ids = bag_model.get(query=query, fields=['items_ids'])
    if items_ids:
        items_ids = items_ids['items_ids']
    else:
        print(f'Usuário de ID "{user_id}" não possui itens na bolsa.')
        return None
    total_drop_items = randint(3, 10)
    total_drop_items = min(total_drop_items, len(items_ids))
    for _ in range(total_drop_items):
        choiced_index = randrange(len(items_ids))
        item_dict = items_ids.pop(choiced_index)
        item_id = item_dict['_id']
        item_quantity = item_dict['quantity']
        drop_quantity = randint(1, item_quantity)
        drop_item = item_model.get(query={'_id': item_id})
        drop_item = Item(drop_item, quantity=drop_quantity)
        drop_items.append(drop_item)

    for drop_item in drop_items:
        bag_model.sub(drop_item, user_id, drop_item.quantity)

    return drop_items


def is_full_bag(user_id: int) -> bool:
    '''Verifica se a bag está cheia.
    Retorna True caso tenho uma quantidade de itens igual ou maior que
    LIMIT_ITEM_IN_BAG e False caso contrário.
    '''

    bag_model = BagModel()
    query = {
        'player_id': user_id,
        f'items_ids.{LIMIT_ITEM_IN_BAG}': {'$exists': True}
    }
    bag_dict = bag_model.get(query=query, fields=['player_id'])
    print(bag_dict)

    return bool(bag_dict)


if __name__ == '__main__':
    from decouple import config

    MY_ID = config('MY_ID', cast=int)

    # sub_identifying_lens(MY_ID)
    id_lens = get_identifying_lens()
    print(type(id_lens))
    print(id_lens)
    print('have_identifying_lens:', have_identifying_lens(MY_ID))
    # print(drop_random_items_from_bag(MY_ID))
    print('is_full_bag:', is_full_bag(MY_ID))
