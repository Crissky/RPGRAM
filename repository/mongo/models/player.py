from repository.mongo import CollectionEnum
from repository.mongo import Database
from rpgram import Player


class PlayerModel:

    def get(self, telegram_id: str) -> Player or None:
        player = self.database.find(
            self.collection, {'telegram_id': telegram_id})
        if player:
            return Player(**player)

    def save(self, player: Player):
        player_json = player.__dict__
        player_json.pop('_id')
        query = {'telegram_id': player.telegram_id}
        if self.database.find(self.collection, query):
            print('update')
            result = self.database.update(
                self.collection, query, {'$set': player_json}
            )
        else:
            print('insert')
            result = self.database.insert(self.collection, player_json)
        return result

    collection = property(lambda s: CollectionEnum.players.value)
    database = property(lambda s: Database.get_instance())


if __name__ == '__main__':
    player = Player('ID1', 'TEL2', 'Aroldo Novo')
    player_model = PlayerModel()
    print(f'Collection: {player_model.collection}')
    result = player_model.save(player)
    print(result)
    player2 = player_model.get('TEL2')
    print('player2:', player2)
