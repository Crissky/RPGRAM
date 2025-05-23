from datetime import datetime
from statistics import mean
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Union
from bson import ObjectId

from constant.text import SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code

from rpgram.boosters.stats_booster import StatsBooster
from rpgram.constants.text import (
    CHARISMA_EMOJI_TEXT,
    CONSTITUTION_EMOJI_TEXT,
    DEXTERITY_EMOJI_TEXT,
    EVASION_EMOJI_TEXT,
    HIT_EMOJI_TEXT,
    HIT_POINT_FULL_EMOJI_TEXT,
    INITIATIVE_EMOJI_TEXT,
    INTELLIGENCE_EMOJI_TEXT,
    MAGICAL_ATTACK_EMOJI_TEXT,
    MAGICAL_DEFENSE_EMOJI_TEXT,
    PHYSICAL_ATTACK_EMOJI_TEXT,
    PHYSICAL_DEFENSE_EMOJI_TEXT,
    PRECISION_ATTACK_EMOJI_TEXT,
    STRENGTH_EMOJI_TEXT,
    WISDOM_EMOJI_TEXT
)
from rpgram.enums.damage import DamageEnum
from rpgram.enums.equipment import EquipmentEnum
from rpgram.enums.function import get_enum_index
from rpgram.enums.rarity import RarityEnum
from rpgram.enums.emojis import EmojiEnum
from rpgram.stats.stats_combat import (
    EVASION_CHARISMA,
    EVASION_DEXTERITY,
    EVASION_INTELLIGENCE,
    EVASION_WISDOM,
    HIT_CHARISMA,
    HIT_DEXTERITY,
    HIT_INTELLIGENCE,
    HIT_POINTS_CONSTITUTION,
    HIT_POINTS_STRENGTH,
    HIT_WISDOM,
    INITIATIVE_CHARISMA,
    INITIATIVE_DEXTERITY,
    INITIATIVE_INTELLIGENCE,
    INITIATIVE_WISDOM,
    MAGICAL_ATTACK_INTELLIGENCE,
    MAGICAL_ATTACK_WISDOM,
    MAGICAL_DEFENSE_CONSTITUTION,
    MAGICAL_DEFENSE_INTELLIGENCE,
    MAGICAL_DEFENSE_WISDOM,
    PHYSICAL_ATTACK_DEXTERITY,
    PHYSICAL_ATTACK_STRENGTH,
    PHYSICAL_DEFENSE_CONSTITUTION,
    PHYSICAL_DEFENSE_DEXTERITY,
    PRECISION_ATTACK_DEXTERITY,
    PRECISION_ATTACK_STRENGTH
)

if TYPE_CHECKING:
    from rpgram.skills.special_damage import SpecialDamage


MULTIPLIER_BONUS_STRENGTH = sum([
    HIT_POINTS_STRENGTH,
    PHYSICAL_ATTACK_STRENGTH,
    PRECISION_ATTACK_STRENGTH,
])
MULTIPLIER_BONUS_DEXTERITY = sum([
    INITIATIVE_DEXTERITY,
    PHYSICAL_ATTACK_DEXTERITY,
    PRECISION_ATTACK_DEXTERITY,
    PHYSICAL_DEFENSE_DEXTERITY,
    HIT_DEXTERITY,
    EVASION_DEXTERITY,
])
MULTIPLIER_BONUS_CONSTITUTION = sum([
    HIT_POINTS_CONSTITUTION,
    PHYSICAL_DEFENSE_CONSTITUTION,
    MAGICAL_DEFENSE_CONSTITUTION,
])
MULTIPLIER_BONUS_INTELLIGENCE = sum([
    INITIATIVE_INTELLIGENCE,
    MAGICAL_ATTACK_INTELLIGENCE,
    MAGICAL_DEFENSE_INTELLIGENCE,
    HIT_INTELLIGENCE,
    EVASION_INTELLIGENCE,
])
MULTIPLIER_BONUS_WISDOM = sum([
    INITIATIVE_WISDOM,
    MAGICAL_ATTACK_WISDOM,
    MAGICAL_DEFENSE_WISDOM,
    HIT_WISDOM,
    EVASION_WISDOM,
])
MULTIPLIER_BONUS_CHARISMA = sum([
    INITIATIVE_CHARISMA,
    HIT_CHARISMA,
    EVASION_CHARISMA,
])


class Equipment(StatsBooster):
    MIN_HP_MULTIPLIER = 5
    MAX_HP_MULTIPLIER = 10
    AVG_HP_MULTIPLIER = mean([MIN_HP_MULTIPLIER, MAX_HP_MULTIPLIER])

    def __init__(
        self,
        name: str,
        equip_type: Union[str, EquipmentEnum],
        damage_types: List[Union[str, DamageEnum]] = None,
        weight: float = 10,
        requirements: Dict[str, Any] = None,
        rarity: Union[RarityEnum, str] = 'COMMON',
        material_level: int = None,
        _id: Union[str, ObjectId] = None,
        bonus_strength: int = 0,
        bonus_dexterity: int = 0,
        bonus_constitution: int = 0,
        bonus_intelligence: int = 0,
        bonus_wisdom: int = 0,
        bonus_charisma: int = 0,
        multiplier_strength: float = 1.0,
        multiplier_dexterity: float = 1.0,
        multiplier_constitution: float = 1.0,
        multiplier_intelligence: float = 1.0,
        multiplier_wisdom: float = 1.0,
        multiplier_charisma: float = 1.0,
        bonus_hit_points: int = 0,
        bonus_initiative: int = 0,
        bonus_physical_attack: int = 0,
        bonus_precision_attack: int = 0,
        bonus_magical_attack: int = 0,
        bonus_physical_defense: int = 0,
        bonus_magical_defense: int = 0,
        bonus_hit: int = 0,
        bonus_evasion: int = 0,
        secret_bonus_strength: int = 0,
        secret_bonus_dexterity: int = 0,
        secret_bonus_constitution: int = 0,
        secret_bonus_intelligence: int = 0,
        secret_bonus_wisdom: int = 0,
        secret_bonus_charisma: int = 0,
        secret_multiplier_strength: float = 0.0,
        secret_multiplier_dexterity: float = 0.0,
        secret_multiplier_constitution: float = 0.0,
        secret_multiplier_intelligence: float = 0.0,
        secret_multiplier_wisdom: float = 0.0,
        secret_multiplier_charisma: float = 0.0,
        secret_bonus_hit_points: int = 0,
        secret_bonus_initiative: int = 0,
        secret_bonus_physical_attack: int = 0,
        secret_bonus_precision_attack: int = 0,
        secret_bonus_magical_attack: int = 0,
        secret_bonus_physical_defense: int = 0,
        secret_bonus_magical_defense: int = 0,
        secret_bonus_hit: int = 0,
        secret_bonus_evasion: int = 0,
        identified: bool = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        super().__init__(
            _id=_id,
            bonus_strength=bonus_strength,
            bonus_dexterity=bonus_dexterity,
            bonus_constitution=bonus_constitution,
            bonus_intelligence=bonus_intelligence,
            bonus_wisdom=bonus_wisdom,
            bonus_charisma=bonus_charisma,
            bonus_hit_points=bonus_hit_points,
            bonus_initiative=bonus_initiative,
            multiplier_strength=multiplier_strength,
            multiplier_dexterity=multiplier_dexterity,
            multiplier_constitution=multiplier_constitution,
            multiplier_intelligence=multiplier_intelligence,
            multiplier_wisdom=multiplier_wisdom,
            multiplier_charisma=multiplier_charisma,
            bonus_physical_attack=bonus_physical_attack,
            bonus_precision_attack=bonus_precision_attack,
            bonus_magical_attack=bonus_magical_attack,
            bonus_physical_defense=bonus_physical_defense,
            bonus_magical_defense=bonus_magical_defense,
            bonus_hit=bonus_hit,
            bonus_evasion=bonus_evasion,
            secret_bonus_strength=secret_bonus_strength,
            secret_bonus_dexterity=secret_bonus_dexterity,
            secret_bonus_constitution=secret_bonus_constitution,
            secret_bonus_intelligence=secret_bonus_intelligence,
            secret_bonus_wisdom=secret_bonus_wisdom,
            secret_bonus_charisma=secret_bonus_charisma,
            secret_multiplier_strength=secret_multiplier_strength,
            secret_multiplier_dexterity=secret_multiplier_dexterity,
            secret_multiplier_constitution=secret_multiplier_constitution,
            secret_multiplier_intelligence=secret_multiplier_intelligence,
            secret_multiplier_wisdom=secret_multiplier_wisdom,
            secret_multiplier_charisma=secret_multiplier_charisma,
            secret_bonus_hit_points=secret_bonus_hit_points,
            secret_bonus_initiative=secret_bonus_initiative,
            secret_bonus_physical_attack=secret_bonus_physical_attack,
            secret_bonus_precision_attack=secret_bonus_precision_attack,
            secret_bonus_magical_attack=secret_bonus_magical_attack,
            secret_bonus_physical_defense=secret_bonus_physical_defense,
            secret_bonus_magical_defense=secret_bonus_magical_defense,
            secret_bonus_hit=secret_bonus_hit,
            secret_bonus_evasion=secret_bonus_evasion,
            identified=identified,
            created_at=created_at,
            updated_at=updated_at
        )
        if isinstance(equip_type, str):
            equip_type = EquipmentEnum[equip_type]
        elif not isinstance(equip_type, EquipmentEnum):
            raise ValueError(
                f'equip_type precisa ser uma string ou EquipmentEnum.'
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

        if requirements is None:
            requirements = {}
        if isinstance(rarity, str):
            rarity = RarityEnum[rarity]
        if not isinstance(rarity, RarityEnum):
            raise ValueError(
                f'rarity precisa ser uma string ou RarityEnum. '
                f'({type(rarity)})'
            )

        self.__name = name
        self.__equip_type = equip_type
        self.__damage_types = damage_types
        self.__weight = weight
        self.__requirements = requirements
        self.__rarity = rarity
        self.__material_level = material_level

    def compare(
        self,
        *others_equipment: List[StatsBooster],
        is_sell: bool = False,
    ) -> str:
        if isinstance(others_equipment, StatsBooster):
            others_equipment = [others_equipment]

        for other_equipment in others_equipment:
            if self.equip_type != other_equipment.equip_type:
                equips_hand = [EquipmentEnum.ONE_HAND, EquipmentEnum.TWO_HANDS]
                if (
                    self.equip_type not in equips_hand or
                    other_equipment.equip_type not in equips_hand
                ):
                    raise TypeError(
                        f'Equipamentos são de tipos diferentes.'
                        f'("{self.equip_type.name}" e '
                        f'"{other_equipment.equip_type.name}")'
                    )

        # DIFFs
        other_names = []
        other_power = 0
        other_rarity_level = 0
        other_material_level = 0
        other_strength = 0
        other_dexterity = 0
        other_constitution = 0
        other_intelligence = 0
        other_wisdom = 0
        other_charisma = 0
        other_multiplier_strength = 1
        other_multiplier_dexterity = 1
        other_multiplier_constitution = 1
        other_multiplier_intelligence = 1
        other_multiplier_wisdom = 1
        other_multiplier_charisma = 1
        other_hp = 0
        other_initiative = 0
        other_physical_attack = 0
        other_precision_attack = 0
        other_magical_attack = 0
        other_physical_defense = 0
        other_magical_defense = 0
        other_hit = 0
        other_evasion = 0

        for other_equipment in others_equipment:
            other_names.append(other_equipment.name_and_power)
            other_power += other_equipment.power
            other_rarity_level = max(
                other_rarity_level,
                other_equipment.rarity_level
            )
            other_material_level = max(
                other_material_level,
                other_equipment.material_level
            )
            other_strength += other_equipment.strength
            other_dexterity += other_equipment.dexterity
            other_constitution += other_equipment.constitution
            other_intelligence += other_equipment.intelligence
            other_wisdom += other_equipment.wisdom
            other_charisma += other_equipment.charisma
            other_multiplier_strength += (
                other_equipment.multiplier_strength - 1
            )
            other_multiplier_dexterity += (
                other_equipment.multiplier_dexterity - 1
            )
            other_multiplier_constitution += (
                other_equipment.multiplier_constitution - 1
            )
            other_multiplier_intelligence += (
                other_equipment.multiplier_intelligence - 1
            )
            other_multiplier_wisdom += (
                other_equipment.multiplier_wisdom - 1
            )
            other_multiplier_charisma += (
                other_equipment.multiplier_charisma - 1
            )
            other_hp += other_equipment.hp
            other_initiative += other_equipment.initiative
            other_physical_attack += other_equipment.physical_attack
            other_precision_attack += other_equipment.precision_attack
            other_magical_attack += other_equipment.magical_attack
            other_physical_defense += other_equipment.physical_defense
            other_magical_defense += other_equipment.magical_defense
            other_hit += other_equipment.hit
            other_evasion += other_equipment.evasion

        other_names = ' e '.join(other_names)
        rarity_level_diff = (self.rarity_level - other_rarity_level)
        material_level_diff = (self.material_level - other_material_level)
        power_diff = (self.power - other_power)

        strength_diff = (self.strength - other_strength)
        dexterity_diff = (self.dexterity - other_dexterity)
        constitution_diff = (self.constitution - other_constitution)
        intelligence_diff = (self.intelligence - other_intelligence)
        wisdom_diff = (self.wisdom - other_wisdom)
        charisma_diff = (self.charisma - other_charisma)

        multiplier_strength_diff = (
            self.multiplier_strength - other_multiplier_strength
        )
        multiplier_dexterity_diff = (
            self.multiplier_dexterity - other_multiplier_dexterity
        )
        multiplier_constitution_diff = (
            self.multiplier_constitution - other_multiplier_constitution
        )
        multiplier_intelligence_diff = (
            self.multiplier_intelligence - other_multiplier_intelligence
        )
        multiplier_wisdom_diff = (
            self.multiplier_wisdom - other_multiplier_wisdom
        )
        multiplier_charisma_diff = (
            self.multiplier_charisma - other_multiplier_charisma
        )

        hp_diff = (self.hp - other_hp)
        initiative_diff = (self.initiative - other_initiative)
        physical_attack_diff = (self.physical_attack - other_physical_attack)
        precision_attack_diff = (
            self.precision_attack - other_precision_attack
        )
        magical_attack_diff = (self.magical_attack - other_magical_attack)
        physical_defense_diff = (
            self.physical_defense - other_physical_defense
        )
        magical_defense_diff = (self.magical_defense - other_magical_defense)
        hit_diff = (self.hit - other_hit)
        evasion_diff = (self.evasion - other_evasion)

        damage_types = self.sheet_damage_types()
        power_multiplier = self.sheet_power_multiplier()
        requirements = self.sheet_requirements()
        special_damages = self.sheet_special_damages()

        type_icon = EmojiEnum[self.equip_type.name].value
        price_text = self.price_text if is_sell else self.sell_price_text
        text = (
            f'COMPARANDO COM: {other_names}\n\n'
            f'*Equipamento*: {self.name}\n'
            f'*Tipo*: {self.equip_type.value}{type_icon}\n'
            f'{damage_types}'
            f'*Raridade*: {self.rarity.value}\n'
            f'*Nível de Raridade*: {self.rarity_text} '
            f'{{{rarity_level_diff:+}}}\n'
            f'*Nível do Material*: {self.material_text} '
            f'{{{material_level_diff:+}}}\n'
            f'*Poder*: {self.power}{EmojiEnum.EQUIPMENT_POWER.value} '
            f'{{{power_diff:+}}}{power_multiplier}\n'
            f'*Valor*: {price_text}\n'
            f'*Peso*: {self.weight:.2f}{EmojiEnum.WEIGHT.value}\n'
            f'{requirements}'
            f'{special_damages}'
        )
        text += (
            f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

            f'`{STRENGTH_EMOJI_TEXT}: {self.strength:+} '
            f'{{{strength_diff:+}}}'
            f' x({self.multiplier_strength:+.2f}) '
            f'{{{multiplier_strength_diff:+.2f}}}`\n'

            f'`{DEXTERITY_EMOJI_TEXT}: {self.dexterity:+} '
            f'{{{dexterity_diff:+}}}'
            f' x({self.multiplier_dexterity:+.2f}) '
            f'{{{multiplier_dexterity_diff:+.2f}}}`\n'

            f'`{CONSTITUTION_EMOJI_TEXT}: {self.constitution:+} '
            f'{{{constitution_diff:+}}}'
            f' x({self.multiplier_constitution:+.2f}) '
            f'{{{multiplier_constitution_diff:+.2f}}}`\n'

            f'`{INTELLIGENCE_EMOJI_TEXT}: {self.intelligence:+} '
            f'{{{intelligence_diff:+}}}'
            f' x({self.multiplier_intelligence:+.2f}) '
            f'{{{multiplier_intelligence_diff:+.2f}}}`\n'

            f'`{WISDOM_EMOJI_TEXT}: {self.wisdom:+} '
            f'{{{wisdom_diff:+}}}'
            f' x({self.multiplier_wisdom:+.2f}) '
            f'{{{multiplier_wisdom_diff:+.2f}}}`\n'

            f'`{CHARISMA_EMOJI_TEXT}: {self.charisma:+} '
            f'{{{charisma_diff:+}}}'
            f' x({self.multiplier_charisma:+.2f}) '
            f'{{{multiplier_charisma_diff:+.2f}}}`\n\n'

            f'`{HIT_POINT_FULL_EMOJI_TEXT}: {self.hp:+} '
            f'{{{hp_diff:+}}}`\n'
            f'`{INITIATIVE_EMOJI_TEXT}: {self.initiative:+} '
            f'{{{initiative_diff:+}}}`\n'
            f'`{PHYSICAL_ATTACK_EMOJI_TEXT}: {self.physical_attack:+} '
            f'{{{physical_attack_diff:+}}}`\n'
            f'`{PRECISION_ATTACK_EMOJI_TEXT}: {self.precision_attack:+} '
            f'{{{precision_attack_diff:+}}}`\n'
            f'`{MAGICAL_ATTACK_EMOJI_TEXT}: {self.magical_attack:+} '
            f'{{{magical_attack_diff:+}}}`\n'
            f'`{PHYSICAL_DEFENSE_EMOJI_TEXT}: {self.physical_defense:+} '
            f'{{{physical_defense_diff:+}}}`\n'
            f'`{MAGICAL_DEFENSE_EMOJI_TEXT}: {self.magical_defense:+} '
            f'{{{magical_defense_diff:+}}}`\n'
            f'`{HIT_EMOJI_TEXT}: {self.hit:+} '
            f'{{{hit_diff:+}}}`\n'
            f'`{EVASION_EMOJI_TEXT}: {self.evasion:+} '
            f'{{{evasion_diff:+}}}`\n'
        )

        return escape_basic_markdown_v2(text)

    def sheet_damage_types(self):
        damage_types = ''
        if self.damage_types:
            damage_types = '/'.join(
                [d.value.title() for d in self.damage_types]
            )
            damage_types = f'*Tipo de Dano*: {damage_types}\n'
        return damage_types

    def sheet_power_multiplier(self):
        power_multiplier = ''
        if self.power_multiplier > 0:
            power_multiplier = f' +[x{self.power_multiplier:.2f}]'
        return power_multiplier

    def sheet_requirements(self):
        requirements = '\n'
        if self.__requirements:
            requirements = '\n'.join(
                [f'  {k}: {v}' for k, v in self.__requirements.items()]
            )
            requirements = f'*Requisitos*:\n{requirements}\n'
        return requirements

    def sheet_special_damages(self):
        special_damage_text = '\n'.join((
            f'    {special_damage.help_emoji_text}'
            for special_damage in self.special_damage_iter
        ))
        if special_damage_text:
            special_damage_text = f'*Dano Especial*:\n{special_damage_text}\n'
        special_damage_text += f'\n'

        return special_damage_text

    def get_sheet(
        self,
        verbose: bool = False,
        markdown: bool = False,
        is_sell: bool = False
    ) -> str:
        damage_types = self.sheet_damage_types()
        power_multiplier = self.sheet_power_multiplier()
        requirements = self.sheet_requirements()
        special_damages = self.sheet_special_damages()
        material_level = (
            self.material_text
            if self.material_level
            else 'Nível não identificado'
        )

        type_icon = EmojiEnum[self.equip_type.name].value
        price_text = self.price_text if is_sell else self.sell_price_text
        text = (
            f'*Equipamento*: {self.name}\n'
            f'*Tipo*: {self.name_type}{type_icon}\n'
            f'{damage_types}'
            f'*Raridade*: {self.rarity.value}\n'
            f'*Nível de Raridade*: {self.rarity_text}\n'
            f'*Nível do Material*: {material_level}\n'
            f'*Poder*: {self.power}{EmojiEnum.EQUIPMENT_POWER.value} '
            f'{power_multiplier}\n'
            f'*Valor*: {price_text}\n'
            f'*Peso*: {self.weight:.2f}{EmojiEnum.WEIGHT.value}\n'
            f'{requirements}'
            f'{special_damages}'
        )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        text += f'{super().get_sheet(verbose, markdown)}'

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}\n'
        )

    def to_dict(self):
        damage_types = None
        if self.__damage_types:
            damage_types = [d.name for d in self.__damage_types]
        _dict = dict(
            name=self.__name,
            equip_type=self.__equip_type.name,
            damage_types=damage_types,
            requirements=self.__requirements,
            weight=self.__weight,
            rarity=self.__rarity.name,
            material_level=self.__material_level,
        )
        _dict.update(super().to_dict())

        return _dict

    def __eq__(self, other):
        if isinstance(other, Equipment):
            if self._id is not None and other._id is not None:
                return self._id == other._id
        return False

    # Getters
    @property
    def power(self) -> int:
        return int(sum([
            (self.bonus_strength * MULTIPLIER_BONUS_STRENGTH),
            (self.bonus_dexterity * MULTIPLIER_BONUS_DEXTERITY),
            (self.bonus_constitution * MULTIPLIER_BONUS_CONSTITUTION),
            (self.bonus_intelligence * MULTIPLIER_BONUS_INTELLIGENCE),
            (self.bonus_wisdom * MULTIPLIER_BONUS_WISDOM),
            (self.bonus_charisma * MULTIPLIER_BONUS_CHARISMA),

            (self.bonus_hit_points / Equipment.AVG_HP_MULTIPLIER),
            self.bonus_initiative,
            self.bonus_physical_attack,
            self.bonus_precision_attack,
            self.bonus_magical_attack,
            self.bonus_physical_defense,
            self.bonus_magical_defense,
            self.bonus_hit,
            self.bonus_evasion,
        ]))

    @property
    def power_multiplier(self) -> float:
        return (
            self.multiplier_strength +
            self.multiplier_dexterity +
            self.multiplier_constitution +
            self.multiplier_intelligence +
            self.multiplier_wisdom +
            self.multiplier_charisma
        ) - 6

    @property
    def power_text(self) -> str:
        power_emoji = EmojiEnum.EQUIPMENT_POWER.value
        return f'{self.power}{power_emoji}'

    @property
    def name_type(self) -> str:
        return self.equip_type.value

    @property
    def emoji_type(self) -> str:
        name_type = self.equip_type.name
        emoji_type = EmojiEnum[name_type].value
        return emoji_type

    @property
    def emoji_name_type(self) -> str:
        return f'{self.emoji_type}{self.name_type}'

    @property
    def name_emoji_type(self) -> str:
        return f'{self.name_type}{self.emoji_type}'

    @property
    def power_and_type(self) -> str:
        emoji_type = self.emoji_type
        return f'{self.power_text}{emoji_type}'

    @property
    def level(self) -> int:
        level = self.requirements.get('level', 0)
        return level

    @property
    def level_text(self) -> str:
        level_emoji = EmojiEnum.EQUIPMENT_LEVEL.value
        return f'{self.level}{level_emoji}'

    @property
    def material_level(self) -> int:
        return self.__material_level or 0

    @property
    def material_text(self) -> str:
        material_emoji = EmojiEnum.EQUIPMENT_MATERIAL.value
        return f'{self.material_level}{material_emoji}'

    @property
    def power_and_level(self) -> str:
        return f'({self.power_text}|{self.level_text})'

    @property
    def power_and_level_and_material(self) -> str:
        return f'({self.power_text}|{self.level_text}|{self.material_text})'

    @property
    def name_and_power(self) -> str:
        return f'{self.name} ({self.power_text})'

    @property
    def name_power_type(self) -> str:
        return f'{self.name} ({self.power_and_type})'

    @property
    def name_power_level(self) -> str:
        return f'{self.name} {self.power_and_level}'

    @property
    def identifiable_tag(self) -> str:
        text = ''
        if self.identifiable:
            text = EmojiEnum.IDENTIFY.value
        return text

    @property
    def price(self) -> int:
        rarity_multiplier = get_enum_index(self.rarity) + 1
        price = self.power * rarity_multiplier * 5

        return int(price)

    @property
    def sell_price(self) -> int:
        return int(self.price / 10)

    @property
    def price_text(self) -> str:
        return f'{self.price}{EmojiEnum.TROCADO.value}'

    @property
    def sell_price_text(self) -> str:
        return f'{self.sell_price}{EmojiEnum.TROCADO.value}'

    @property
    def rarity_level(self) -> int:
        return get_enum_index(self.rarity) + 1

    @property
    def rarity_text(self) -> str:
        rarity_emoji = EmojiEnum.EQUIPMENT_RARITY.value
        return f'{self.rarity_level}{rarity_emoji}'

    @property
    def max_attack_value(self) -> int:
        special_damage_base_value = sum([
            max(self.physical_attack, 0),
            max(self.precision_attack, 0),
            max(self.magical_attack, 0),
            max(self.level, 0),
            1,
        ])

        return int(special_damage_base_value)

    @property
    def special_damage_iter(self) -> Iterator['SpecialDamage']:
        from rpgram.skills.special_damage import SpecialDamage

        damage_types = (
            self.damage_types
            if self.damage_types is not None
            else []
        )
        base_damage = self.max_attack_value
        for damage_type in damage_types:
            if base_damage > 0:
                yield SpecialDamage(
                    base_damage=base_damage,
                    damage_type=damage_type,
                    equipment_level=self.level,
                )
            else:
                break

    name: str = property(lambda self: self.identifiable_tag + self.__name)
    equip_type: EquipmentEnum = property(lambda self: self.__equip_type)
    damage_types: List[DamageEnum] = property(lambda self: self.__damage_types)
    weight: float = property(lambda self: self.__weight)
    requirements: dict = property(lambda self: self.__requirements)
    rarity: RarityEnum = property(lambda self: self.__rarity)


if __name__ == '__main__':
    sword = Equipment(
        name='Espada de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=[DamageEnum.SLASHING, 'FIRE'],
        weight=15,
        requirements={'Nível': 1, 'FOR': 12},
        rarity='RARE',
        _id='ffffffffffffffffffffffff',
        bonus_strength=0,
        bonus_dexterity=0,
        bonus_constitution=0,
        bonus_intelligence=0,
        bonus_wisdom=0,
        bonus_charisma=0,
        bonus_hit_points=0,
        bonus_initiative=0,
        bonus_physical_attack=30,
        bonus_precision_attack=0,
        bonus_magical_attack=0,
        bonus_physical_defense=0,
        bonus_magical_defense=0,
        bonus_hit=15,
        bonus_evasion=-0,
        secret_bonus_strength=10,
        secret_bonus_dexterity=10,
        secret_bonus_constitution=10,
        secret_bonus_intelligence=10,
        secret_bonus_wisdom=10,
        secret_bonus_charisma=10,
        secret_multiplier_strength=1,
        secret_multiplier_dexterity=1,
        secret_multiplier_constitution=1,
        secret_multiplier_intelligence=1,
        secret_multiplier_wisdom=1,
        secret_multiplier_charisma=1,
        secret_bonus_hit_points=100,
        secret_bonus_initiative=10,
        secret_bonus_physical_attack=10,
        secret_bonus_precision_attack=10,
        secret_bonus_magical_attack=10,
        secret_bonus_physical_defense=10,
        secret_bonus_magical_defense=10,
        secret_bonus_hit=10,
        secret_bonus_evasion=10,
        identified=True,
    )
    print(sword)
    print(sword.to_dict())

    sword = Equipment(
        name='Espada Comparativa de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=[DamageEnum.SLASHING, 'FIRE'],
        weight=15,
        requirements={'Nível': 10, 'FOR': 13},
        rarity='RARE',
        material_level=3,
        _id='ffffffffffffffffffffffff',
        bonus_strength=1,
        bonus_dexterity=2,
        bonus_constitution=3,
        bonus_intelligence=4,
        bonus_wisdom=5,
        bonus_charisma=6,
        bonus_hit_points=1,
        bonus_initiative=2,
        bonus_physical_attack=3,
        bonus_precision_attack=4,
        bonus_magical_attack=5,
        bonus_physical_defense=6,
        bonus_magical_defense=7,
        bonus_hit=8,
        bonus_evasion=9,
    )
    shield = Equipment(
        name='Escudo Comparativo de Madeira',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=[DamageEnum.HITTING, 'FIRE'],
        weight=15,
        requirements={'Nível': 10, 'FOR': 13},
        rarity='RARE',
        material_level=1,
        _id='ffffffffffffffffffffffff',
        bonus_strength=11,
        bonus_dexterity=12,
        bonus_constitution=13,
        bonus_intelligence=14,
        bonus_wisdom=15,
        bonus_charisma=16,
        bonus_hit_points=101,
        bonus_initiative=102,
        bonus_physical_attack=103,
        bonus_precision_attack=104,
        bonus_magical_attack=105,
        bonus_physical_defense=106,
        bonus_magical_defense=107,
        bonus_hit=108,
        bonus_evasion=109,
    )
    print('COMPARE:\n', sword.compare(shield))

    print('MULTIPLIER_BONUS_STRENGTH', MULTIPLIER_BONUS_STRENGTH)
    print('MULTIPLIER_BONUS_DEXTERITY', MULTIPLIER_BONUS_DEXTERITY)
    print('MULTIPLIER_BONUS_CONSTITUTION', MULTIPLIER_BONUS_CONSTITUTION)
    print('MULTIPLIER_BONUS_INTELLIGENCE', MULTIPLIER_BONUS_INTELLIGENCE)
    print('MULTIPLIER_BONUS_WISDOM', MULTIPLIER_BONUS_WISDOM)
    print('MULTIPLIER_BONUS_CHARISMA', MULTIPLIER_BONUS_CHARISMA)
