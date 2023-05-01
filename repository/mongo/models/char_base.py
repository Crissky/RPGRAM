from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram.characters import BaseCharacter


class BaseCharacterModel(Model):

    _class = property(lambda self: BaseCharacter)
    collection = property(lambda self: CollectionEnum.BASE_CHARS.value)


if __name__ == '__main__':
    base_character = BaseCharacter(
        char_name='Personagem Teste',
        level=21,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        race_name='Elfo',
        race_description='Elfo Teste',
        race_bonus_strength=8,
        race_bonus_dexterity=12,
        race_bonus_constitution=8,
        race_bonus_intelligence=10,
        race_bonus_wisdom=12,
        race_bonus_charisma=10,
        race_multiplier_strength=1.0,
        race_multiplier_dexterity=1.0,
        race_multiplier_constitution=1.0,
        race_multiplier_intelligence=1.2,
        race_multiplier_wisdom=1.2,
        race_multiplier_charisma=1.0,
        classe_name='Arqueiro',
        classe_description='Arqueiro Teste',
        classe_bonus_strength=5,
        classe_bonus_dexterity=15,
        classe_bonus_constitution=10,
        classe_bonus_intelligence=10,
        classe_bonus_wisdom=10,
        classe_bonus_charisma=10,
        classe_multiplier_strength=1,
        classe_multiplier_dexterity=1.5,
        classe_multiplier_constitution=1,
        classe_multiplier_intelligence=1,
        classe_multiplier_wisdom=1,
        classe_multiplier_charisma=1,
    )
    base_char_model = BaseCharacterModel()
    print(f'Collection: {base_char_model.collection}')
    result = base_char_model.save(base_character)
    print('result:', result)
    _id = result.inserted_id
    print(f'_id: {_id}')
    base_character2 = base_char_model.get(_id)
    print(base_character2)
