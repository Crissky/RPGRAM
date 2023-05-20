from typing import List

from constants.text import SECTION_HEAD, TEXT_DELIMITER
from rpgram.boosters import Equipament
from rpgram.enums import EquipamentEnum

if __name__ in ['__main__', 'equip']:
    from rpgram.enums import DamageEnum


class Equips:
    '''Classe responsável por armazenar os equipamentos do jogador'''

    def __init__(self) -> None:
        self.__helmet = None
        self.__left_hand = None
        self.__right_hand = None
        self.__armor = None
        self.__boots = None
        self.__ring = None
        self.__necklace = None
        self.__weight = 0
        self.__observers = []

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

    def equip(self, new_equipament: Equipament) -> List[Equipament]:
        equip_type = new_equipament.equip_type.name
        old_equipaments = []

        if equip_type == 'helmet':
            if self.__helmet is not None:
                old_equipaments.append(self.__helmet)
            self.__helmet = new_equipament
        elif equip_type == 'one_hand':
            if self.__left_hand is None:
                self.__left_hand = new_equipament
            elif self.__right_hand is None:
                self.__right_hand = new_equipament
            else:
                old_equipaments.append(self.__left_hand)
                old_equipaments.append(self.__right_hand)
                self.__left_hand = new_equipament
        elif equip_type == 'two_hands':
            if self.__left_hand is not None:
                old_equipaments.append(self.__left_hand)
            elif self.__right_hand is not None:
                old_equipaments.append(self.__right_hand)
            self.__left_hand = new_equipament
            self.__right_hand = new_equipament
        elif equip_type == 'armor':
            if self.__armor is not None:
                old_equipaments.append(self.__armor)
            self.__armor = new_equipament
        elif equip_type == 'boots':
            if self.__boots is not None:
                old_equipaments.append(self.__boots)
            self.__boots = new_equipament
        elif equip_type == 'ring':
            if self.__ring is not None:
                old_equipaments.append(self.__ring)
            self.__ring = new_equipament
        elif equip_type == 'necklace':
            if self.__necklace is not None:
                old_equipaments.append(self.__necklace)
            self.__necklace = new_equipament

        self.__update_stats()
        return old_equipaments

    # TODO: Implementar uma função para remover equipamentos
    def unequip(self, equip_type: str):
        ...

    def attach_observer(self, observer):
        self.__observers.append(observer)

    def detach_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

    def __update_stats(self):
        self.__weight = 0

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

        equips = set(
            [
                self.helmet, self.left_hand, self.right_hand, self.armor,
                self.boots, self.ring, self.necklace
            ]
        ) - set([None])
        for e in equips:
            self.__weight += float(e.weight)

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

    def get_sheet(self) -> str:
        return (
            f'Capacete: {self.helmet.name if self.helmet else ""}\n'
            f'Mão esquerda: {self.left_hand.name if self.left_hand else ""}\n'
            f'Mão direita: {self.right_hand.name if self.right_hand else ""}\n'
            f'Armadura: {self.armor.name if self.armor else ""}\n'
            f'Botas: {self.boots.name if self.boots else ""}\n'
            f'Anel: {self.ring.name if self.ring else ""}\n'
            f'Necklace: {self.necklace.name if self.necklace else ""}\n'
            f'Peso: {self.weight:.2f}\n\n'

            + SECTION_HEAD.format('BÔNUS E MULTIPLICADORES') +

            f'FOR: {self.strength:+} '
            f'x({self.__multiplier_strength:+.2f})\n'
            f'DES: {self.dexterity:+} '
            f'x({self.__multiplier_dexterity:+.2f})\n'
            f'CON: {self.constitution:+} '
            f'x({self.__multiplier_constitution:+.2f})\n'
            f'INT: {self.intelligence:+} '
            f'x({self.__multiplier_intelligence:+.2f})\n'
            f'SAB: {self.wisdom:+} '
            f'x({self.__multiplier_wisdom:+.2f})\n'
            f'CAR: {self.charisma:+} '
            f'x({self.__multiplier_charisma:+.2f})\n\n'

            f'HP: {self.hp:+}\n'
            f'INICIATIVA: {self.initiative:+}\n'
            f'ATAQUE FÍSICO: {self.physical_attack:+}\n'
            f'ATAQUE DE PRECISÃO: {self.precision_attack:+}\n'
            f'ATAQUE MÁGICO: {self.magical_attack:+}\n'
            f'DEFESA FÍSICA: {self.physical_defense:+}\n'
            f'DEFESA MÁGICA: {self.magical_defense:+}\n'
            f'ACERTO: {self.hit:+}\n'
            f'EVASÃO: {self.evasion:+}\n'
        )

    def __repr__(self) -> str:
        return (
            TEXT_DELIMITER +
            SECTION_HEAD.format('EQUIPAMENTOS') +
            f'{self.get_sheet()}'
            + TEXT_DELIMITER
        )

    helmet = property(lambda self: self.__helmet)
    left_hand = property(lambda self: self.__left_hand)
    right_hand = property(lambda self: self.__right_hand)
    armor = property(lambda self: self.__armor)
    boots = property(lambda self: self.__boots)
    ring = property(lambda self: self.__ring)
    necklace = property(lambda self: self.__necklace)
    weight = property(lambda self: self.__weight)

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
    equip = Equips()
    helmet = Equipament(
        name='Capacete de Aço',
        equip_type=EquipamentEnum.helmet,
        damage_type=None,
        weight=10,
        bonus_physical_defense=30,
        bonus_evasion=-5,
    )
    sword = Equipament(
        name='Espada Gigante de Aço',
        equip_type=EquipamentEnum.two_hands,
        damage_type=DamageEnum.slashing,
        weight=40,
        bonus_physical_attack=30,
        bonus_hit=15,
        bonus_evasion=-10,
    )
    armor = Equipament(
        name='Armadura de Aço',
        equip_type=EquipamentEnum.armor,
        damage_type=None,
        weight=60,
        bonus_physical_defense=80,
        bonus_evasion=-25,
    )
    boots = Equipament(
        name='Botas de Couro',
        equip_type=EquipamentEnum.boots,
        damage_type=None,
        weight=10,
        bonus_physical_defense=10,
        bonus_magical_defense=10,
        bonus_evasion=30,
    )
    any_ring = Equipament(
        name='Algum Anel',
        equip_type=EquipamentEnum.ring,
        damage_type=None,
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
    necklace = Equipament(
        name='Colar Brilhante',
        equip_type=EquipamentEnum.necklace,
        damage_type=None,
        weight=0.2,
        bonus_charisma=150,
    )

    equip.equip(helmet)
    equip.equip(sword)
    equip.equip(armor)
    equip.equip(boots)
    equip.equip(any_ring)
    equip.equip(necklace)
    print(equip)
