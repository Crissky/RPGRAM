from repository.mongo import ItemModel
from rpgram import Consumable
from rpgram.enums import RarityEnum


CONSUMABLES = [
    {
        'name': 'Minor Healing Potion',
        'description': 'Cura 100 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 100',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Light Healing Potion',
        'description': 'Cura 250 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 250',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Healing Potion',
        'description': 'Cura 500 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 500',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Greater Healing Potion',
        'description': 'Cura 1000 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 1000',
        'rarity': RarityEnum.UNCOMMON.name,
    }, {
        'name': 'Rare Healing Potion',
        'description': 'Cura 2000 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 2000',
        'rarity': RarityEnum.RARE.name,
    }, {
        'name': 'Epic Healing Potion',
        'description': 'Cura 5000 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 5000',
        'rarity': RarityEnum.EPIC.name,
    }, {
        'name': 'Legendary Healing Potion',
        'description': 'Cura 10000 de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = 10000',
        'rarity': RarityEnum.LEGENDARY.name,
    }, {
        'name': 'Mythic Healing Potion',
        'description': 'Cura TODO de HP.',
        'weight': 0.1,
        'function': 'target.combat_stats.hp = target.combat_stats.hp',
        'rarity': RarityEnum.MYTHIC.name,
    },
]

if __name__ == "__main__":
    items_model = ItemModel()
    for consumable_dict in CONSUMABLES:
        consumable = Consumable(**consumable_dict)
        print(consumable)
        items_model.save(consumable)
