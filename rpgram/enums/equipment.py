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
    ONE_HAND = 1
    TWO_HANDS = 2
    ARMOR = 3
    BOOTS = 5
    RING = 6
    AMULET = 7


ACCESSORIES_ENUM_LIST = [
    EquipmentEnum.RING, EquipmentEnum.RING.name,
    EquipmentEnum.AMULET, EquipmentEnum.AMULET.name,
]

if __name__ == '__main__':
    for equipment in EquipmentEnum:
        print(EquipmentEnumOrder[equipment.name])
