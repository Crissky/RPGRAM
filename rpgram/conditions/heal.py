from datetime import datetime
from typing import Union

from bson import ObjectId
from rpgram.conditions.condition import Condition
from rpgram.consumables.heal import (
    MINOR_HEALING_POTION_POWER,
    LIGHT_HEALING_POTION_POWER,
    HEALING_POTION_POWER,
    GREATER_HEALING_POTION_POWER,
    RARE_HEALING_POTION_POWER,
    EPIC_HEALING_POTION_POWER,
    LEGENDARY_HEALING_POTION_POWER,
)
from rpgram.enums.consumable import HealingConsumableEmojiEnum, HealingConsumableEnum
from rpgram.enums.turn import TurnEnum

MINOR_HEALING_POTION_TURNPOWER = MINOR_HEALING_POTION_POWER // 5
LIGHT_HEALING_POTION_TURNPOWER = LIGHT_HEALING_POTION_POWER // 5
HEALING_POTION_TURNPOWER = HEALING_POTION_POWER // 5
GREATER_HEALING_POTION_TURNPOWER = GREATER_HEALING_POTION_POWER // 5
RARE_HEALING_POTION_TURNPOWER = RARE_HEALING_POTION_POWER // 5
EPIC_HEALING_POTION_TURNPOWER = EPIC_HEALING_POTION_POWER // 5
LEGENDARY_HEALING_POTION_TURNPOWER = LEGENDARY_HEALING_POTION_POWER // 5
MYTHIC_HEALING_POTION_TURNPOWER = LEGENDARY_HEALING_POTION_TURNPOWER


class HealingCondition(Condition):
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        frequency: Union[str, TurnEnum],
        turn: int = 1,
        level: int = 1,
        emoji: str = '',
        _id: Union[str, ObjectId] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(
            name=name,
            description=description,
            function=None,
            battle_function=None,
            frequency=frequency,
            turn=turn,
            level=level,
            _id=_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.power = power
        self.__emoji = emoji

    @property
    def function(self) -> str:
        return (
            'remaining_heal = abs(self.power * self.turn);'
            'report = target.combat_stats.cure_hit_points(remaining_heal);'
            'self.last_turn()'
        )

    @property
    def battle_function(self) -> str:
        return (
            'report = target.combat_stats.cure_hit_points(self.power)'
        )
    
    @property
    def emoji(self) -> str:
        return self.__emoji

    def to_dict(self) -> dict:
        super_dict = super().to_dict()
        return dict(
            name=super_dict['name'],
            description=super_dict['description'],
            power=self.power,
            frequency=super_dict['frequency'],
            turn=super_dict['turn'],
            _id=super_dict['_id'],
            created_at=super_dict['created_at'],
            updated_at=super_dict['updated_at'],
        )


class Heal1Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL1.value,
            description=(
                f'Cura {MINOR_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=MINOR_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL1.value,
        )


class Heal2Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL2.value,
            description=(
                f'Cura {LIGHT_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=LIGHT_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL2.value,
        )


class Heal3Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL3.value,
            description=(
                f'Cura {HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL3.value,
        )


class Heal4Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL4.value,
            description=(
                f'Cura {GREATER_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=GREATER_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL4.value,
        )


class Heal5Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL5.value,
            description=(
                f'Cura {RARE_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=RARE_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL5.value,
        )


class Heal6Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL6.value,
            description=(
                f'Cura {EPIC_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=EPIC_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL6.value,
        )


class Heal7Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL7.value,
            description=(
                f'Cura {LEGENDARY_HEALING_POTION_POWER} de HP em 5 Turnos.'
            ),
            power=LEGENDARY_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL7.value,
        )


class Heal8Condition(HealingCondition):
    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL8.value,
            description=(
                f'Cura {MYTHIC_HEALING_POTION_TURNPOWER} de HP por Turno.'
            ),
            power=MYTHIC_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL8.value,
        )


class HealStatus:
    __list = [
        Heal1Condition,
        Heal2Condition,
        Heal3Condition,
        Heal4Condition,
        Heal5Condition,
        Heal6Condition,
        Heal7Condition,
        Heal8Condition,
    ]

    def __iter__(self):
        for condition_class in self.__list:
            yield condition_class()


HEALSTATUS = HealStatus()


if __name__ == '__main__':
    print(Heal1Condition())
    print(Heal1Condition().to_dict())
    print(Heal2Condition())
    print(Heal2Condition().to_dict())
    print(Heal3Condition())
    print(Heal3Condition().to_dict())
    print(Heal4Condition())
    print(Heal4Condition().to_dict())
    print(Heal5Condition())
    print(Heal5Condition().to_dict())
    print(Heal6Condition())
    print(Heal6Condition().to_dict())
    print(Heal7Condition())
    print(Heal7Condition().to_dict())
    print(Heal8Condition())
    print(Heal8Condition().to_dict())
