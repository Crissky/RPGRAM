from typing import Any, Dict, List, Union

from rpgram.enums.damage import DamageEnum
from rpgram.enums.skill import SkillTypeEnum, TargetEnum


class BaseSkill:
    def __init__(
        self,
        name: str,
        description: str,
        power: int,
        level: int,
        cost: int,
        target_type: TargetEnum,
        skill_type: SkillTypeEnum,
        requirements: Dict[str, Any] = {},
        damage_types: List[Union[str, DamageEnum]] = None,
    ):
        if isinstance(target_type, str):
            target_type = TargetEnum[target_type]
        if not isinstance(target_type, TargetEnum):
            raise TypeError(
                f'target_type precisa ser uma string ou TargetEnum.'
                f'"{type(target_type)}" não é válido.'
            )

        if isinstance(skill_type, str):
            skill_type = SkillTypeEnum[skill_type]
        if not isinstance(skill_type, SkillTypeEnum):
            raise TypeError(
                f'skill_type precisa ser uma string ou SkillTypeEnum.'
                f'"{type(skill_type)}" não é válido.'
            )

        if not isinstance(requirements, dict):
            raise TypeError(
                f'requirements precisa ser um dicionário.'
                f'"{type(requirements)}" não é válido.'
            )

        if isinstance(damage_types, (DamageEnum, str)):
            damage_types = [damage_types]
        if damage_types is not None:
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

        self.name = name
        self.description = description
        self.power = int(power)
        self.level = int(level)
        self.cost = int(cost)
        self.target_type = target_type
        self.skill_type = skill_type
        self.requirements = requirements
        self.damage_types = damage_types
