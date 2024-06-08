from itertools import chain
from typing import TYPE_CHECKING, Any, Dict, Iterable, Iterator, List, Tuple, Union

from rpgram.dice import Dice
from rpgram.enums.damage import DamageEnum
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_base import BaseStatsEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.errors import SkillRequirementError
from rpgram.skills.special_damage import SpecialDamage

if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


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
        target_type: Union[TargetEnum, str],
        skill_type: Union[SkillTypeEnum, str],
        skill_defense: Union[SkillDefenseEnum, str],
        char: 'BaseCharacter',
        dice: Union[int, Tuple[int, float]] = 20,
        use_equips_damage_types: bool = False,
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

        if isinstance(skill_defense, str):
            skill_defense = SkillDefenseEnum[skill_defense]
        if not isinstance(skill_defense, SkillDefenseEnum):
            raise TypeError(
                f'skill_defense precisa ser uma string ou SkillDefenseEnum.'
                f'"{type(skill_defense)}" não é válido.'
            )

        if isinstance(dice, int):
            dice = (dice, None)
        dice = Dice(
            character=char,
            skill=self,
            faces=dice[0],
            base_multiplier=dice[1]
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
        self.skill_defense = skill_defense
        self.char = char
        self.base_stats = char.base_stats
        self.combat_stats = char.combat_stats
        self.equips = char.equips
        self.dice: Dice = dice
        self.use_equips_damage_types = use_equips_damage_types
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

    def __special_damage_iter(self) -> Iterator[SpecialDamage]:
        damage_types = (
            self.damage_types
            if self.damage_types is not None
            else []
        )
        base_damage = self.power
        for damage_type in damage_types:
            if base_damage > 0:
                yield SpecialDamage(
                    base_damage=base_damage,
                    damage_type=damage_type,
                    equipment_level=self.level,
                )
            else:
                break

    def attributes_power_texts(self) -> Iterable[str]:
        for attribute, multiplier in self.iter_multipliers():
            attribute_value = self[attribute]
            attribute_percent = int(multiplier*100)
            attribute_emoji = EmojiEnum[attribute.name].value

            yield (
                f'{attribute_value}'
                f'({attribute_percent}%{attribute_emoji})'
            )

    def special_damage_texts(self) -> Iterable[str]:
        for special_damage in self.special_damage_iter:
            yield special_damage.help_emoji_text

    # GETTERS
    @property
    def level_multiplier_dict(self) -> dict:
        return None

    @property
    def level_multiplier_default(self) -> float:
        return 1.0

    @property
    def level_multiplier(self) -> float:
        if (level_multiplier_dict := self.level_multiplier_dict) is not None:
            return level_multiplier_dict.get(
                self.level,
                self.level_multiplier_default
            )
        else:
            return 1 + (self.level / 20)

    @property
    def hit_multiplier(self) -> float:
        return 1.0

    @property
    def hit(self) -> int:
        return int(self.combat_stats.hit * self.hit_multiplier)

    @property
    def hit_text(self) -> str:
        hit_percent = self.hit_multiplier*100
        return f'Acerto: {self.hit}({hit_percent}%{EmojiEnum.HIT.value})'

    @property
    def power(self) -> int:
        power_point = 0
        for attribute, multiplier in self.iter_multipliers():
            power_point += self[attribute]

        return int(power_point)

    @property
    def powers_text(self) -> str:
        attributes_power_texts = (
            f'Dano dos Atributos: {self.attributes_power_text}'
        )

        if (special_damage_texts := self.special_damage_text):
            special_damage_texts = f'\nDanos Especiais: {special_damage_texts}'

        return (
            f'{attributes_power_texts}'
            f'{special_damage_texts}'
        )

    @property
    def is_true_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.TRUE

    @property
    def special_damage_text(self):
        return ', '.join(self.special_damage_texts())

    @property
    def attributes_power_text(self):
        return ', '.join(self.attributes_power_texts())

    @property
    def special_damage_iter(self) -> Iterable[SpecialDamage]:
        special_damage_iter = self.__special_damage_iter()
        if self.use_equips_damage_types:
            special_damage_iter = chain(
                special_damage_iter,
                self.equips.special_damage_iter
            )

        return special_damage_iter

    @property
    def description_text(self) -> str:
        return (
            f'{self.name}: {self.description}\n'
            f'{self.hit_text}\n'
            f'{self.powers_text}'
        )

    def __getitem__(self, item: STATS_MULTIPLIER_TYPES) -> int:
        if isinstance(item, STATS_ENUM_TYPES):
            item = item.name

        item = item.upper()

        if item in BaseStatsEnum.__members__:
            bs_enum = BaseStatsEnum[item]
            return int(
                self.base_stats[item] *
                self.base_stats_multiplier[bs_enum] *
                self.level_multiplier
            )
        elif item in CombatStatsEnum.__members__:
            cs_enum = CombatStatsEnum[item]
            return int(
                self.combat_stats[item] *
                self.combat_stats_multiplier[cs_enum] *
                self.level_multiplier
            )
        else:
            raise KeyError(f'"{item}" não é um atributo válido.')

    def __repr__(self) -> str:
        special_damage_text = self.special_damage_text
        if special_damage_text:
            special_damage_text = f' + ({special_damage_text})'
        return (
            f'<{self.__class__.__name__}-Power: '
            f'{self.power}{special_damage_text}>'
        )
