from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import Player


class PlayerModel(Model):

    _class = property(lambda s: Player)
    collection = property(lambda s: CollectionEnum.PLAYERS.value)


if __name__ == '__main__':
    player = Player(
        name='PLAYER TESTE MODEL',
        player_id=2,
        _id='ffffffffffffffffffffffff'
    )
    player_model = PlayerModel()
    print(f'Collection: {player_model.collection}')
    result = player_model.save(player)
    print('result:', result)
    player2 = player_model.get(2)
    print('player2:', player2)
