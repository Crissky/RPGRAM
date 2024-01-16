from repository.mongo import ItemModel
from rpgram.conditions import Condition
from rpgram.consumables import (
    CureConsumable,
    IdentifyingConsumable,
    HealingConsumable,
    ReviveConsumable,
    XPConsumable,
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
    MINOR_REVIVE_POWER,
)
from rpgram.consumables.other import (
    EPIC_PROFICIENCY_ELIXIR_POWER,
    LEGENDARY_PROFICIENCY_ELIXIR_POWER,
    MYTHIC_PROFICIENCY_ELIXIR_POWER,
    PROFICIENCY_ELIXIR_POWER,
    RARE_PROFICIENCY_ELIXIR_POWER
)
from rpgram.enums import HealingConsumableEnum, RarityEnum, TurnEnum
from rpgram.enums.debuff import (
    BERSERKER,
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

    # Revive Itens
    {
        'name': 'Minor Phoenix Feather',
        'description': (
            f'Revive personagem curando {MINOR_REVIVE_POWER} de HP.'
        ),
        'power': MINOR_REVIVE_POWER,
        'weight': 0.50,
        'rarity': RarityEnum.RARE.name,
        'class': ReviveConsumable,
    },

    # Cure Potions
    {
        'name': "GrayMage's Pipe",
        'description': f'Cura 1 Nível da condição "{BERSERKER}".',
        'condition_target': BERSERKER,
        'weight': 0.05,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Cotton Bandage',
        'description': f'Cura 1 Nível da condição "{BLEEDING}".',
        'condition_target': BLEEDING,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Eye Drops',
        'description': f'Cura 1 Nível da condição "{BLINDNESS}".',
        'condition_target': BLINDNESS,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Aloe Compress',
        'description': f'Cura 1 Nível da condição "{BURN}".',
        'condition_target': BURN,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Red Remedy',
        'description': f'Cura 1 Nível da condição "{CONFUSION}".',
        'condition_target': CONFUSION,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Mystical Incense',
        'description': f'Cura 1 Nível da condição "{CURSE}".',
        'condition_target': CURSE,
        'weight': 0.20,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Energy Potion',
        'description': f'Cura 1 Nível da condição "{EXHAUSTION}".',
        'condition_target': EXHAUSTION,
        'weight': 0.25,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Hot Potion',
        'description': f'Cura 1 Nível da condição "{FROZEN}".',
        'condition_target': FROZEN,
        'weight': 0.25,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Vitamin Fruit',
        'description': f'Cura 1 Nível da condição "{PARALYSIS}".',
        'condition_target': PARALYSIS,
        'weight': 0.55,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Gold Needle',
        'description': f'Cura 1 Nível da condição "{PETRIFIED}".',
        'condition_target': PETRIFIED,
        'weight': 0.15,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Antidote',
        'description': f'Cura 1 Nível da condição "{POISONING}".',
        'condition_target': POISONING,
        'weight': 0.15,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Echo Herb',
        'description': f'Cura 1 Nível da condição "{SILENCE}".',
        'condition_target': SILENCE,
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Panacea',
        'description': (
            f'Cura 1 Nível das condições "{BERSERKER}", "{BLEEDING}", "{BLINDNESS}", '
            f'"{BURN}", "{CONFUSION}", "{CURSE}", "{EXHAUSTION}", "{FROZEN}", '
            f'"{PARALYSIS}", "{PETRIFIED}", "{POISONING}", "{SILENCE}".'
        ),
        'condition_target': [
            BERSERKER, BLEEDING, BLINDNESS, BURN, CONFUSION, CURSE,
            EXHAUSTION, FROZEN, PARALYSIS, PETRIFIED, POISONING, SILENCE
        ],
        'weight': 1.23,
        'rarity': RarityEnum.EPIC.name,
        'class': CureConsumable
    },


    # Greater Cure Potions
    {
        'name': "Greater GrayMage's Pipe",
        'description': f'Cura 3 Níveis da condição "{BERSERKER}".',
        'condition_target': [BERSERKER, BERSERKER, BERSERKER],
        'weight': 0.05,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },

    {
        'name': 'Greater Cotton Bandage',
        'description': f'Cura 3 Níveis da condição "{BLEEDING}".',
        'condition_target': [BLEEDING, BLEEDING, BLEEDING],
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Eye Drops',
        'description': f'Cura 3 Níveis da condição "{BLINDNESS}".',
        'condition_target': [BLINDNESS, BLINDNESS, BLINDNESS],
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Aloe Compress',
        'description': f'Cura 3 Níveis da condição "{BURN}".',
        'condition_target': [BURN, BURN, BURN],
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Red Remedy',
        'description': f'Cura 3 Níveis da condição "{CONFUSION}".',
        'condition_target': [CONFUSION, CONFUSION, CONFUSION],
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Mystical Incense',
        'description': f'Cura 3 Níveis da condição "{CURSE}".',
        'condition_target': [CURSE, CURSE, CURSE],
        'weight': 0.20,
        'rarity': RarityEnum.EPIC.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Energy Potion',
        'description': f'Cura 3 Níveis da condição "{EXHAUSTION}".',
        'condition_target': [EXHAUSTION, EXHAUSTION, EXHAUSTION],
        'weight': 0.25,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Hot Potion',
        'description': f'Cura 3 Níveis da condição "{FROZEN}".',
        'condition_target': [FROZEN, FROZEN, FROZEN],
        'weight': 0.25,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Vitamin Fruit',
        'description': f'Cura 3 Níveis da condição "{PARALYSIS}".',
        'condition_target': [PARALYSIS, PARALYSIS, PARALYSIS],
        'weight': 0.55,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Gold Needle',
        'description': f'Cura 3 Níveis da condição "{PETRIFIED}".',
        'condition_target': [PETRIFIED, PETRIFIED, PETRIFIED],
        'weight': 0.15,
        'rarity': RarityEnum.EPIC.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Antidote',
        'description': f'Cura 3 Níveis da condição "{POISONING}".',
        'condition_target': [POISONING, POISONING, POISONING],
        'weight': 0.15,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Echo Herb',
        'description': f'Cura 3 Níveis da condição "{SILENCE}".',
        'condition_target': [SILENCE, SILENCE, SILENCE],
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
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
    {
        'name': 'Proficiency Elixir',
        'description': (
            f'Adiciona {PROFICIENCY_ELIXIR_POWER} pontos de experiência.'
        ),
        'power': PROFICIENCY_ELIXIR_POWER,
        'weight': 0.50,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': XPConsumable
    },
    {
        'name': 'Rare Proficiency Elixir',
        'description': (
            f'Adiciona {RARE_PROFICIENCY_ELIXIR_POWER} pontos de experiência.'
        ),
        'power': RARE_PROFICIENCY_ELIXIR_POWER,
        'weight': 0.75,
        'rarity': RarityEnum.RARE.name,
        'class': XPConsumable
    },
    {
        'name': 'Epic Proficiency Elixir',
        'description': (
            f'Adiciona {EPIC_PROFICIENCY_ELIXIR_POWER} pontos de experiência.'
        ),
        'power': EPIC_PROFICIENCY_ELIXIR_POWER,
        'weight': 1.00,
        'rarity': RarityEnum.EPIC.name,
        'class': XPConsumable
    },
    {
        'name': 'Legendary Proficiency Elixir',
        'description': (
            f'Adiciona {LEGENDARY_PROFICIENCY_ELIXIR_POWER} '
            f'pontos de experiência.'
        ),
        'power': LEGENDARY_PROFICIENCY_ELIXIR_POWER,
        'weight': 1.25,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': XPConsumable
    },
    {
        'name': 'Mythic Proficiency Elixir',
        'description': (
            f'Adiciona {MYTHIC_PROFICIENCY_ELIXIR_POWER} '
            f'pontos de experiência.'
        ),
        'power': MYTHIC_PROFICIENCY_ELIXIR_POWER,
        'weight': 1.50,
        'rarity': RarityEnum.MYTHIC.name,
        'class': XPConsumable
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
