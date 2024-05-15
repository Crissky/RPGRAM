from typing import Any

from function.date_time import get_brazil_time_now
from repository.mongo import GroupModel


def get_attribute_group(_id: Any, attribute: str):
    group_model = GroupModel()
    if (value := group_model.get(_id=_id, fields=[attribute])):
        return value[attribute]


def is_group_spawn_time(chat_id: int) -> bool:
    group_model = GroupModel()
    group = group_model.get(chat_id)
    spawn_start_time = group.spawn_start_time
    spawn_end_time = group.spawn_end_time
    now = get_brazil_time_now()
    is_spawn_time = now.hour >= spawn_start_time and now.hour < spawn_end_time

    return is_spawn_time
