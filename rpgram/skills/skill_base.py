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
from rpgram.enums.skill import (
    SkillDefenseEmojiEnum,
    SkillDefenseEnum,
    SkillTypeEmojiEnum,
    SkillTypeEnum,
    TargetEmojiEnum,
    TargetEnum
)
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
    REQUIREMENTS: Requirement = Requirement()

    def __init__(
        self,
        name: str,
        description: str,
        rank: int,
        level: int,
        base_stats_multiplier: Dict[Union[str, BaseStatsEnum], float],
        combat_stats_multiplier: Dict[Union[str, CombatStatsEnum], float],
        target_type: Union[TargetEnum, str],
        skill_type: Union[SkillTypeEnum, str],
        skill_defense: Union[SkillDefenseEnum, str],
        char: 'BaseCharacter',
        cost: int = None,
        dice: Union[int, Tuple[int, float]] = 20,
        is_elusive: bool = False,
        use_equips_damage_types: bool = False,
        requirements: Union[Requirement, Dict[str, Any]] = None,
        damage_types: List[Union[str, DamageEnum]] = None,
        condition_list: List[Condition] = None,
    ):
        '''
        Args:
            name: Nome da habilidade
            description: Descrição da habilidade
            rank: Rank da habilidade
            level: Nível da habilidade
            base_stats_multiplier: Dicionário com os multiplicadores de
                atributos base
            combat_stats_multiplier: Dicionário com os multiplicadores de
                atributos de combate
            target_type: Tipo de alvo da habilidade
            skill_type: Tipo da habilidade (ataque, cura, etc)
            skill_defense: Tipo de defesa usada para defender a habilidade
            char: Personagem que possui a habilidade
            cost: Custo para usar da habilidade
            dice: Dado usado para rolar a habilidade
            is_elusive: Se False, a habilidade pode ser esquivado, 
                ineludível caso contrário.
            use_equips_damage_types: Se True, a habilidade usa os tipos de dano
                dos equipamentos do personagem
            requirements: Requisitos para usar a habilidade
            damage_types: Lista com os Tipos de Dano que a habilidade causa.
            condition_list: Não usado.
        '''

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

        if requirements is None:
            requirements = {}
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

        if condition_list is None:
            condition_list = []

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
        self.cost = int(cost) if cost is not None else int(rank + 1)
        self.target_type = target_type
        self.skill_type = skill_type
        self.skill_defense = skill_defense
        self.char = char
        self.base_stats = char.base_stats
        self.combat_stats = char.combat_stats
        self.equips = char.equips
        self.status = char.status
        self.dice: Dice = dice
        self.is_elusive = is_elusive
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

    def pre_hit_function(self, target: 'BaseCharacter') -> dict:
        return {'text': ''}

    def hit_function(
        self,
        target: 'BaseCharacter',
        damage: int,
        total_damage: int,
    ) -> dict:
        return {'text': ''}

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
            attribute_percent = int(
                round((multiplier + self.level_multiplier) * 100, 2)
            )
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
    def full_name(self) -> str:
        return (
            f'{self.skill_type_emoji}'
            f'{self.name}'
        )

    @property
    def full_name_and_inline_info(self) -> str:
        return (
            f'{self.full_name}'
            f'({self.rank_emoji}{self.rank}|{self.level_emoji}{self.level})'
        )

    @property
    def target_emoji(self) -> str:
        return TargetEmojiEnum[self.target_type.name].value

    @property
    def skill_type_emoji(self) -> str:
        return SkillTypeEmojiEnum[self.skill_type.name].value

    @property
    def skill_defense_emoji(self) -> str:
        return SkillDefenseEmojiEnum[self.skill_defense.name].value

    @property
    def rank_emoji(self):
        return EmojiEnum.RANK.value

    @property
    def rank_text(self) -> str:
        if self.rank == 0:
            return ''
        return f'{self.rank_emoji}*Rank*: {self.rank}\n'

    @property
    def level_text(self) -> str:
        if self.level == 0:
            return ''
        return f'{self.level_emoji}*Nível*: {self.level}\n'

    @property
    def level_emoji(self):
        return EmojiEnum.LEVEL.value

    @property
    def level_multiplier_dict(self) -> dict:
        return None

    @property
    def level_multiplier(self) -> float:
        if isinstance(self.level_multiplier_dict, dict):
            return self.level_multiplier_dict[self.level]
        else:
            divisor = 20
            if self.target_type == TargetEnum.TEAM:
                divisor = 40

            return (self.level_rank / divisor)

    @property
    def level_rank(self) -> int:
        level = max(1, int(self.level))
        rank = max(1, int(self.rank))
        level_rank = int(level * rank)

        return level_rank

    @property
    def cost_text(self) -> str:
        if self.cost == 0:
            return ''
        return f'{EmojiEnum.ACTION_POINTS.value}*Custo*: {self.cost}\n'

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
        elif self.is_elusive:
            return f'{EmojiEnum.HIT2.value}*Acerto*: Ineludível\n'

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

    # IS DAMAGE TYPE
    @property
    def is_physical_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.PHYSICAL

    @property
    def is_magical_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.MAGICAL

    @property
    def is_true_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.TRUE

    @property
    def is_na_damage(self) -> bool:
        return self.skill_defense == SkillDefenseEnum.NA

    # IS TARGET TYPE
    @property
    def is_self_target_skill(self) -> bool:
        return self.target_type == TargetEnum.SELF

    @property
    def is_single_target_skill(self) -> bool:
        return self.target_type == TargetEnum.SINGLE

    @property
    def is_team_target_skill(self) -> bool:
        return self.target_type == TargetEnum.TEAM

    @property
    def is_all_target_skill(self) -> bool:
        return self.target_type == TargetEnum.ALL

    # IS SKILL TYPE
    @property
    def is_attack_type_skill(self) -> bool:
        return self.skill_type == SkillTypeEnum.ATTACK

    @property
    def is_barrier_type_skill(self) -> bool:
        return self.skill_type == SkillTypeEnum.BARRIER

    @property
    def is_buff_type_skill(self) -> bool:
        return self.skill_type == SkillTypeEnum.BUFF

    @property
    def is_defense_type_skill(self) -> bool:
        return self.skill_type == SkillTypeEnum.DEFENSE

    @property
    def is_healing_type_skill(self) -> bool:
        return self.skill_type == SkillTypeEnum.HEALING

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
                self.equips.special_damage_iter,
                self.status.special_damage_iter,
            )

        return special_damage_iter

    @property
    def target_type_text(self) -> str:
        if self.target_type == TargetEnum.SELF:
            target_type = 'Si Mesmo'
        elif self.target_type == TargetEnum.SINGLE:
            target_type = 'Único'
        elif self.target_type == TargetEnum.TEAM:
            target_type = 'Equipe'
        elif self.target_type == TargetEnum.ALL:
            target_type = 'Todes'

        return (
            f'{EmojiEnum.TARGET_TYPE.value}*Tipo de Alvo*: '
            f'{self.target_emoji}{target_type}\n'
        )

    @property
    def skill_type_text(self) -> str:
        if self.skill_type == SkillTypeEnum.ATTACK:
            skill_type = 'Ofensivo'
        elif self.skill_type == SkillTypeEnum.BARRIER:
            skill_type = 'Barreira'
        elif self.skill_type == SkillTypeEnum.BUFF:
            skill_type = 'Fortalecimento'
        elif self.skill_type == SkillTypeEnum.DEFENSE:
            skill_type = 'Defensivo'
        elif self.skill_type == SkillTypeEnum.HEALING:
            skill_type = 'Cura'

        return (
            f'{EmojiEnum.SKILL_TYPE.value}*Tipo de Habilidade*: '
            f'{self.skill_type_emoji}{skill_type}\n'
        )

    @property
    def skill_defense_text(self) -> str:
        if self.skill_defense == SkillDefenseEnum.PHYSICAL:
            skill_defense = 'Físico'
        elif self.skill_defense == SkillDefenseEnum.MAGICAL:
            skill_defense = 'Mágico'
        elif self.skill_defense == SkillDefenseEnum.TRUE:
            skill_defense = 'Verdadeiro'
        elif self.skill_defense == SkillDefenseEnum.NA:
            skill_defense = 'Nenhum'
            return ''

        return (
            f'{EmojiEnum.SKILL_DEFENSE.value}*Tipo de Dano*: '
            f'{self.skill_defense_emoji}{skill_defense}\n'
        )

    @property
    def description_text(self) -> str:
        return (
            f'*{self.name.upper()}*: {self.description}\n\n'
            f'{self.rank_text}'
            f'{self.level_text}'
            f'{self.cost_text}'
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
            stats_value = self.base_stats_multiplier[bs_enum]
            sum_multiplier = round(stats_value + self.level_multiplier, 2)
            return int(self.base_stats[item] * sum_multiplier)
        elif item in CombatStatsEnum.__members__:
            cs_enum = CombatStatsEnum[item]
            stats_value = self.combat_stats_multiplier[cs_enum]
            sum_multiplier = round(stats_value + self.level_multiplier, 2)
            return int(self.combat_stats[item] * sum_multiplier)
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
            f'{self.__class__.__name__}{self.level}('
            f'Power: {self.power}{special_damage_text}'
            f')'
        )

    def __str__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.description_text}'
            f'{TEXT_DELIMITER}\n'
        )
