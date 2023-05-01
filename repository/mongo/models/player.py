from bson import ObjectId
from repository.mongo import CollectionEnum
from repository.mongo import Database
from rpgram import Player
from repository.mongo import Model


class PlayerModel(Model):

    _class = property(lambda s: Player)
    collection = property(lambda s: CollectionEnum.PLAYERS.value)
    database = property(lambda s: Database.get_instance())


if __name__ == '__main__':
    player = Player('Aroldo de Novo','PLAYER_2', '645006f6d8fefae3f4c268f1')
    player_model = PlayerModel()
    print(f'Collection: {player_model.collection}')
    result = player_model.save(player)
    print('result:', result)
    player2 = player_model.get('PLAYER_2')
    print('player2:', player2)
