from datetime import datetime
from typing import List, Union

from bson import ObjectId

from constant.text import SECTION_HEAD, TEXT_DELIMITER
from function.text import escape_basic_markdown_v2, remove_bold, remove_code
from rpgram.boosters import Equipment
from rpgram.enums import EmojiEnum, EquipmentEnum
from rpgram.errors import EquipmentRequirementError
from rpgram.stats import BaseStats

if __name__ in ['__main__', 'equip']:
    from rpgram.enums import DamageEnum


class Equips:
    '''Classe responsável por armazenar os equipamentos do jogador'''

    def __init__(
        self,
        player_id: int,
        _id: Union[str, ObjectId] = None,
        helmet: Equipment = None,
        left_hand: Equipment = None,
        right_hand: Equipment = None,
        armor: Equipment = None,
        boots: Equipment = None,
        ring: Equipment = None,
        amulet: Equipment = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ) -> None:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        self.__player_id = player_id
        self.__id = _id

        self.__helmet = None
        self.__left_hand = None
        self.__right_hand = None
        self.__armor = None
        self.__boots = None
        self.__ring = None
        self.__amulet = None

        self.__equipments_weight = 0
        self.__observers = []

        self.__created_at = created_at
        self.__updated_at = updated_at

        self.__init = True

        if isinstance(helmet, Equipment):
            self.equip(helmet)
        if isinstance(left_hand, Equipment):
            self.equip(left_hand, 'LEFT')
        if isinstance(right_hand, Equipment):
            if right_hand.equip_type != EquipmentEnum.TWO_HANDS:
                self.equip(right_hand, 'RIGHT')
        if isinstance(armor, Equipment):
            self.equip(armor)
        if isinstance(boots, Equipment):
            self.equip(boots)
        if isinstance(ring, Equipment):
            self.equip(ring)
        if isinstance(amulet, Equipment):
            self.equip(amulet)

        self.__init = False

        self.__update_stats()

    def equip(
        self, new_equipment: Equipment, hand: str = None
    ) -> List[Equipment]:
        equip_type = new_equipment.equip_type
        requirements = new_equipment.requirements
        old_equipments = []
        errors = []
        if not self.__init:
            for attribute, value in requirements.items():
                if value > self.base_stats[attribute]:
                    errors.append(
                        f'    {attribute}: '
                        f'"{value}" ({self.base_stats[attribute]}).'
                    )

        if errors:
            errors = "\n".join(errors)
            raise EquipmentRequirementError(
                f'Não foi possível equipar o item "{new_equipment.name}".\n'
                f'O personagem não possui os requisitos:\n'
                f'{errors}'
            )

        if equip_type == EquipmentEnum.HELMET:
            if self.helmet is not None:
                old_equipments.append(self.helmet)
            self.__helmet = new_equipment
        elif equip_type == EquipmentEnum.ONE_HAND:
            if not isinstance(hand, str):
                raise ValueError(
                    f'É necessário indicar em qual das mãos o '
                    f'item será equipado usando "LEFT" ou "RIGHT".\n'
                    f'Valor de hand, "{hand}", não é uma string.'
                )

            if (
                self.right_hand and
                self.right_hand.equip_type == EquipmentEnum.TWO_HANDS
            ):
                old_equipments.append(self.right_hand)
                self.__right_hand = None
                self.__left_hand = None

            if hand.upper() in ['R', 'RIGHT']:
                if self.right_hand is not None:
                    old_equipments.append(self.right_hand)
                self.__right_hand = new_equipment
            elif hand.upper() in ['L', 'LEFT']:
                if self.left_hand is not None:
                    old_equipments.append(self.left_hand)
                self.__left_hand = new_equipment
            else:
                raise ValueError(
                    f'Valor de hand, "{hand}", não é uma string válida. '
                    f'Use LEFT ou RIGHT para a mão ESQUERDA ou DIREITA.'
                )

        elif equip_type == EquipmentEnum.TWO_HANDS:
            if (
                self.right_hand and
                self.right_hand.equip_type == EquipmentEnum.TWO_HANDS
            ):
                old_equipments.append(self.right_hand)
                self.__right_hand = None
                self.__left_hand = None

            if self.left_hand is not None:
                old_equipments.append(self.left_hand)
            if self.right_hand is not None:
                old_equipments.append(self.right_hand)
            self.__left_hand = new_equipment
            self.__right_hand = new_equipment
        elif equip_type == EquipmentEnum.ARMOR:
            if self.armor is not None:
                old_equipments.append(self.armor)
            self.__armor = new_equipment
        elif equip_type == EquipmentEnum.BOOTS:
            if self.boots is not None:
                old_equipments.append(self.boots)
            self.__boots = new_equipment
        elif equip_type == EquipmentEnum.RING:
            if self.ring is not None:
                old_equipments.append(self.ring)
            self.__ring = new_equipment
        elif equip_type == EquipmentEnum.AMULET:
            if self.amulet is not None:
                old_equipments.append(self.amulet)
            self.__amulet = new_equipment

        self.__update_stats()
        return old_equipments

    def unequip(self, equipment: Equipment) -> Equipment:
        equip_type = equipment.equip_type

        if self.helmet == equipment:
            equipment = self.helmet
            self.__helmet = None
        elif self.left_hand == equipment:
            equipment = self.left_hand
            self.__left_hand = None
        elif self.right_hand == equipment:
            equipment = self.right_hand
            self.__right_hand = None
        elif self.armor == equipment:
            equipment = self.armor
            self.__armor = None
        elif self.boots == equipment:
            equipment = self.boots
            self.__boots = None
        elif self.ring == equipment:
            equipment = self.ring
            self.__ring = None
        elif self.amulet == equipment:
            equipment = self.amulet
            self.__amulet = None
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

        equips = list(self)
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

    def compare(self, equipment: Equipment) -> str:
        other_equipment = []
        if equipment.equip_type == EquipmentEnum.HELMET:
            other_equipment.append(self.helmet)
        elif equipment.equip_type == EquipmentEnum.ONE_HAND:
            other_equipment.append(self.right_hand)
        elif equipment.equip_type == EquipmentEnum.TWO_HANDS:
            other_equipment.extend([self.right_hand, self.left_hand])
        elif equipment.equip_type == EquipmentEnum.ARMOR:
            other_equipment.append(self.armor)
        elif equipment.equip_type == EquipmentEnum.BOOTS:
            other_equipment.append(self.boots)
        elif equipment.equip_type == EquipmentEnum.RING:
            other_equipment.append(self.ring)
        elif equipment.equip_type == EquipmentEnum.AMULET:
            other_equipment.append(self.amulet)

        other_equipment = [e for e in other_equipment if e is not None]

        if not other_equipment:
            return equipment.get_sheet(True, True)
        else:
            return equipment.compare(*other_equipment)

    def get_sheet(self, verbose: bool = False, markdown: bool = False) -> str:
        text = (
            f'*{SECTION_HEAD.format("EQUIPAMENTOS")}*\n'
            f'*Poder*: {self.power:}{EmojiEnum.EQUIPMENT_POWER.value}\n'
            f'*Peso*: {self.equipments_weight:.2f}{EmojiEnum.WEIGHT.value}\n\n'

            f'*Capacete*: '
            f'{self.helmet.name_and_power if self.helmet else ""}\n'
            f'*Mão Esq.*: '
            f'{self.left_hand.name_and_power if self.left_hand else ""}\n'
            f'*Mão Dir.*: '
            f'{self.right_hand.name_and_power if self.right_hand else ""}\n'
            f'*Armadura*: '
            f'{self.armor.name_and_power if self.armor else ""}\n'
            f'*Botas*: '
            f'{self.boots.name_and_power if self.boots else ""}\n'
            f'*Anel*: '
            f'{self.ring.name_and_power if self.ring else ""}\n'
            f'*Amuleto*: '
            f'{self.amulet.name_and_power if self.amulet else ""}\n\n'
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
            player_id=self.__player_id,
            _id=self.__id,
            helmet_id=self.helmet._id if self.helmet else None,
            left_hand_id=self.left_hand._id if self.left_hand else None,
            right_hand_id=self.right_hand._id if self.right_hand else None,
            armor_id=self.armor._id if self.armor else None,
            boots_id=self.boots._id if self.boots else None,
            ring_id=self.ring._id if self.ring else None,
            amulet_id=self.amulet._id if self.amulet else None,
            # observers=[o._id for o in self.__observers],
            created_at=self.__created_at,
            updated_at=self.__updated_at,
        )

    def __iter__(self):
        equips = [
            self.helmet, self.left_hand, self.right_hand,
            self.armor, self.boots, self.ring, self.amulet
        ]
        if (
            self.right_hand and
            self.right_hand.equip_type == EquipmentEnum.TWO_HANDS
        ):
            equips.remove(self.right_hand)

        for equip in equips:
            if equip:
                yield equip

    # Getters
    @property
    def base_stats(self):
        for observer in self.__observers:
            if isinstance(observer, BaseStats):
                return observer
        raise NameError('Não foi encontrado um observer do tipo BaseStats.')

    @property
    def power(self):
        power = 0
        for equip in self:
            power += equip.power

        return power

    _id = property(lambda self: self.__id)
    helmet = property(lambda self: self.__helmet)
    left_hand = property(lambda self: self.__left_hand)
    right_hand = property(lambda self: self.__right_hand)
    armor = property(lambda self: self.__armor)
    boots = property(lambda self: self.__boots)
    ring = property(lambda self: self.__ring)
    amulet = property(lambda self: self.__amulet)
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
    helmet = Equipment(
        name='Capacete de Aço',
        equip_type=EquipmentEnum.HELMET,
        damage_types=None,
        weight=10,
        requirements={'level': 10},
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipment(
        name='Espada Gigante de Aço',
        equip_type=EquipmentEnum.TWO_HANDS,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=60,
        bonus_hit=15,
        bonus_evasion=-20,
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
    amulet = Equipment(
        name='Colar Brilhante',
        equip_type=EquipmentEnum.AMULET,
        damage_types=None,
        weight=0.2,
        bonus_charisma=150,
    )
    dagger = Equipment(
        name='Adaga de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=DamageEnum.SLASHING,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    shield = Equipment(
        name='Escudo de Aço',
        equip_type=EquipmentEnum.ONE_HAND,
        damage_types=DamageEnum.BLUDGEONING,
        weight=40,
        bonus_physical_defense=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )

    equips = Equips(player_id=123, helmet=helmet)
    equips.equip(sword)
    equips.equip(shield, 'LEFT')
    equips.equip(dagger, 'RIGHT')
    # equips.equip(dagger)
    equips.equip(armor)
    equips.equip(boots)
    equips.equip(any_ring)
    equips.equip(amulet)
    print(equips.compare(sword))
    print(equips.get_sheet(True))
    print(equips.to_dict())

    # Verificar se estar retornando os equipamentos certos 
    # ao trocar de equipamentos
    result = equips.equip(sword)
    if shield in result and dagger in result:
        print(
            f'Equipou {sword.name} e '
            f'recebeu {result[0].name} e {result[1].name}.'
        )
    else:
        raise Exception(
            f'Deveria receber dois equipamentos (shield e dagger), '
            f'mas rebebeu {result}.'
        )
    result = equips.equip(sword)
    if sword in result:
        print(
            f'Equipou {sword.name} e '
            f'recebeu {result[0].name}.'
        )
    else:
        raise Exception(
            f'Deveria receber um equipamento (sword), mas rebebeu {result}.'
        )
