from datetime import datetime
from typing import List, Union

from bson import ObjectId

from constants.text import SECTION_HEAD, TEXT_DELIMITER
from functions.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import Equipment
from rpgram.enums import EquipmentEnum
from rpgram.errors import EquipmentRequirementError
from rpgram.stats import BaseStats

if __name__ in ['__main__', 'equip']:
    from rpgram.enums import DamageEnum


class Equips:
    '''Classe responsável por armazenar os equipamentos do jogador'''

    def __init__(
        self,
        _id: Union[str, ObjectId] = None,
        helmet: Equipment = None,
        left_hand: Equipment = None,
        right_hand: Equipment = None,
        armor: Equipment = None,
        boots: Equipment = None,
        ring: Equipment = None,
        necklace: Equipment = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__id = _id

        self.__helmet = helmet
        self.__left_hand = left_hand
        self.__right_hand = right_hand
        self.__armor = armor
        self.__boots = boots
        self.__ring = ring
        self.__necklace = necklace

        self.__equipments_weight = 0
        self.__observers = []

        self.__created_at = created_at
        self.__updated_at = updated_at

        self.__update_stats()

    def equip(self, new_equipment: Equipment) -> List[Equipment]:
        equip_type = new_equipment.equip_type
        requirements = new_equipment.requirements
        old_equipments = []
        for attribute, value in requirements.items():
            if self.base_stats[attribute] < value:
                raise EquipmentRequirementError(
                    f'O personagem possui "{self.base_stats[attribute]}" '
                    f'pontos de "{attribute}" e o requerido é "{value}".'
                )

        if equip_type == EquipmentEnum.HELMET:
            if self.__helmet is not None:
                old_equipments.append(self.__helmet)
            self.__helmet = new_equipment
        elif equip_type == EquipmentEnum.ONE_HAND:
            if self.__left_hand is None:
                self.__left_hand = new_equipment
            elif self.__right_hand is None:
                self.__right_hand = new_equipment
            else:
                old_equipments.append(self.__left_hand)
                old_equipments.append(self.__right_hand)
                self.__left_hand = new_equipment
        elif equip_type == EquipmentEnum.TWO_HANDS:
            if self.__left_hand is not None:
                old_equipments.append(self.__left_hand)
            elif self.__right_hand is not None:
                old_equipments.append(self.__right_hand)
            self.__left_hand = new_equipment
            self.__right_hand = new_equipment
        elif equip_type == EquipmentEnum.ARMOR:
            if self.__armor is not None:
                old_equipments.append(self.__armor)
            self.__armor = new_equipment
        elif equip_type == EquipmentEnum.BOOTS:
            if self.__boots is not None:
                old_equipments.append(self.__boots)
            self.__boots = new_equipment
        elif equip_type == EquipmentEnum.RING:
            if self.__ring is not None:
                old_equipments.append(self.__ring)
            self.__ring = new_equipment
        elif equip_type == EquipmentEnum.NECKLACE:
            if self.__necklace is not None:
                old_equipments.append(self.__necklace)
            self.__necklace = new_equipment

        self.__update_stats()
        return old_equipments

    def unequip(self, equipment: Equipment) -> Equipment:
        equip_type = equipment.equip_type

        if self.helmet == equipment:
            equipment = self.__helmet
            self.__helmet = None
        elif self.left_hand == equipment:
            equipment = self.__left_hand
            self.__left_hand = None
        elif self.right_hand == equipment:
            equipment = self.__right_hand
            self.__right_hand = None
        elif self.armor == equipment:
            equipment = self.__armor
            self.__armor = None
        elif self.boots == equipment:
            equipment = self.__boots
            self.__boots = None
        elif self.ring == equipment:
            equipment = self.__ring
            self.__ring = None
        elif self.necklace == equipment:
            equipment = self.__necklace
            self.__necklace = None
        else:
            raise ValueError(f'"{equipment}" não está equipado.')

        if equip_type == EquipmentEnum.TWO_HANDS:
            self.__left_hand = None
            self.__right_hand = None

        self.__update_stats()
        return equipment

    def attach_observer(self, observer):
        self.__observers.append(observer)

    def detach_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

    def __update_stats(self):
        self.__equipments_weight = 0

        self.__bonus_strength = 0
        self.__bonus_dexterity = 0
        self.__bonus_constitution = 0
        self.__bonus_intelligence = 0
        self.__bonus_wisdom = 0
        self.__bonus_charisma = 0

        self.__multiplier_strength = 1
        self.__multiplier_dexterity = 1
        self.__multiplier_constitution = 1
        self.__multiplier_intelligence = 1
        self.__multiplier_wisdom = 1
        self.__multiplier_charisma = 1

        self.__bonus_hit_points = 0
        self.__bonus_initiative = 0
        self.__bonus_physical_attack = 0
        self.__bonus_precision_attack = 0
        self.__bonus_magical_attack = 0
        self.__bonus_physical_defense = 0
        self.__bonus_magical_defense = 0
        self.__bonus_hit = 0
        self.__bonus_evasion = 0

        if (
            self.left_hand is not None and
            self.left_hand.equip_type == EquipmentEnum.TWO_HANDS
        ):
            equips = [
                self.helmet, self.left_hand, self.armor,
                self.boots, self.ring, self.necklace
            ]
        else:
            equips = [
                self.helmet, self.left_hand, self.right_hand, self.armor,
                self.boots, self.ring, self.necklace
            ]
        equips = [e for e in equips if e is not None]
        for e in equips:
            self.__equipments_weight += float(e.weight)

            self.__bonus_strength += int(e.bonus_strength)
            self.__bonus_dexterity += int(e.bonus_dexterity)
            self.__bonus_constitution += int(e.bonus_constitution)
            self.__bonus_intelligence += int(e.bonus_intelligence)
            self.__bonus_wisdom += int(e.bonus_wisdom)
            self.__bonus_charisma += int(e.bonus_charisma)

            self.__multiplier_strength += e.multiplier_strength - 1.0
            self.__multiplier_dexterity += e.multiplier_dexterity - 1.0
            self.__multiplier_constitution += e.multiplier_constitution - 1.0
            self.__multiplier_intelligence += e.multiplier_intelligence - 1.0
            self.__multiplier_wisdom += e.multiplier_wisdom - 1.0
            self.__multiplier_charisma += e.multiplier_charisma - 1.0

            self.__bonus_hit_points += int(e.bonus_hit_points)
            self.__bonus_initiative += int(e.bonus_initiative)
            self.__bonus_physical_attack += int(e.bonus_physical_attack)
            self.__bonus_precision_attack += int(e.bonus_precision_attack)
            self.__bonus_magical_attack += int(e.bonus_magical_attack)
            self.__bonus_physical_defense += int(e.bonus_physical_defense)
            self.__bonus_magical_defense += int(e.bonus_magical_defense)
            self.__bonus_hit += int(e.bonus_hit)
            self.__bonus_evasion += int(e.bonus_evasion)

        self.notify_observers()

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = (
            f'*{SECTION_HEAD.format("EQUIPAMENTOS")}*\n'
            f'*Capacete*: {self.helmet.name if self.helmet else ""}\n'
            f'*Mão Esquerda*: {self.left_hand.name if self.left_hand else ""}\n'
            f'*Mão Direita*: {self.right_hand.name if self.right_hand else ""}\n'
            f'*Armadura*: {self.armor.name if self.armor else ""}\n'
            f'*Botas*: {self.boots.name if self.boots else ""}\n'
            f'*Anel*: {self.ring.name if self.ring else ""}\n'
            f'*Necklace*: {self.necklace.name if self.necklace else ""}\n'
            f'*Peso*: {self.equipments_weight:.2f}w\n\n'
        )

        if verbose:
            text += (
                f'*{SECTION_HEAD.format("BÔNUS E MULTIPLICADORES")}*\n'

                f'`FOR: {self.strength:+} '
                f'x({self.__multiplier_strength:+.2f})`\n'
                f'`DES: {self.dexterity:+} '
                f'x({self.__multiplier_dexterity:+.2f})`\n'
                f'`CON: {self.constitution:+} '
                f'x({self.__multiplier_constitution:+.2f})`\n'
                f'`INT: {self.intelligence:+} '
                f'x({self.__multiplier_intelligence:+.2f})`\n'
                f'`SAB: {self.wisdom:+} '
                f'x({self.__multiplier_wisdom:+.2f})`\n'
                f'`CAR: {self.charisma:+} '
                f'x({self.__multiplier_charisma:+.2f})`\n\n'

                f'`HP: {self.hp:+}`\n'
                f'`INICIATIVA: {self.initiative:+}`\n'
                f'`ATAQUE FÍSICO: {self.physical_attack:+}`\n'
                f'`ATAQUE DE PRECISÃO: {self.precision_attack:+}`\n'
                f'`ATAQUE MÁGICO: {self.magical_attack:+}`\n'
                f'`DEFESA FÍSICA: {self.physical_defense:+}`\n'
                f'`DEFESA MÁGICA: {self.magical_defense:+}`\n'
                f'`ACERTO: {self.hit:+}`\n'
                f'`EVASÃO: {self.evasion:+}`\n'
            )

        if not markdown:
            text = remove_bold(text)
            text = remove_code(text)
        else:
            text = escape_basic_markdown_v2(text)

        return text

    def get_all_sheets(
        self, verbose: bool = False, markdown: bool = False
    ) -> str:
        return self.get_sheet(verbose=verbose, markdown=markdown)

    def __repr__(self) -> str:
        return (
            f'{TEXT_DELIMITER}\n'
            f'{self.get_sheet(True)}'
            f'{TEXT_DELIMITER}'
        )

    def to_dict(self):
        return dict(
            _id=self.__id,
            helmet_id=self.__helmet._id if self.__helmet else None,
            left_hand_id=self.__left_hand._id if self.__left_hand else None,
            right_hand_id=self.__right_hand._id if self.__right_hand else None,
            armor_id=self.__armor._id if self.__armor else None,
            boots_id=self.__boots._id if self.__boots else None,
            ring_id=self.__ring._id if self.__ring else None,
            necklace_id=self.__necklace._id if self.__necklace else None,
            # observers=[o._id for o in self.__observers],
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    # Getters
    @property
    def base_stats(self):
        for observer in self.__observers:
            if isinstance(observer, BaseStats):
                return observer
        raise NameError('Não foi encontrado um observer do tipo BaseStats.')

    _id = property(lambda self: self.__id)
    helmet = property(lambda self: self.__helmet)
    left_hand = property(lambda self: self.__left_hand)
    right_hand = property(lambda self: self.__right_hand)
    armor = property(lambda self: self.__armor)
    boots = property(lambda self: self.__boots)
    ring = property(lambda self: self.__ring)
    necklace = property(lambda self: self.__necklace)
    equipments_weight = property(lambda self: self.__equipments_weight)

    strength = bonus_strength = property(
        fget=lambda self: self.__bonus_strength)
    dexterity = bonus_dexterity = property(
        fget=lambda self: self.__bonus_dexterity)
    constitution = bonus_constitution = property(
        fget=lambda self: self.__bonus_constitution)
    intelligence = bonus_intelligence = property(
        fget=lambda self: self.__bonus_intelligence)
    wisdom = bonus_wisdom = property(
        fget=lambda self: self.__bonus_wisdom)
    charisma = bonus_charisma = property(
        fget=lambda self: self.__bonus_charisma)
    multiplier_strength = property(
        fget=lambda self: self.__multiplier_strength)
    multiplier_dexterity = property(
        fget=lambda self: self.__multiplier_dexterity)
    multiplier_constitution = property(
        fget=lambda self: self.__multiplier_constitution)
    multiplier_intelligence = property(
        fget=lambda self: self.__multiplier_intelligence)
    multiplier_wisdom = property(
        fget=lambda self: self.__multiplier_wisdom)
    multiplier_charisma = property(
        fget=lambda self: self.__multiplier_charisma)
    hp = hit_points = bonus_hit_points = property(
        fget=lambda self: self.__bonus_hit_points)
    initiative = bonus_initiative = property(
        fget=lambda self: self.__bonus_initiative)
    physical_attack = bonus_physical_attack = property(
        fget=lambda self: self.__bonus_physical_attack)
    precision_attack = bonus_precision_attack = property(
        fget=lambda self: self.__bonus_precision_attack)
    magical_attack = bonus_magical_attack = property(
        fget=lambda self: self.__bonus_magical_attack)
    physical_defense = bonus_physical_defense = property(
        fget=lambda self: self.__bonus_physical_defense)
    magical_defense = bonus_magical_defense = property(
        fget=lambda self: self.__bonus_magical_defense)
    hit = bonus_hit = property(fget=lambda self: self.__bonus_hit)
    evasion = bonus_evasion = property(fget=lambda self: self.__bonus_evasion)


if __name__ == '__main__':
    equips = Equips()
    helmet = Equipment(
        name='Capacete de Aço',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        weight=10,
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipment(
        name='Espada Gigante de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    armor = Equipment(
        name='Armadura de Aço',
        equip_type=EquipmentEnum.ARMOR,
        damage_types=None,
        weight=60,
        bonus_physical_defense=80,
        bonus_evasion=-25,
    )
    boots = Equipment(
        name='Botas de Couro',
        equip_type=EquipmentEnum.BOOTS,
        damage_types=None,
        weight=10,
        bonus_physical_defense=10,
        bonus_magical_defense=10,
        bonus_evasion=30,
    )
    any_ring = Equipment(
        name='Algum Anel',
        equip_type=EquipmentEnum.RING,
        damage_types=None,
        weight=0.1,
        bonus_strength=100,
        bonus_dexterity=100,
        bonus_constitution=100,
        bonus_intelligence=100,
        bonus_wisdom=100,
        bonus_charisma=100,
        multiplier_strength=2,
        multiplier_dexterity=2,
        multiplier_constitution=2,
        multiplier_intelligence=2,
        multiplier_wisdom=2,
        multiplier_charisma=2,
        bonus_hit_points=1000,
        bonus_initiative=100,
        bonus_physical_attack=100,
        bonus_precision_attack=100,
        bonus_magical_attack=100,
        bonus_physical_defense=100,
        bonus_magical_defense=-100,
        bonus_hit=100,
        bonus_evasion=100,
    )
    necklace = Equipment(
        name='Colar Brilhante',
        equip_type=EquipmentEnum.NECKLACE,
        damage_types=None,
        weight=0.2,
        bonus_charisma=150,
    )

    equips.equip(helmet)
    equips.equip(sword)
    equips.equip(armor)
    equips.equip(boots)
    equips.equip(any_ring)
    equips.equip(necklace)
    print(equips)
    print(equips.to_dict())
