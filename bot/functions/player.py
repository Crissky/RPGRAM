from typing import Any

from repository.mongo import PlayerModel


def get_attribute_player(_id: Any, attribute: str):
    player_model = PlayerModel()
    if (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]


def get_player_name_by_chat_id(chat_id: int):
    player_model = PlayerModel()
    query = {'chat_ids': chat_id}
    fields = ['name']
    player_names = player_model.get_all(query=query, fields=fields)

    if player_names:
        return player_names
