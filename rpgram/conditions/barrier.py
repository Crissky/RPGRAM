from datetime import datetime
from typing import Union

from bson import ObjectId
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.conditions.condition import Condition
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.turn import TurnEnum


class BarrierCondition(Condition):

    def __init__(
        self,
        name: str,
        frequency: Union[str, TurnEnum],
        power: int,
        damage: int = 0,
        turn: int = 1,
        level: int = 1,
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
        self.__power = power
        self.__damage = int(damage)

    def add_damage(self, value: int) -> int:
        value = int(abs(value))
        remaining_damage = 0
        if value > 0:
            print(f'Barreira recebeu {value} de Dano!!!', end=' ')
        if value > self.current_barrier_points:
            remaining_damage = value - self.current_barrier_points
        self.__damage += value
        if self.__damage > self.barrier_points:
            self.__damage = self.barrier_points
        print(f'BP: {self.show_bp}')

        return remaining_damage

    def damage_barrier_points(
        self,
        value: int,
        markdown: bool = False,
    ) -> dict:

        value = int(abs(value))
        old_bp = self.current_barrier_points
        old_show_bp = self.show_barrier_points
        remaining_damage = self.add_damage(value)
        new_bp = self.current_barrier_points
        new_show_bp = self.show_barrier_points
        absolute_damage = (old_bp - new_bp)
        text = f'*BP*: {old_show_bp} ››› {new_show_bp} (*{value}*).'

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return {
            'old_bp': old_bp,
            'old_show_bp': old_show_bp,
            'new_bp': new_bp,
            'new_show_bp': new_show_bp,
            'damage': value,
            'absolute_damage': absolute_damage,
            'action': 'DANO',
            'remaining_damage': remaining_damage,
            'text': text,
        }

    @property
    def barrier_points(self) -> int:
        return self.__power
    power = bp = barrier_points

    @property
    def current_barrier_points(self) -> int:
        return int(self.__power - self.__damage)
    current_bp = current_barrier_points

    @property
    def show_barrier_points(self) -> str:
        current_barrier_points = max(self.current_barrier_points, 0)
        alert_text = ''
        if self.current_barrier_points < 0:
            alert_text = EmojiEnum.UNDER_ZERO.value
        return f'{current_barrier_points}/{self.barrier_points}{alert_text}'
    show_bp = show_barrier_points
