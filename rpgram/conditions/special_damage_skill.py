from datetime import datetime
from typing import Iterator, List, Union

from bson import ObjectId

from rpgram.conditions.buff import BuffCondition
from rpgram.enums.damage import DamageEnum
from rpgram.enums.turn import TurnEnum
from rpgram.skills.special_damage import SpecialDamage


class SpecialDamageSkillCondition(BuffCondition):

    def __init__(
        self,
        name: str,
        frequency: Union[str, TurnEnum],
        power: int,
        damage_types: List[Union[str, DamageEnum]],
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

        if isinstance(damage_types, (DamageEnum, str)):
            damage_types = [damage_types]
        for index, damage_type in enumerate(damage_types):
            if isinstance(damage_type, str):
                damage_type = DamageEnum[damage_type]
            if isinstance(damage_type, DamageEnum):
                damage_types[index] = damage_type
            else:
                raise ValueError(
                    f'damage_types precisa ser uma string ou DamageEnum ou '
                    f'uma lista de strings ou DamageEnums. '
                    f'"{type(damage_type)}" não é válido.'
                )

        self.__power = int(power)
        self.damage_types = damage_types

    @property
    def power(self) -> int:
        power_multiplier = 1 + (self.level / 10)
        power_multiplier = round(power_multiplier, 2)

        return int(self.__power * power_multiplier)

    @property
    def special_damage_iter(self) -> Iterator[SpecialDamage]:
        # Mesmo valor de condition_reducer em SpecialDamage
        condition_multiplier = 20
        base_damage = self.power
        for damage_type in self.damage_types:
            if base_damage > 0:
                yield SpecialDamage(
                    base_damage=base_damage,
                    damage_type=damage_type,
                    equipment_level=int(self.level * condition_multiplier),
                    is_skill=True
                )
            else:
                break

    def to_dict(self) -> dict:
        _dict = {'power': self.__power}
        _dict.update(super().to_dict())

        return _dict
