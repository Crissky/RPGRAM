from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import Group


class GroupModel(Model):
    _class = property(lambda self: Group)
    collection = property(
        lambda self: CollectionEnum.GROUP.value
    )
    alternative_id = property(lambda self: 'chat_id')


if __name__ == '__main__':
    group = Group(
        name='GRUPO TESTE MODELO',
        chat_id=1234,
        _id='ffffffffffffffffffffffff',
    )
    group_model = GroupModel()
    print(f'Collection: {group_model.collection}')
    result = group_model.save(group)
    print('result:', result)
    group_config2 = group_model.get(1234)
    print('player2:', group_config2)
