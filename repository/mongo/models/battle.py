from repository.mongo import Model
from repository.mongo import CollectionEnum
from repository.mongo import CharacterModel
from rpgram import Battle


class BattleModel(Model):
    _class = property(lambda self: Battle)
    collection = property(lambda self: CollectionEnum.BATTLE.value)
    alternative_id = property(lambda self: None)
    populate_fields = property(
        lambda self: {
            'blue_team': {
                'id_key': 'blue_team',
                'model': CharacterModel()
            },
            'red_team': {
                'id_key': 'red_team',
                'model': CharacterModel()
            },
            'current_player': {
                'id_key': 'current_player',
                'model': CharacterModel()
            },
        }
    )

if __name__ == '__main__':
    from decouple import config

    MY_ID = config('MY_ID')
    OTHER_ID = config('OTHER_ID')

    character_model = CharacterModel()
    battle_model = BattleModel()
    blue_char = character_model.get(MY_ID)
    red_char = character_model.get(OTHER_ID)
    battle = Battle(
        blue_team=blue_char,
        red_team=red_char,
        chat_id=-987654321,
        _id='ffffffffffffffffffffffff'
    )
    print(f'battle: {battle}')
    battle_model.save(battle)
    battle2 = battle_model.get('ffffffffffffffffffffffff')
    print(f'battle2: {battle2}')