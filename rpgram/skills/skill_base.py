import re

from abc import abstractmethod
from itertools import chain
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Tuple,
    Union
)

from constant.text import TEXT_DELIMITER
from rpgram.conditions.condition import Condition
from rpgram.dice import Dice
from rpgram.enums.damage import DamageEnum
from rpgram.enums.emojis import EmojiEnum
from rpgram.enums.skill import SkillDefenseEnum, SkillTypeEnum, TargetEnum
from rpgram.enums.stats_base import BaseStatsEnum
from rpgram.enums.stats_combat import CombatStatsEnum
from rpgram.requirement import Requirement
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
    NAME: str = 'Base Skill'
    DESCRIPTION: str = 'Base Skill Classe'
    RANK: str = 'Base Rank'
    REQUIREMENT: Requirement = Requirement()

    def __init__(
        self,
        name: str,
        description: str,
        rank: int,
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
        requirements: Union[Requirement, Dict[str, Any]] = {},
        damage_types: List[Union[str, DamageEnum]] = None,
        condition_list: List[Condition] = [],
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

        if not isinstance(requirements, (dict, Requirement)):
            raise TypeError(
                f'requirements precisa ser um dicionário.'
                f'"{type(requirements)}" não é válido.'
            )
        elif isinstance(requirements, dict):
            requirements = Requirement(**requirements)

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

        for condition in condition_list:
            if not isinstance(condition, Condition):
                raise TypeError(
                    f'condition_list precisa ser uma lista de Condition.'
                    f'"{type(condition)}" não é válido.'
                )

        self.name = name
        self.description = description
        self.rank = int(rank)
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
        self.condition_list = condition_list

        self.requirements.check_requirements(
            character=self.char,
            level=self.level,
            rank=self.rank,
        )

    @abstractmethod
    def function(self, target: 'BaseCharacter') -> dict:
        ...

    @abstractmethod
    def battle_function(self, target: 'BaseCharacter') -> dict:
        ...

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
        # Mesmo valor de condition_reducer em SpecialDamage
        condition_multiplier = 20
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
                    equipment_level=int(self.level * condition_multiplier),
                    is_skill=True
                )
            else:
                break

    def attributes_power_texts(self) -> Iterable[str]:
        for attribute, multiplier in self.iter_multipliers():
            attribute_value = self[attribute]
            attribute_percent = int(multiplier*100*self.level_multiplier)
            attribute_emoji = EmojiEnum[attribute.name].value

            yield (
                f'    {attribute_emoji}{attribute_value}'
                f'({attribute_percent}%)'
            )

    def special_damage_texts(self) -> Iterable[str]:
        for special_damage in self.special_damage_iter:
            yield f'    {special_damage.help_emoji_text}'

    def add_level(self, value: int = 1) -> None:
        value = int(abs(value))
        self.level += value

    # GETTERS
    @property
    def rank_text(self) -> str:
        if self.rank == 0:
            return ''
        return f'{EmojiEnum.RANK.value}*Rank*: {self.rank}\n'

    @property
    def level_text(self) -> str:
        if self.level == 0:
            return ''
        return f'{EmojiEnum.LEVEL.value}*Nível*: {self.level}\n'

    @property
    def level_multiplier_dict(self) -> dict:
        return None

    @property
    def level_multiplier(self) -> float:
        if isinstance(self.level_multiplier_dict, dict):
            return self.level_multiplier_dict[self.level]
        else:
            level = max(0, (self.level - 1))
            return 1 + (level / 20)

    @property
    def hit_multiplier(self) -> float:
        return 1.0

    @property
    def hit(self) -> int:
        return int(self.combat_stats.hit * self.hit_multiplier)

    @property
    def hit_text(self) -> str:
        if any((
            self.hit == 0,
            self.target_type == TargetEnum.SELF,
            self.skill_type != SkillTypeEnum.ATTACK
        )):
            return ''
        hit_percent = int(self.hit_multiplier*100)
        return (
            f'{EmojiEnum.HIT2.value}*Acerto*: '
            f'{self.hit}({hit_percent}%{EmojiEnum.HIT.value})\n'
        )

    @property
    def power(self) -> int:
        power_point = 0
        for attribute, multiplier in self.iter_multipliers():
            power_point += self[attribute]

        return int(power_point)

    @property
    def power_text(self) -> str:
        if self.power == 0:
            return ''
        return f'{EmojiEnum.EQUIPMENT_POWER.value}*Poder*: {self.power}\n'

    @property
    def power_detail_text(self) -> str:
        if attributes_power_texts := self.attributes_power_text:
            attributes_power_texts = (
                f'{EmojiEnum.BASE_ATTRIBUTES.value}*Dano dos Atributos*:'
                f'\n{attributes_power_texts}\n'
            )

        if (special_damage_texts := self.special_damage_text):
            special_damage_texts = (
                f'{EmojiEnum.SPECIAL_DAMAGE.value}*Danos Especiais*:'
                f'\n{special_damage_texts}\n'
            )

        return (
            f'{attributes_power_texts}'
            f'{special_damage_texts}'
        )

    @property
    def is_true_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.TRUE

    @property
    def special_damage_text(self):
        return '\n'.join(self.special_damage_texts())

    @property
    def attributes_power_text(self):
        return '\n'.join(self.attributes_power_texts())

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
    def target_type_text(self) -> str:
        if self.target_type == TargetEnum.SELF:
            target_type = 'Si Mesmo'
        if self.target_type == TargetEnum.SINGLE:
            target_type = 'Único'
        if self.target_type == TargetEnum.TEAM:
            target_type = 'Equipe'
        if self.target_type == TargetEnum.ALL:
            target_type = 'Todes'

        return f'{EmojiEnum.TARGET_TYPE.value}*Tipo de Alvo*: {target_type}\n'

    @property
    def skill_type_text(self) -> str:
        if self.skill_type == SkillTypeEnum.ATTACK:
            skill_type = 'Ofensivo'
        if self.skill_type == SkillTypeEnum.DEFENSE:
            skill_type = 'Defensivo'
        if self.skill_type == SkillTypeEnum.HEALING:
            skill_type = 'Cura'

        return (
            f'{EmojiEnum.SKILL_TYPE.value}*Tipo de Habilidade*: '
            f'{skill_type}\n'
        )

    @property
    def skill_defense_text(self) -> str:
        if self.skill_defense == SkillDefenseEnum.PHYSICAL:
            emoji_text = EmojiEnum.PHYSICAL_ATTACK.value
            skill_defense = 'Físico'
        if self.skill_defense == SkillDefenseEnum.MAGICAL:
            emoji_text = EmojiEnum.MAGICAL_ATTACK.value
            skill_defense = 'Mágico'
        if self.skill_defense == SkillDefenseEnum.TRUE:
            emoji_text = EmojiEnum.SKILL_DEFENSE_TRUE.value
            skill_defense = 'Verdadeiro'
        if self.skill_defense == SkillDefenseEnum.NA:
            emoji_text = EmojiEnum.SKILL_DEFENSE_NA.value
            skill_defense = 'Nenhum'
            return ''

        return (
            f'{EmojiEnum.SKILL_DEFENSE.value}*Tipo de Dano*: '
            f'{emoji_text}{skill_defense}\n'
        )

    @property
    def description_text(self) -> str:
        return (
            f'*{self.name.upper()}*: {self.description}\n\n'
            f'{self.rank_text}'
            f'{self.level_text}'
            f'{self.power_text}'
            f'{self.hit_text}'
            f'{self.target_type_text}'
            f'{self.skill_type_text}'
            f'{self.skill_defense_text}'
            f'{self.power_detail_text}'
        )

    def to_dict(self) -> dict:
        return {
            'class_name': self.__class__.__name__,
            'level': self.level,
        }

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

    def __eq__(self, other):
        if isinstance(other, BaseSkill):
            return all((
                self.__class__ == other.__class__,
                self.name == other.name
            ))
        elif isinstance(other, str):
            return (
                self.name.upper() == other.upper()
                or self.__class__.__name__.upper() == other.upper()
            )
        return False

    def __hash__(self):
        return hash(self.name)

    def __repr__(self) -> str:
        special_damage_text = self.special_damage_text
        if special_damage_text:
            special_damage_text = re.sub(r'\s+', ' ', special_damage_text)
            special_damage_text = special_damage_text.strip()
            special_damage_text = f' + ({special_damage_text})'
        return (
            f'<{self.__class__.__name__}{self.level}-Power: '
            f'{self.power}{special_damage_text}>'
        )

    def __str__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.description_text}'
            f'{TEXT_DELIMITER}\n'
        )
