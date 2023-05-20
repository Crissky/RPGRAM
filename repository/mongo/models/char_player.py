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
    player_character = PlayerCharacter(
        player_id=10,
        player_name='JOGADOR TESTE MODELO',
        char_name='PERSONAGEM JOGADOR TESTE MODELO',
        _id='ffffffffffffffffffffffff',
        level=21,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='ANÃO TESTE MODELO',
        race_description='ANÃO TESTE DO JOGADOR TESTE MODELO',
        race_bonus_strength=10,
        race_bonus_dexterity=8,
        race_bonus_constitution=14,
        race_bonus_intelligence=10,
        race_bonus_wisdom=10,
        race_bonus_charisma=8,
        race_multiplier_strength=1.0,
        race_multiplier_dexterity=1.0,
        race_multiplier_constitution=1.4,
        race_multiplier_intelligence=1.0,
        race_multiplier_wisdom=1.0,
        race_multiplier_charisma=1.0,
        classe_name='BÁRBARO',
        classe_description='BÁRBARO TESTE DE JOGADOR TESTE MODELO',
        classe_bonus_strength=18,
        classe_bonus_dexterity=12,
        classe_bonus_constitution=15,
        classe_bonus_intelligence=5,
        classe_bonus_wisdom=5,
        classe_bonus_charisma=5,
        classe_multiplier_strength=2,
        classe_multiplier_dexterity=1.0,
        classe_multiplier_constitution=1.5,
        classe_multiplier_intelligence=0.5,
        classe_multiplier_wisdom=1,
        classe_multiplier_charisma=0.5,
    )
    player_char_model = PlayerCharacterModel()
    print(f'Collection:', player_char_model.collection)
    result = player_char_model.save(player_character)
    print('result:', result)
    player_character2 = player_char_model.get('ffffffffffffffffffffffff')
    print(player_character2)
