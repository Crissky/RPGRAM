from repository.mongo import Model
from repository.mongo.collection_enum import CollectionEnum
from rpgram.boosters import Condition


class ConditionModel(Model):
    _class = property(lambda self: Condition)
    collection = property(lambda self: CollectionEnum.CONDITION.value)
    alternative_id = property(lambda self: 'name')


if __name__ == '__main__':
    from rpgram.enums import TurnEnum
    condition = Condition(
        name='BURN TESTE',
        description='Queimaduras que reduzem a Constituição em 10%.',
        function='self.__multiplier_constitution = 0.9',
        battle_function='self.__multiplier_constitution = 0.9',
        frequency=TurnEnum.CONTINUOUS.name,
        _id='ffffffffffffffffffffffff'
    )
    print('CONDITION:', condition)
    conditions_model = ConditionModel()
    result = conditions_model.save(condition)
    print('result:', result)
    condition2 = conditions_model.get('ffffffffffffffffffffffff')
    print('CONDITION2:', condition2)
