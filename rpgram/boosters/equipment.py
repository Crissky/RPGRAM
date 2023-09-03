from datetime import datetime
from typing import Any, Dict, List, Union
from bson import ObjectId

from constant.text import SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import StatsBooster
from rpgram.enums import DamageEnum, EquipmentEnum, RarityEnum
from rpgram.enums import EmojiEnum


class Equipment(StatsBooster):
    def __init__(
        self,
        name: str,
        equip_type: Union[str, EquipmentEnum],
        damage_types: List[Union[str, DamageEnum]] = None,
        weight: float = 10,
        requirements: Dict[str, Any] = {},
        rarity: Union[RarityEnum, str] = 'COMMON',
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

        if isinstance(rarity, str):
            rarity = RarityEnum[rarity]

        self.__name = name
        self.__equip_type = equip_type
        self.__damage_types = damage_types
        self.__weight = weight
        self.__requirements = requirements
        self.__rarity = rarity

    def compare(self, other_equipment) -> str:
        if self.equip_type != other_equipment.equip_type:
            equip_hand = [EquipmentEnum.ONE_HAND, EquipmentEnum.TWO_HANDS]
            if (
                self.equip_type not in equip_hand or
                other_equipment.equip_type not in equip_hand
            ):
                raise TypeError(
                    f'Equipamentos são de tipos diferentes.'
                    f'("{self.equip_type.name}" e '
                    f'"{other_equipment.equip_type.name}")'
                )

        # DIFFs
        power_diff = (self.power - other_equipment.power)

        strength_diff = (self.strength - other_equipment.strength)
        dexterity_diff = (self.dexterity - other_equipment.dexterity)
        constitution_diff = (self.constitution - other_equipment.constitution)
        intelligence_diff = (self.intelligence - other_equipment.intelligence)
        wisdom_diff = (self.wisdom - other_equipment.wisdom)
        charisma_diff = (self.charisma - other_equipment.charisma)

        multiplier_strength_diff = (
            self.multiplier_strength - other_equipment.multiplier_strength
        )
        multiplier_dexterity_diff = (
            self.multiplier_dexterity - other_equipment.multiplier_dexterity
        )
        multiplier_constitution_diff = (
            self.multiplier_constitution -
            other_equipment.multiplier_constitution
        )
        multiplier_intelligence_diff = (
            self.multiplier_intelligence -
            other_equipment.multiplier_intelligence
        )
        multiplier_wisdom_diff = (
            self.multiplier_wisdom - other_equipment.multiplier_wisdom
        )
        multiplier_charisma_diff = (
            self.multiplier_charisma - other_equipment.multiplier_charisma
        )

        hp_diff = (self.hp - other_equipment.hp)
        initiative_diff = (self.initiative - other_equipment.initiative)
        physical_attack_diff = (
            self.physical_attack - other_equipment.physical_attack
        )
        precision_attack_diff = (
            self.precision_attack - other_equipment.precision_attack
        )
        magical_attack_diff = (
            self.magical_attack - other_equipment.magical_attack
        )
        physical_defense_diff = (
            self.physical_defense - other_equipment.physical_defense
        )
        magical_defense_diff = (
            self.magical_defense - other_equipment.magical_defense
        )
        hit_diff = (self.hit - other_equipment.hit)
        evasion_diff = (self.evasion - other_equipment.evasion)

        damage_types = self.sheet_damage_types()
        power_multiplier = self.sheet_power_multiplier()
        requirements = self.sheet_requirements()

        text = (
            f'*Equipamento*: {self.name}\n'
            f'*Tipo*: {self.equip_type.value}\n'
            f'{damage_types}'
            f'*Poder*: {self.power}{EmojiEnum.EQUIPMENT_POWER.value} '
            f'{{{power_diff:+}}}{power_multiplier}\n'
            f'*Peso*: {self.weight:.2f}w\n'
            f'{requirements}'
        )
        text += (
            f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

            f'`FOR: {self.strength:+} {{{strength_diff:+}}}'
            f' x({self.multiplier_strength:+.2f} '
            f'{{{multiplier_strength_diff:+.2f}}})`\n'

            f'`DES: {self.dexterity:+} {{{dexterity_diff:+}}}'
            f' x({self.multiplier_dexterity:+.2f} '
            f'{{{multiplier_dexterity_diff:+.2f}}})`\n'

            f'`CON: {self.constitution:+} {{{constitution_diff:+}}}'
            f' x({self.multiplier_constitution:+.2f} '
            f'{{{multiplier_constitution_diff:+.2f}}})`\n'

            f'`INT: {self.intelligence:+} {{{intelligence_diff:+}}}'
            f' x({self.multiplier_intelligence:+.2f} '
            f'{{{multiplier_intelligence_diff:+.2f}}})`\n'

            f'`SAB: {self.wisdom:+} {{{wisdom_diff:+}}}'
            f' x({self.multiplier_wisdom:+.2f} '
            f'{{{multiplier_wisdom_diff:+.2f}}})`\n'

            f'`CAR: {self.charisma:+} {{{charisma_diff:+}}}'
            f' x({self.multiplier_charisma:+.2f} '
            f'{{{multiplier_charisma_diff:+.2f}}})`\n\n'

            f'`HP: {self.hp:+} '
            f'{{{hp_diff:+}}}`\n'
            f'`INICIATIVA: {self.initiative:+} '
            f'{{{initiative_diff:+}}}`\n'
            f'`ATAQUE FÍSICO: {self.physical_attack:+} '
            f'{{{physical_attack_diff:+}}}`\n'
            f'`ATAQUE DE PRECISÃO: {self.precision_attack:+} '
            f'{{{precision_attack_diff:+}}}`\n'
            f'`ATAQUE MÁGICO: {self.magical_attack:+} '
            f'{{{magical_attack_diff:+}}}`\n'
            f'`DEFESA FÍSICA: {self.physical_defense:+} '
            f'{{{physical_defense_diff:+}}}`\n'
            f'`DEFESA MÁGICA: {self.magical_defense:+} '
            f'{{{magical_defense_diff:+}}}`\n'
            f'`ACERTO: {self.hit:+} '
            f'{{{hit_diff:+}}}`\n'
            f'`EVASÃO: {self.evasion:+} '
            f'{{{evasion_diff:+}}}`\n'
        )

        return escape_basic_markdown_v2(text)

    def sheet_damage_types(self):
        damage_types = ''
        if self.damage_types:
            damage_types = '/'.join([d.value for d in self.damage_types])
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
            requirements = f'*Requisitos*:\n{requirements}\n\n'
        return requirements

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        damage_types = self.sheet_damage_types()
        power_multiplier = self.sheet_power_multiplier()
        requirements = self.sheet_requirements()

        text = (
            f'*Equipamento*: {self.name}\n'
            f'*Tipo*: {self.equip_type.value}\n'
            f'{damage_types}'
            f'*Poder*: {self.power}{EmojiEnum.EQUIPMENT_POWER.value} '
            f'{power_multiplier}\n'
            f'*Peso*: {self.weight:.2f}w\n'
            f'{requirements}'
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
        )
        _dict.update(super().to_dict())

        return _dict

    def __eq__(self, other):
        if isinstance(other, Equipment):
            return self._id == other._id
        return False

    # Getters
    @property
    def power(self) -> int:
        return (
            (self.bonus_strength * 7) +
            (self.bonus_dexterity * 10) +
            (self.bonus_constitution * 13) +
            (self.bonus_intelligence * 3) +
            (self.bonus_wisdom * 7) +
            (self.bonus_charisma * 3) +
            sum([
                self.bonus_hit_points,
                self.bonus_initiative,
                self.bonus_physical_attack,
                self.bonus_precision_attack,
                self.bonus_magical_attack,
                self.bonus_physical_defense,
                self.bonus_magical_defense,
                self.bonus_hit,
                self.bonus_evasion,
            ])
        )

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

    name = property(lambda self: self.__name)
    equip_type = property(lambda self: self.__equip_type)
    damage_types = property(lambda self: self.__damage_types)
    requirements = property(lambda self: self.__requirements)
    weight = property(lambda self: self.__weight)


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
        damage_types=[DamageEnum.SLASHING, 'FIRE'],
        weight=15,
        requirements={'Nível': 10, 'FOR': 13},
        rarity='RARE',
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
