from repository.mongo import CollectionEnum
from repository.mongo import Model
from rpgram import GroupConfiguration


class GroupConfigurationModel(Model):
    _class = property(lambda s: GroupConfiguration)
    collection = property(lambda s: CollectionEnum.GROUP_CONFIGURATION.value)
    alternative_id = property(lambda s: 'chat_id')


if __name__ == '__main__':
    group_config = GroupConfiguration(
        'chat-1234', _id='ff0123456789ff0123456789'
    )
    group_config_model = GroupConfigurationModel()
    print(f'Collection: {group_config_model.collection}')
    result = group_config_model.save(group_config)
    print('result:', result)
    group_config2 = group_config_model.get('chat-1234')
    print('player2:', group_config2)
