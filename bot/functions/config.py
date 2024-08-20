from typing import Any

from bot.functions.char import get_player_ids_from_group
from function.date_time import get_brazil_time_now
from repository.mongo import GroupModel
from rpgram.group import Group


def get_attribute_group(_id: Any, attribute: str):
    group_model = GroupModel()
    if (value := group_model.get(_id=_id, fields=[attribute])):
        return value[attribute]


def is_group_spawn_time(chat_id: int) -> bool:
    group_model = GroupModel()
    group: Group = group_model.get(chat_id)
    spawn_start_time = group.spawn_start_time
    spawn_end_time = group.spawn_end_time
    now = get_brazil_time_now()
    is_spawn_time = now.hour >= spawn_start_time and now.hour < spawn_end_time

    return is_spawn_time


def update_total_players(chat_id: int = None, group: Group = None):
    group_model = GroupModel()
    if isinstance(chat_id, int):
        group: Group = group_model.get(chat_id)
    elif isinstance(group, Group):
        chat_id = group.chat_id

    player_id_list = get_player_ids_from_group(chat_id=chat_id)
    total_players = len(player_id_list)
    if total_players != group.total_players:
        group.set_total_players(total_players=total_players)
        group_model.save(group)
