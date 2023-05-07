from repository.mongo import Model
from repository.mongo import CollectionEnum
from rpgram.boosters import Classe


class ClasseModel(Model):
    _class = property(lambda self: Classe)
    collection = property(lambda self: CollectionEnum.CLASSES.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    classe = Classe(
        name='CLÉRIGO TESTE MODELO',
        description='CLÉRIGO TESTE MODELO',
        _id='ffffffffffffffffffffffff',
        bonus_strength=5,
        bonus_dexterity=5,
        bonus_constitution=8,
        bonus_intelligence=10,
        bonus_wisdom=16,
        bonus_charisma=16,
        multiplier_strength=0.5,
        multiplier_dexterity=0.5,
        multiplier_constitution=1.0,
        multiplier_intelligence=1.0,
        multiplier_wisdom=1.8,
        multiplier_charisma=1.7,
    )
    classe_model = ClasseModel()
    print(f'Collection: {classe_model.collection}')
    result = classe_model.save(classe)
    print(f'Result: {result}')
    classe2 = classe_model.get('CLÉRIGO TESTE MODELO')
    print('Classe2:\n', classe2)
