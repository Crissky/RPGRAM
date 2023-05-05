from repository.mongo import CollectionEnum
from rpgram import Player
from repository.mongo import Model


class PlayerModel(Model):

    _class = property(lambda s: Player)
    collection = property(lambda s: CollectionEnum.PLAYERS.value)


if __name__ == '__main__':
    player = Player('Aroldo de Novo', 2, '645006f6d8fefae3f4c268f1')
    player_model = PlayerModel()
    print(f'Collection: {player_model.collection}')
    result = player_model.save(player)
    print('result:', result)
    player2 = player_model.get(2)
    print('player2:', player2)
