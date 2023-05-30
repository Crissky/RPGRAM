from repository.mongo import Model
from repository.mongo import CollectionEnum
from repository.mongo import CharacterModel
from rpgram import Battle


class BattleModel(Model):
    _class = property(lambda self: Battle)
    collection = property(lambda self: CollectionEnum.BATTLE.value)
    populate_fields = property(
        lambda self: {
            'blue_team': {
                'id_key': 'classe_name',
                'model': CharacterModel()
            },
            'red_team': {
                'id_key': 'classe_name',
                'model': CharacterModel()
            },
            'current_player_turn': {
                'id_key': 'classe_name',
                'model': CharacterModel()
            },
        }
    )
