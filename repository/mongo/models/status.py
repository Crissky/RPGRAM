from repository.mongo import CollectionEnum, Model
from repository.mongo.models.condition import ConditionModel

from rpgram import Status
from rpgram.boosters import Condition


class StatusModel(Model):
    _class = property(lambda self: Status)
    collection = property(lambda self: CollectionEnum.STATUS.value)
    populate_fields = property(
        lambda self: {
            'conditions': {
                'id_key': 'condition_ids',
                'model': ConditionModel(),
                'remakeclass': Condition,
            }
        }
    )

if __name__ == '__main__':
    conditions_model = ConditionModel()
    condition = conditions_model.get('ffffffffffffffffffffffff')
    status_model = StatusModel()
    status = Status(
        player_id=1,
        conditions=[condition],
        _id='ffffffffffffffffffffffff'
    )
    status_model.save(status)
    status2 = status_model.get('ffffffffffffffffffffffff')
    print('status2:\n', status2)
