from repository.mongo import CollectionEnum
from repository.mongo import Model
from repository.mongo.models.classe import ClasseModel
from repository.mongo.models.race import RaceModel
from rpgram.characters import BaseCharacter


class BaseCharacterModel(Model):

    _class = property(lambda self: BaseCharacter)
    collection = property(lambda self: CollectionEnum.BASE_CHARS.value)
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
    classe_model = ClasseModel()
    race_model = RaceModel()
    guerreiro = classe_model.get('Guerreiro')
    elfo = race_model.get('Elfo')
    base_character = BaseCharacter(
        char_name='PERSONAGEM TESTE MODELO',
        classe=guerreiro,
        race=elfo,
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
    base_char_model = BaseCharacterModel()
    print(f'Collection: {base_char_model.collection}')
    result = base_char_model.save(base_character)
    print('result:', result)
    base_character2 = base_char_model.get('ffffffffffffffffffffffff')
    print(base_character2)
