from typing import Any

from repository.mongo import GroupModel


def get_attribute_group(_id: Any, attribute: str):
    group_model = GroupModel()
    if (value := group_model.get(_id=_id, fields=[attribute])):
        return value[attribute]
