from pymongo import MongoClient
from decouple import config

URL_CONNECTION = config('URL_CONNECTION')
DATABASE_NAME = config('DATABASE_NAME')

if __name__ == '__main__':
    client = MongoClient(URL_CONNECTION, serverSelectionTimeoutMS=5000)
    db = client[DATABASE_NAME]

    # Collections
    bags = db['bags']
    equips = db['equips']
    items = db['items']

    cursor = items.find(filter={'_class': 'Equipment'}, projection={'_id': 1})
    ids = []
    for i, doc in enumerate(cursor):
        _id = doc['_id']
        bag_query = {'items_ids._id': _id}
        equips_query = {'$or': [
            {'helmet_id': _id},
            {'left_hand_id': _id},
            {'right_hand_id': _id},
            {'armor_id': _id},
            {'boots_id': _id},
            {'ring_id': _id},
            {'amulet_id': _id},
        ]}
        if bags.find_one(filter=bag_query, projection={'_id': 1}):
            print(f'({i:03}) {_id}: TÁ NA BOLSA!')
        elif equips.find_one(filter=equips_query, projection={'_id': 1}):
            print(f'({i:03}) {_id}: TÁ EQUIPADO!')
        else:
            ids.append(_id)
            print(f'({i:03}) {_id}: TÁ EM CANTO NENHUM!')

    result = items.delete_many({'_id': {'$in': ids}})
    print('TOTAL DE EQUIPAMENTOS DELETADOS:', result.deleted_count)
