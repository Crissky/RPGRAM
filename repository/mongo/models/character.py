from repository.mongo import CollectionEnum
from repository.mongo import Model
from repository.mongo.models.classe import ClasseModel
from repository.mongo.models.race import RaceModel
from repository.mongo.models.equips import EquipsModel
from rpgram.characters import BaseCharacter, PlayerCharacter


class CharacterModel(Model):

    _class = property(lambda self: BaseCharacter)
    collection = property(lambda self: CollectionEnum.CHARACTERS.value)
    populate_fields = property(
        lambda self: {
            'classe': {
                'id_key': 'classe_name',
                'model': ClasseModel()
            },
            'race': {
                'id_key': 'race_name',
                'model': RaceModel()
            },
            'equips': {
                'id_key': 'equips_id',
                'model': EquipsModel()
            },
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
    char_model = CharacterModel()
    print('Collection:', char_model.collection)
    result = char_model.save(player_character)
    print('result:', result)
    player_character2 = char_model.get('ffffffffffffffffffffffff')
    print(player_character2)
