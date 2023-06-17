from datetime import datetime
from typing import Any, Dict, List, Union
from bson import ObjectId

from constants.text import TEXT_DELIMITER
from functions.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import StatsBooster
from rpgram.enums import EquipmentEnum, DamageEnum


class Equipment(StatsBooster):
    def __init__(
        self,
        name: str,
        equip_type: Union[str, EquipmentEnum],
        damage_types: List[Union[str, DamageEnum]],
        weight: float = 10,
        requirements: Dict[str, Any] = {},
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
            created_at=created_at,
            updated_at=updated_at
        )
        if isinstance(equip_type, str):
            equip_type = EquipmentEnum[equip_type]
        if isinstance(damage_types, str):
            damage_types = [DamageEnum[damage_types]]
        elif isinstance(damage_types, DamageEnum):
            damage_types = [damage_types]
        elif isinstance(damage_types, list):
            for index, damage_type in enumerate(damage_types):
                if isinstance(damage_type, str):
                    damage_type = DamageEnum[damage_type]
                damage_types[index] = damage_type

        self.__name = name
        self.__equip_type = equip_type
        self.__damage_types = damage_types
        self.__weight = weight
        self.__requirements = requirements

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        damage_types = '/'.join([d.value for d in self.damage_types])
        requirements = '\n'.join(
            [f'  {k}: {v}' for k, v in self.requirements.items()]
        )
        text = (
            f'*Equipamento*: {self.name}\n'
            f'*Tipo*: {self.equip_type.value}\n'
            f'*Tipo de Dano*: {damage_types}\n'
            f'*Peso*: {self.weight}\n'
            f'*Requisitos*:\n{requirements}\n'
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
        damage_types = [d.name for d in self.damage_types]
        _dict = dict(
            name=self.name,
            equip_type=self.equip_type.name,
            damage_types=damage_types,
            requirements=self.requirements,
            weight=self.weight,
        )
        _dict.update(super().to_dict())

        return _dict

    # Getters
    name = property(lambda self: self.__name)
    equip_type = property(lambda self: self.__equip_type)
    damage_types = property(lambda self: self.__damage_types)
    requirements = property(lambda self: self.__requirements)
    weight = property(lambda self: self.__weight)


if __name__ == '__main__':
    sword = Equipment(
        name='Espada de Aço',
        equip_type=EquipmentEnum.one_hand,
        damage_types=[DamageEnum.slashing, 'fire'],
        weight=15,
        requirements={'Nível': 1, 'FOR': 12},
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
    )
    print(sword)
    print(sword.to_dict())
