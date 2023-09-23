from enum import Enum


class RarityEnum(Enum):
    COMMON = 'Comum'
    UNCOMMON = 'Incomum'
    RARE = 'Raro'
    EPIC = 'Épico'
    LEGENDARY = 'Lendário'
    MYTHIC = 'Mítico'


class RarityEnumOrder(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    MYTHIC = 6


if __name__ == '__main__':
    for rarity in RarityEnum:
        print(RarityEnumOrder[rarity.name])
