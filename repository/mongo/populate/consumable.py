from repository.mongo import ItemModel
from rpgram import Consumable
from rpgram.enums import RarityEnum


CONSUMABLES = [
    {
        'name': 'Minor Healing Potion',
        'description': 'Cura 100 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(100)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Light Healing Potion',
        'description': 'Cura 250 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(250)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Healing Potion',
        'description': 'Cura 500 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(500)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Greater Healing Potion',
        'description': 'Cura 1000 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(1000)',
        'rarity': RarityEnum.UNCOMMON.name,
    }, {
        'name': 'Rare Healing Potion',
        'description': 'Cura 2000 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(2000)',
        'rarity': RarityEnum.RARE.name,
    }, {
        'name': 'Epic Healing Potion',
        'description': 'Cura 5000 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(5000)',
        'rarity': RarityEnum.EPIC.name,
    }, {
        'name': 'Legendary Healing Potion',
        'description': 'Cura 10000 de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(10000)',
        'rarity': RarityEnum.LEGENDARY.name,
    }, {
        'name': 'Mythic Healing Potion',
        'description': 'Cura TODO de HP.',
        'weight': 0.1,
        'function': 'report = target.combat_stats.cure_hit_points(target.combat_stats.hp)',
        'rarity': RarityEnum.MYTHIC.name,
    },
]

if __name__ == "__main__":
    items_model = ItemModel()
    fields = ['_id', 'name', 'created_at']
    for consumable_dict in CONSUMABLES:
        consumable_name = consumable_dict['name']
        mongo_dict = items_model.get(
            query={'name': consumable_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                consumable_dict[field] = mongo_dict[field]
        consumable = Consumable(**consumable_dict)
        print(consumable)
        items_model.save(consumable)
