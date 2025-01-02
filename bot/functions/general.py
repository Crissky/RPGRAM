from random import randint, random
from typing import Any

from repository.mongo import GroupModel, PlayerModel


def get_attribute_group_or_player(_id: Any, attribute: str):
    group_model = GroupModel()
    player_model = PlayerModel()
    value: dict = group_model.get(_id=_id, fields=[attribute])

    if value and attribute in value:
        return value[attribute]
    elif (value := player_model.get(_id=_id, fields=[attribute])):
        return value[attribute]


def luck_test(threshold_value: float = 0.5) -> bool:
    test_score = random()
    return test_score < threshold_value


def get_event_random_minutes(multiplier: int = 0):
    multiplier = int(multiplier)

    return randint(1 + (multiplier * 30), 10 + (multiplier * 30))


if __name__ == '__main__':
    print(luck_test())
    print(get_event_random_minutes())
