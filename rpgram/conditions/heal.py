from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Iterable, Union

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
from rpgram.enums.consumable import (
    HealingConsumableEmojiEnum,
    HealingConsumableEnum
)
from rpgram.enums.turn import TurnEnum

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter

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
        name: Enum,
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
    def description(self) -> str:
        return f'Cura {self.power * self.turn} de HP em 5 Turnos.'

    def function(self, target: 'BaseCharacter') -> dict:
        remaining_heal = abs(self.power * self.turn)
        report = target.combat_stats.cure_hit_points(remaining_heal)
        self.last_turn()

        return report

    @property
    def name(self) -> str:
        return self.enum_name.value

    @property
    def emoji(self) -> str:
        return self.__emoji


class Heal1Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL1,
            power=MINOR_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL1.value,
        )


class Heal2Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL2,
            power=LIGHT_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL2.value,
        )


class Heal3Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL3,
            power=HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL3.value,
        )


class Heal4Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL4,
            power=GREATER_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL4.value,
        )


class Heal5Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL5,
            power=RARE_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL5.value,
        )


class Heal6Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL6,
            power=EPIC_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL6.value,
        )


class Heal7Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL7,
            power=LEGENDARY_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL7.value,
        )


class Heal8Condition(HealingCondition):

    def __init__(self, turn: int = 5, level: int = 1):
        super().__init__(
            name=HealingConsumableEnum.HEAL8,
            power=MYTHIC_HEALING_POTION_TURNPOWER,
            frequency=TurnEnum.START,
            turn=turn,
            level=1,
            emoji=HealingConsumableEmojiEnum.HEAL8.value,
        )

    @property
    def description(self) -> str:
        return f'Cura {self.power} de HP por Turno.'


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

    def __iter__(self) -> Iterable[HealingCondition]:
        for condition_class in self.__list:
            yield condition_class()


HEAL_STATUS: Iterable[HealingCondition] = HealStatus()


if __name__ == '__main__':
    from rpgram.conditions.factory import condition_factory

    print(Heal1Condition())
    print(Heal2Condition())
    print(Heal3Condition())
    print(Heal4Condition())
    print(Heal5Condition())
    print(Heal6Condition())
    print(Heal7Condition())
    print(Heal8Condition())

    for debuff in HEAL_STATUS:
        condition = debuff
        print(condition.to_dict())
        _dict = {**condition.to_dict()}
        assert condition_factory(**_dict) == condition
