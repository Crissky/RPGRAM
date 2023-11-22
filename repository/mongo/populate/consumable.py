from repository.mongo import ItemModel
from rpgram.conditions import Condition
from rpgram.consumables import (
    CureConsumable,
    IdentifyingConsumable,
    HealingConsumable
)
from rpgram.consumables.heal import (
    MINOR_HEALING_POTION_POWER,
    LIGHT_HEALING_POTION_POWER,
    HEALING_POTION_POWER,
    GREATER_HEALING_POTION_POWER,
    RARE_HEALING_POTION_POWER,
    EPIC_HEALING_POTION_POWER,
    LEGENDARY_HEALING_POTION_POWER,
    MYTHIC_HEALING_POTION_POWER,
)
from rpgram.enums import HealingConsumableEnum, RarityEnum, TurnEnum
from rpgram.enums.debuff import (
    BLEEDING,
    BLINDNESS,
    BURN,
    CONFUSION,
    CURSE,
    EXHAUSTION,
    FROZEN,
    PARALYSIS,
    PETRIFIED,
    POISONING,
    SILENCE,
)


CONSUMABLES = [
    # Healing Potions
    {
        'name': HealingConsumableEnum.HEAL1.value,
        'description': f'Cura {MINOR_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': MINOR_HEALING_POTION_POWER,
        'weight': 0.10,
        'condition': Condition(
            HealingConsumableEnum.HEAL1.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL2.value,
        'description': f'Cura {LIGHT_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': LIGHT_HEALING_POTION_POWER,
        'weight': 0.15,
        'condition': Condition(
            HealingConsumableEnum.HEAL2.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL3.value,
        'description': f'Cura {HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': HEALING_POTION_POWER,
        'weight': 0.20,
        'condition': Condition(
            HealingConsumableEnum.HEAL3.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL4.value,
        'description': (
            f'Cura {GREATER_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': GREATER_HEALING_POTION_POWER,
        'weight': 0.25,
        'condition': Condition(
            HealingConsumableEnum.HEAL4.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.UNCOMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL5.value,
        'description': f'Cura {RARE_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': RARE_HEALING_POTION_POWER,
        'weight': 0.30,
        'condition': Condition(
            HealingConsumableEnum.HEAL5.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.RARE.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL6.value,
        'description': f'Cura {EPIC_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': EPIC_HEALING_POTION_POWER,
        'weight': 0.35,
        'condition': Condition(
            HealingConsumableEnum.HEAL6.value, None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.EPIC.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL7.value,
        'description': (
            f'Cura {LEGENDARY_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': LEGENDARY_HEALING_POTION_POWER,
        'weight': 0.40,
        'condition': Condition(
            HealingConsumableEnum.HEAL7.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.LEGENDARY.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL8.value,
        'description': 'Cura TODO de HP ou 1000 a cada Turno.',
        'power': MYTHIC_HEALING_POTION_POWER,
        'weight': 0.45,
        'condition': Condition(
            HealingConsumableEnum.HEAL8.value,
            None, None, None, TurnEnum.START
        ),
        'rarity': RarityEnum.MYTHIC.name,
        'class': HealingConsumable,
    },

    # Cure Potions
    {
        'name': 'Cotton Bandage',
        'description': f'Cura condição "{BLEEDING}".',
        'condition_target': BLEEDING,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Eye Drops',
        'description': f'Cura condição "{BLINDNESS}".',
        'condition_target': BLINDNESS,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Aloe Compress',
        'description': f'Cura condição "{BURN}".',
        'condition_target': BURN,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Red Remedy',
        'description': f'Cura condição "{CONFUSION}".',
        'condition_target': CONFUSION,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Mystical Incense',
        'description': f'Cura condição "{CURSE}".',
        'condition_target': CURSE,
        'weight': 0.20,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Energy Potion',
        'description': f'Cura condição "{EXHAUSTION}".',
        'condition_target': EXHAUSTION,
        'weight': 0.25,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Hot Potion',
        'description': f'Cura condição "{FROZEN}".',
        'condition_target': FROZEN,
        'weight': 0.25,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Vitamin Fruit',
        'description': f'Cura condição "{PARALYSIS}".',
        'condition_target': PARALYSIS,
        'weight': 0.55,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Gold Needle',
        'description': f'Cura condição "{PETRIFIED}".',
        'condition_target': PETRIFIED,
        'weight': 0.15,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Antidote',
        'description': f'Cura condição "{POISONING}".',
        'condition_target': POISONING,
        'weight': 0.15,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Echo Herb',
        'description': f'Cura condição "{SILENCE}".',
        'condition_target': SILENCE,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },

    # Other Items
    {
        'name': 'Identifying Lens',
        'description': f'Identifica bônus ocultos de um Equipamento.',
        'weight': 0.30,
        'rarity': RarityEnum.RARE.name,
        'class': IdentifyingConsumable
    },
]

if __name__ == "__main__":
    items_model = ItemModel()
    fields = ['_id', 'name', 'created_at']
    for consumable_dict in CONSUMABLES:
        consumable_name = consumable_dict['name']
        consumable_class = consumable_dict.pop('class')
        mongo_dict = items_model.get(
            query={'name': consumable_name},
            fields=fields,
        )
        if mongo_dict:
            for field in fields:
                consumable_dict[field] = mongo_dict[field]
        consumable = consumable_class(**consumable_dict)
        print(consumable)
        items_model.save(consumable, replace=True)
