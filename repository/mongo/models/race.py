from repository.mongo import Model
from repository.mongo import CollectionEnum
from rpgram.boosters import Race


class RaceModel(Model):
    _class = property(lambda self: Race)
    collection = property(lambda self: CollectionEnum.RACES.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    race = Race(
        name='HUMANO TESTE MODELO',
        description='HUMANO TESTE MODELO',
        _id='ffffffffffffffffffffffff',
        bonus_strength=10,
        bonus_dexterity=10,
        bonus_constitution=10,
        bonus_intelligence=10,
        bonus_wisdom=10,
        bonus_charisma=10,
        multiplier_strength=1,
        multiplier_dexterity=1.2,
        multiplier_constitution=1.3,
        multiplier_intelligence=1.4,
        multiplier_wisdom=1.5,
        multiplier_charisma=1.6,
    )
    race_model = RaceModel()
    print(f'Collection: {race_model.collection}')
    result = race_model.save(race)
    print('Result:', result)
    race2 = race_model.get('HUMANO TESTE MODELO')
    print('Race2:\n', race2)
