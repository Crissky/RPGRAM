from typing import Any

from repository.mongo import GroupModel, PlayerModel
from random import random


def get_attribute_group_or_player(_id: Any, attribute: str):
    group_model = GroupModel()
    player_model = PlayerModel()
    value = group_model.get(_id=_id, fields=[attribute])

    if value and attribute in value:
        return value[attribute]
    elif (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]

def activated_condition(condition_score: float = 0.5) -> bool:
    resist_score = random()
    return resist_score < condition_score
