from datetime import datetime
from typing import TYPE_CHECKING, List, Union

from bson import ObjectId
from rpgram.consumables.consumable import Consumable
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


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

    def function(self, target: 'BaseCharacter') -> dict:
        report_list = target.status.remove_conditions(*self.condition_target)
        report_list = [report['text'] for report in report_list]
        report_list = list(dict.fromkeys(report_list))
        report = {"text": "\n".join(report_list)}

        return report

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
        price = (base_value * cure_multiplier) - (rarity_multiplier * 10)
        if cure_multiplier >= 50:
            price /= 2

        return int(price)


class PanaceaConsumable(Consumable):
    def __init__(
        self,
        name: str,
        description: str,
        quantity_condition: int,
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

        self.quantity_condition = quantity_condition

    def function(self, target: 'BaseCharacter') -> dict:
        condition_target = []
        for condition in target.status.get_debuffs():
            condition_target.extend([condition.name] * self.quantity_condition)
        report_list = target.status.remove_conditions(*condition_target)
        report_list = [report['text'] for report in report_list]
        report_list = list(dict.fromkeys(report_list))
        report = {"text": "\n".join(report_list)}

        return report

    def to_dict(self):
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            weight=super_dict['weight'],
            quantity_condition=self.quantity_condition,
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
        base_value = 100
        cure_multiplier = self.quantity_condition
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = (base_value * cure_multiplier) + (rarity_multiplier * 25)

        return int(price)


if __name__ == '__main__':
    from rpgram.conditions.debuff import PoisoningCondition, SilenceCondition
    from rpgram import Status

    poisoning_name = PoisoningCondition().name
    cure_consumable = CureConsumable(
        name='Cure Consumable',
        description='Cure Description',
        condition_target=[poisoning_name]*5,
        weight=1.0,
    )
    panacea_consumable = PanaceaConsumable(
        name='Panacea Consumable',
        description='Panacea Description',
        quantity_condition=5,
        weight=1.0,
        rarity=RarityEnum.RARE.name,
    )

    class Target:
        status = Status(
            [PoisoningCondition(level=20), SilenceCondition(level=20)]
        )

    print(cure_consumable)
    print(cure_consumable.price)
    print(cure_consumable.to_dict())
    print(cure_consumable.use(Target()))

    print(panacea_consumable)
    print(panacea_consumable.price)
    print(panacea_consumable.to_dict())
    print(panacea_consumable.use(Target()))
