from repository.mongo import CollectionEnum, Model

from rpgram import Status
from rpgram.conditions.debuff import BleedingCondition
from rpgram.conditions.factory import condition_factory


class StatusModel(Model):
    _class = property(lambda self: Status)
    collection = property(lambda self: CollectionEnum.STATUS.value)
    populate_fields = property(
        lambda self: {
            'conditions': {
                'id_key': 'condition_args',
                'factory': condition_factory,
            }
        }
    )

if __name__ == '__main__':
    
    condition = BleedingCondition()
    status_model = StatusModel()
    status = Status(
        player_id=1,
        _id='ffffffffffffffffffffffff'
    )
    status.add(condition)
    status.add(condition)
    status.add(condition)
    status_model.save(status)
    status2 = status_model.get('ffffffffffffffffffffffff')
    print('status2:\n', status2)
