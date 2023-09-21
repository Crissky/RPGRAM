from enum import Enum


class EquipmentEnum(Enum):
    HELMET = 'Capacete'
    ONE_HAND = 'Uma Mão'
    TWO_HANDS = 'Duas Mãos'
    ARMOR = 'Armadura'
    BOOTS = 'Botas'
    RING = 'Anel'
    AMULET = 'Amuleto'


class EquipmentEnumOrder(Enum):
    HELMET = 4
    ONE_HAND = 6
    TWO_HANDS = 7
    ARMOR = 5
    BOOTS = 3
    RING = 2
    AMULET = 1


if __name__ == '__main__':
    for equipment in EquipmentEnum:
        print(EquipmentEnumOrder[equipment.name])
