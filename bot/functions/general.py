from typing import Any

from repository.mongo import GroupModel, PlayerModel


def get_attribute_group_or_player(_id: Any, attribute: str):
    group_model = GroupModel()
    player_model = PlayerModel()
    value = group_model.get(_id=_id, fields=[attribute])

    if value and attribute in value:
        return value[attribute]
    elif (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]
