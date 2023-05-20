from repository.mongo import CollectionEnum
from repository.mongo import Model
from repository.mongo.models.classe import ClasseModel
from repository.mongo.models.race import RaceModel
from rpgram.characters import PlayerCharacter


class PlayerCharacterModel(Model):

    _class = property(lambda self: PlayerCharacter)
    collection = property(lambda self: CollectionEnum.PLAYER_CHARS.value)
    populate_fields = property(
        lambda self: {
            'classe': {
                'id_key': 'classe_name',
                'model': ClasseModel()
            },
            'race': {
                'id_key': 'race_name',
                'model': RaceModel()
            }
        }
    )


if __name__ == '__main__':
    from repository.mongo import ClasseModel, RaceModel
    classe = ClasseModel()
    race = RaceModel()
    barbaro = classe.get('Bárbaro')
    anao = race.get('Anão')
    player_character = PlayerCharacter(
        player_id=10,
        player_name='JOGADOR TESTE MODELO',
        char_name='PERSONAGEM JOGADOR TESTE MODELO',
        classe=barbaro,
        race=anao,
        level=21,
        xp=30,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        _id='ffffffffffffffffffffffff',
    )
    player_char_model = PlayerCharacterModel()
    print(f'Collection:', player_char_model.collection)
    result = player_char_model.save(player_character)
    print('result:', result)
    player_character2 = player_char_model.get('ffffffffffffffffffffffff')
    print(player_character2)
