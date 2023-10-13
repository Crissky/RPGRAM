from repository.mongo import ItemModel
from rpgram import Consumable
from rpgram.boosters import Condition
from rpgram.enums import RarityEnum, TurnEnum


CONSUMABLES = [
    {
        'name': 'Minor Healing Potion',
        'description': 'Cura 100 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Minor Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(100)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Light Healing Potion',
        'description': 'Cura 250 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Light Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(250)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Healing Potion',
        'description': 'Cura 500 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(500)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.COMMON.name,
    }, {
        'name': 'Greater Healing Potion',
        'description': 'Cura 1000 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Greater Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(1000)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.UNCOMMON.name,
    }, {
        'name': 'Rare Healing Potion',
        'description': 'Cura 2000 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Rare Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(2000)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.RARE.name,
    }, {
        'name': 'Epic Healing Potion',
        'description': 'Cura 5000 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Epic Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(5000)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.EPIC.name,
    }, {
        'name': 'Legendary Healing Potion',
        'description': 'Cura 10000 de HP em 5 Turnos.',
        'weight': 0.1,
        'condition': Condition(
            'Legendary Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(10000)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
        'rarity': RarityEnum.LEGENDARY.name,
    }, {
        'name': 'Mythic Healing Potion',
        'description': 'Cura TODO de HP ou 1000 a cada Turno.',
        'weight': 0.1,
        'condition': Condition(
            'Mythic Healing Potion', None, None, None, TurnEnum.START
        ),
        'function': 'report = target.combat_stats.cure_hit_points(target.combat_stats.hp)',
        'battle_function': 'report = target.status.add_condition(self.condition)',
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
