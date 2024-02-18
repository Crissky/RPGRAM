from datetime import datetime
from typing import List, Union

from bson import ObjectId
from rpgram.consumables.consumable import Consumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum


class CureConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        condition_target: Union[List[str], str],
        weight: float,
        rarity: Union[str, RarityEnum] = RarityEnum.COMMON,
        usable: bool = True,
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=description,
            weight=weight,
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        if isinstance(condition_target, str):
            condition_target = [condition_target]

        self.condition_target = condition_target

    def function(self, target) -> dict:
        report_list = [
            target.status.remove_condition(condition_target)["text"]
            for condition_target in self.condition_target
        ]
        report_list = list(dict.fromkeys(report_list))
        report = {"text": "\n".join(report_list)}

        return report

    def battle_function(self, target) -> dict:
        return self.function(target)

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            weight=super_dict['weight'],
            condition_target=self.condition_target,
            rarity=super_dict['rarity'],
            usable=super_dict['usable'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )

    @property
    def emoji_type(self) -> str:
        return EmojiEnum.CURE_CONSUMABLE.value

    @property
    def price(self) -> int:
        base_value = 50
        cure_multiplier = max(len(self.condition_target), 1)
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = base_value * rarity_multiplier * cure_multiplier

        return int(price)


if __name__ == '__main__':
    from rpgram import Status
    cure_consumable = CureConsumable(
        name='Cure Consumable',
        description='Cure Description',
        condition_target=['Poison', 'Poison', 'Poison'],
        weight=1.0,
    )

    class Target:
        status = Status(player_id=1)

    print(cure_consumable)
    print(cure_consumable.to_dict())
    print(cure_consumable.use(Target()))
