from itertools import chain
from typing import Any, Dict, Iterable, List, Tuple, Union

from rpgram.characters.char_base import BaseCharacter
from rpgram.enums.damage import DamageEnum
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import SkillTypeEnum, TargetEnum
from rpgram.enums.stats_base import BaseStatsEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.errors import SkillRequirementError


STATS_ENUM_TYPES = (BaseStatsEnum, CombatStatsEnum)
STATS_MULTIPLIER_TYPES = Union[BaseStatsEnum, CombatStatsEnum, str]
ITER_MULTIPLIERS_TYPE = Iterable[
    Tuple[
        Union[
            BaseStatsEnum,
            CombatStatsEnum
        ],
        float
    ]
]


class BaseSkill:
    def __init__(
        self,
        name: str,
        description: str,
        level: int,
        cost: int,
        base_stats_multiplier: Dict[Union[str, BaseStatsEnum], float],
        combat_stats_multiplier: Dict[Union[str, CombatStatsEnum], float],
        target_type: TargetEnum,
        skill_type: SkillTypeEnum,
        char: BaseCharacter,
        requirements: Dict[str, Any] = {},
        damage_types: List[Union[str, DamageEnum]] = None,
    ):
        self.base_stats_multiplier = {}
        for attribute, value in base_stats_multiplier.items():
            if isinstance(attribute, str):
                attribute = BaseStatsEnum[attribute]
            if not isinstance(attribute, BaseStatsEnum):
                raise TypeError(
                    f'Os atributos (chaves) de base_stats_multiplier '
                    f'precisam ser uma string ou BaseStatsEnum.'
                    f'"{type(attribute)}" não é válido.'
                )
            if not isinstance(value, float):
                raise TypeError(
                    f'Os multiplicadores (valores) de base_stats_multiplier '
                    f'precisam ser um float.'
                    f'"{type(value)}" não é válido.'
                )
            self.base_stats_multiplier[attribute] = round(value, 2)

        self.combat_stats_multiplier = {}
        for attribute, value in combat_stats_multiplier.items():
            if isinstance(attribute, str):
                attribute = CombatStatsEnum[attribute]
            if not isinstance(attribute, CombatStatsEnum):
                raise TypeError(
                    f'Os atributos (chaves) de combat_stats_multiplier '
                    f'precisam ser uma string ou CombatStatsEnum.'
                    f'"{type(attribute)}" não é válido.'
                )
            if not isinstance(value, float):
                raise TypeError(
                    f'Os multiplicadores (valores) de combat_stats_multiplier '
                    f'precisam ser um float.'
                    f'"{type(value)}" não é válido.'
                )
            self.combat_stats_multiplier[attribute] = value

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
        self.level = int(level)
        self.cost = int(cost)
        self.target_type = target_type
        self.skill_type = skill_type
        self.char = char
        self.base_stats = char.base_stats
        self.combat_stats = char.combat_stats
        self.equips = char.equips
        self.requirements = requirements
        self.damage_types = damage_types

        self.check_requirements()

    def check_requirements(self):
        errors = []
        for attribute, value in self.requirements.items():
            if value > self.base_stats[attribute]:
                errors.append(
                    f'    {attribute}: '
                    f'"{value}" ({self.base_stats[attribute]}).'
                )

        if errors:
            errors = "\n".join(errors)
            raise SkillRequirementError(
                f'Não foi possível aprender/usar a habilidade '
                f'"{self.name}".\n'
                f'O personagem não possui os requisitos:\n'
                f'{errors}'
            )

    def iter_multipliers(self) -> ITER_MULTIPLIERS_TYPE:
        return chain(
            self.base_stats_multiplier.items(),
            self.combat_stats_multiplier.items()
        )

    def format_attribute_name(self, attribute: STATS_MULTIPLIER_TYPES) -> str:
        if isinstance(attribute, STATS_ENUM_TYPES):
            attribute = attribute.name

        return attribute.replace('_', ' ').title()

    @property
    def power(self) -> int:
        power_point = 0
        for attribute, multiplier in self.iter_multipliers():
            power_point += self[attribute]

        return int(power_point)

    @property
    def powers_text(self) -> str:
        text_list = []

        for attribute, multiplier in self.iter_multipliers():
            attribute_value = self[attribute]
            attribute_percent = int(multiplier*100)
            attribute_emoji = EmojiEnum[attribute.name].value
            text_list.append(
                f'{attribute_value}'
                f'({attribute_percent}%{attribute_emoji})'
            )

        return ', '.join(text_list)

    def __getitem__(self, item: STATS_MULTIPLIER_TYPES) -> int:
        if isinstance(item, STATS_ENUM_TYPES):
            item = item.name

        item = item.upper()

        if item in BaseStatsEnum.__members__:
            bs_enum = BaseStatsEnum[item]
            return int(
                self.base_stats[item] *
                self.base_stats_multiplier[bs_enum]
            )
        elif item in CombatStatsEnum.__members__:
            cs_enum = CombatStatsEnum[item]
            return int(
                self.combat_stats[item] *
                self.combat_stats_multiplier[cs_enum]
            )
        else:
            raise KeyError(f'"{item}" não é um atributo válido.')
