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


def get_player_trocado(_id: Any) -> str:
    return get_player_attribute_by_id(_id=_id, attribute='trocado')


def get_players_attribute_by_chat_id(
    chat_id: int,
    attribute: str
) -> List[Any]:
    player_model = PlayerModel()
    query = {'chat_ids': chat_id}
    fields = [attribute]
    player_attributes = player_model.get_all(query=query, fields=fields)

    return player_attributes if player_attributes else []


def get_players_id_by_chat_id(chat_id: int) -> List[str]:
    player_ids = get_players_attribute_by_chat_id(
        chat_id=chat_id,
        attribute='player_id'
    )

    return player_ids


def get_players_name_by_chat_id(chat_id: int, sort: bool = True) -> List[str]:
    player_names = get_players_attribute_by_chat_id(
        chat_id=chat_id,
        attribute='name'
    )

    if sort:
        player_names.sort()

    return player_names


def player_is_in_chat(chat_id: int, player_id: int) -> bool:
    player_model = PlayerModel()
    query = {'chat_ids': chat_id, 'player_id': player_id}
    player: dict = player_model.get(query=query, fields=['_id'])

    return bool(player)
