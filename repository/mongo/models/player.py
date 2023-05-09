from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import Player


class PlayerModel(Model):

    _class = property(lambda self: Player)
    collection = property(lambda self: CollectionEnum.PLAYERS.value)


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
    print('get_all len=1:', player_model.get_all(fields='name'))
    print('get_all len=2', player_model.get_all(fields=['name', 'player_id']))
    print('get_all None:', player_model.get_all())
