from typing import Any, List

from repository.mongo import PlayerModel


def get_player_attribute_by_id(_id: Any, attribute: str) -> Any:
    player_model = PlayerModel()
    if (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]


def get_player_attribute_by_name(name: str, attribute: str) -> Any:
    player_model = PlayerModel()
    query = {'name': name}
    if (value := player_model.get(query=query, fields=[attribute])):
        return value[attribute]


def get_player_id_by_name(name: str) -> str:
    return get_player_attribute_by_name(name=name, attribute='player_id')


def get_player_name(_id: Any) -> str:
    return get_player_attribute_by_id(_id=_id, attribute='name')


def get_player_name_by_chat_id(chat_id: int, sort: bool = True) -> List[str]:
    player_model = PlayerModel()
    query = {'chat_ids': chat_id}
    fields = ['name']
    player_names = player_model.get_all(query=query, fields=fields)

    if sort:
        player_names.sort()

    if player_names:
        return player_names
