from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import GroupConfiguration


class GroupConfigurationModel(Model):
    _class = property(lambda self: GroupConfiguration)
    collection = property(
        lambda self: CollectionEnum.GROUP_CONFIGURATIONS.value
    )
    alternative_id = property(lambda self: 'chat_id')


if __name__ == '__main__':
    group_config = GroupConfiguration(
        name='GRUPO TESTE MODELO',
        chat_id=1234,
        _id='ffffffffffffffffffffffff',
    )
    group_config_model = GroupConfigurationModel()
    print(f'Collection: {group_config_model.collection}')
    result = group_config_model.save(group_config)
    print('result:', result)
    group_config2 = group_config_model.get(1234)
    print('player2:', group_config2)
