from datetime import datetime
from typing import List, Union

from bson import ObjectId
from rpgram.consumables.consumable import Consumable
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
            function=None,
            battle_function=None,
            rarity=rarity,
            usable=usable,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        if isinstance(condition_target, str):
            condition_target = [condition_target]

        self.condition_target = condition_target

    @property
    def function(self) -> str:
        return (
            r'report_list = ['
            r'target.status.remove_condition(condition_target)["text"] '
            r'for condition_target in self.condition_target'
            r'];'
            r'report_list = set(report_list);'  # Retira msg duplicadas
            r'report = {"text": "\n".join(report_list)}'
        )

    @property
    def battle_function(self) -> None:
        return None

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
