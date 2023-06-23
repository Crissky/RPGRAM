from typing import Any

from repository.mongo import PlayerModel


def get_attribute_player(_id: Any, attribute: str):
    player_model = PlayerModel()
    if (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]
