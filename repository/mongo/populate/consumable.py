from repository.mongo import ItemModel
from rpgram.conditions import (
    Condition,
    Heal1Condition,
    Heal2Condition,
    Heal3Condition,
    Heal4Condition,
    Heal5Condition,
    Heal6Condition,
    Heal7Condition,
    Heal8Condition,
)
from rpgram.consumables import (
    CureConsumable,
    GemstoneConsumable,
    HealingConsumable,
    IdentifyingConsumable,
    ReviveConsumable,
    TrocadoPouchConsumable,
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
    REVIVE_POWER,
)
from rpgram.consumables.other import (
    EPIC_PROFICIENCY_ELIXIR_POWER,
    LEGENDARY_PROFICIENCY_ELIXIR_POWER,
    MYTHIC_PROFICIENCY_ELIXIR_POWER,
    PROFICIENCY_ELIXIR_POWER,
    RARE_PROFICIENCY_ELIXIR_POWER,
)
from rpgram.enums import (
    HealingConsumableEnum,
    RarityEnum,
    TrocadoEnum,
    TurnEnum
    )
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
from rpgram.enums.trocado import TrocadoEnum


CURE_ITEMS_LEVEL = 1
GREATER_CURE_ITEMS_LEVEL = 5
MAJOR_CURE_ITEMS_LEVEL = 10
SUPERIOR_CURE_ITEMS_LEVEL = 50


CONSUMABLES = [
    # Healing Potions
    {
        'name': HealingConsumableEnum.HEAL1.value,
        'description': f'Cura {MINOR_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': MINOR_HEALING_POTION_POWER,
        'weight': 0.10,
        'condition': Heal1Condition(),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL2.value,
        'description': f'Cura {LIGHT_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': LIGHT_HEALING_POTION_POWER,
        'weight': 0.15,
        'condition': Heal2Condition(),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL3.value,
        'description': f'Cura {HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': HEALING_POTION_POWER,
        'weight': 0.20,
        'condition': Heal3Condition(),
        'rarity': RarityEnum.COMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL4.value,
        'description': (
            f'Cura {GREATER_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': GREATER_HEALING_POTION_POWER,
        'weight': 0.25,
        'condition': Heal4Condition(),
        'rarity': RarityEnum.UNCOMMON.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL5.value,
        'description': f'Cura {RARE_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': RARE_HEALING_POTION_POWER,
        'weight': 0.30,
        'condition': Heal5Condition(),
        'rarity': RarityEnum.RARE.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL6.value,
        'description': f'Cura {EPIC_HEALING_POTION_POWER} de HP em 5 Turnos.',
        'power': EPIC_HEALING_POTION_POWER,
        'weight': 0.35,
        'condition': Heal6Condition(),
        'rarity': RarityEnum.EPIC.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL7.value,
        'description': (
            f'Cura {LEGENDARY_HEALING_POTION_POWER} de HP em 5 Turnos.'
        ),
        'power': LEGENDARY_HEALING_POTION_POWER,
        'weight': 0.40,
        'condition': Heal7Condition(),
        'rarity': RarityEnum.LEGENDARY.name,
        'class': HealingConsumable,
    }, {
        'name': HealingConsumableEnum.HEAL8.value,
        'description': 'Cura TODO de HP ou 1000 a cada Turno.',
        'power': MYTHIC_HEALING_POTION_POWER,
        'weight': 0.45,
        'condition': Heal8Condition(),
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
        'rarity': RarityEnum.UNCOMMON.name,
        'class': ReviveConsumable,
    },
    {
        'name': 'Phoenix Feather',
        'description': (
            f'Revive personagem curando {REVIVE_POWER} de HP.'
        ),
        'power': REVIVE_POWER,
        'weight': 1.50,
        'rarity': RarityEnum.RARE.name,
        'class': ReviveConsumable,
    },

    # Cure Potions
    {
        'name': "GrayMage's Pipe",
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{BERSERKER}".'
        ),
        'condition_target': ([BERSERKER] * CURE_ITEMS_LEVEL),
        'weight': 0.05,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Cotton Bandage',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{BLEEDING}".'
        ),
        'condition_target': ([BLEEDING] * CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Eye Drops',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{BLINDNESS}".'
        ),
        'condition_target': ([BLINDNESS] * CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Aloe Compress',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{BURN}".'
        ),
        'condition_target': ([BURN] * CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Red Remedy',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{CONFUSION}".'
        ),
        'condition_target': ([CONFUSION] * CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Mystical Incense',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{CURSE}".'
        ),
        'condition_target': ([CURSE] * CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Energy Potion',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{EXHAUSTION}".'
        ),
        'condition_target': ([EXHAUSTION] * CURE_ITEMS_LEVEL),
        'weight': 0.25,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Hot Potion',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{FROZEN}".'
        ),
        'condition_target': ([FROZEN] * CURE_ITEMS_LEVEL),
        'weight': 0.25,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Vitamin Fruit',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{PARALYSIS}".'
        ),
        'condition_target': ([PARALYSIS] * CURE_ITEMS_LEVEL),
        'weight': 0.55,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Gold Needle',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{PETRIFIED}".'
        ),
        'condition_target': ([PETRIFIED] * CURE_ITEMS_LEVEL),
        'weight': 0.15,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Antidote',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{POISONING}".'
        ),
        'condition_target': ([POISONING] * CURE_ITEMS_LEVEL),
        'weight': 0.15,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Echo Herb',
        'description': (
            f'Cura {CURE_ITEMS_LEVEL} Nível da condição "{SILENCE}".'
        ),
        'condition_target': ([SILENCE] * CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Panacea',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} Nível das condições '
            f'"{BERSERKER}", "{BLEEDING}", "{BLINDNESS}", '
            f'"{BURN}", "{CONFUSION}", "{CURSE}", "{EXHAUSTION}", "{FROZEN}", '
            f'"{PARALYSIS}", "{PETRIFIED}", "{POISONING}", "{SILENCE}".'
        ),
        'condition_target': sorted([
            BERSERKER, BLEEDING, BLINDNESS, BURN, CONFUSION, CURSE,
            EXHAUSTION, FROZEN, PARALYSIS, PETRIFIED, POISONING, SILENCE
        ] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 1.23,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },


    # Greater Cure Potions
    {
        'name': "Greater GrayMage's Pipe",
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BERSERKER}".'
        ),
        'condition_target': ([BERSERKER] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },

    {
        'name': 'Greater Cotton Bandage',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BLEEDING}".'
        ),
        'condition_target': ([BLEEDING] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Eye Drops',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BLINDNESS}".'
        ),
        'condition_target': ([BLINDNESS] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Aloe Compress',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BURN}".'
        ),
        'condition_target': ([BURN] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Red Remedy',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{CONFUSION}".'
        ),
        'condition_target': ([CONFUSION] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Mystical Incense',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{CURSE}".'
        ),
        'condition_target': ([CURSE] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Energy Potion',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{EXHAUSTION}".'
        ),
        'condition_target': ([EXHAUSTION] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.50,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Hot Potion',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{FROZEN}".'
        ),
        'condition_target': ([FROZEN] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.50,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Vitamin Fruit',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{PARALYSIS}".'
        ),
        'condition_target': ([PARALYSIS] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 1.10,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Gold Needle',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{PETRIFIED}".'
        ),
        'condition_target': ([PETRIFIED] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.30,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Antidote',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{POISONING}".'
        ),
        'condition_target': ([POISONING] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.30,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Echo Herb',
        'description': (
            f'Cura {GREATER_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{SILENCE}".'
        ),
        'condition_target': ([SILENCE] * GREATER_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': CureConsumable
    },
    {
        'name': 'Greater Panacea',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} Nível das condições '
            f'"{BERSERKER}", "{BLEEDING}", "{BLINDNESS}", '
            f'"{BURN}", "{CONFUSION}", "{CURSE}", "{EXHAUSTION}", "{FROZEN}", '
            f'"{PARALYSIS}", "{PETRIFIED}", "{POISONING}", "{SILENCE}".'
        ),
        'condition_target': sorted([
            BERSERKER, BLEEDING, BLINDNESS, BURN, CONFUSION, CURSE,
            EXHAUSTION, FROZEN, PARALYSIS, PETRIFIED, POISONING, SILENCE
        ] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 3.14,
        'rarity': RarityEnum.EPIC.name,
        'class': CureConsumable
    },

    # Major Cure Potions
    {
        'name': "Major GrayMage's Pipe",
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BERSERKER}".'
        ),
        'condition_target': ([BERSERKER] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.20,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },

    {
        'name': 'Major Cotton Bandage',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BLEEDING}".'
        ),
        'condition_target': ([BLEEDING] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Eye Drops',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BLINDNESS}".'
        ),
        'condition_target': ([BLINDNESS] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Aloe Compress',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{BURN}".'
        ),
        'condition_target': ([BURN] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Red Remedy',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{CONFUSION}".'
        ),
        'condition_target': ([CONFUSION] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Mystical Incense',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{CURSE}".'
        ),
        'condition_target': ([CURSE] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.80,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Energy Potion',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{EXHAUSTION}".'
        ),
        'condition_target': ([EXHAUSTION] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 1.00,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Hot Potion',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{FROZEN}".'
        ),
        'condition_target': ([FROZEN] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 1.00,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Vitamin Fruit',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{PARALYSIS}".'
        ),
        'condition_target': ([PARALYSIS] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 2.20,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Gold Needle',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{PETRIFIED}".'
        ),
        'condition_target': ([PETRIFIED] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.60,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Antidote',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{POISONING}".'
        ),
        'condition_target': ([POISONING] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.60,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Echo Herb',
        'description': (
            f'Cura {MAJOR_CURE_ITEMS_LEVEL} níveis da '
            f'condição "{SILENCE}".'
        ),
        'condition_target': ([SILENCE] * MAJOR_CURE_ITEMS_LEVEL),
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': CureConsumable
    },
    {
        'name': 'Major Panacea',
        'description': (
            f'Cura {SUPERIOR_CURE_ITEMS_LEVEL} Nível das condições '
            f'"{BERSERKER}", "{BLEEDING}", "{BLINDNESS}", '
            f'"{BURN}", "{CONFUSION}", "{CURSE}", "{EXHAUSTION}", "{FROZEN}", '
            f'"{PARALYSIS}", "{PETRIFIED}", "{POISONING}", "{SILENCE}".'
        ),
        'condition_target': sorted([
            BERSERKER, BLEEDING, BLINDNESS, BURN, CONFUSION, CURSE,
            EXHAUSTION, FROZEN, PARALYSIS, PETRIFIED, POISONING, SILENCE
        ] * SUPERIOR_CURE_ITEMS_LEVEL),
        'weight': 6.66,
        'rarity': RarityEnum.LEGENDARY.name,
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

    #  Trocado Pouch Items
    {
        'name': f'Tiny Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Tiny Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.20,
        'rarity': RarityEnum.COMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Tiny Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.30,
        'rarity': RarityEnum.COMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Tiny Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.40,
        'rarity': RarityEnum.COMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Minor Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.50,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Minor Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.60,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Minor Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.70,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Minor Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 0.80,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 1.00,
        'rarity': RarityEnum.RARE.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 1.15,
        'rarity': RarityEnum.RARE.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 1.30,
        'rarity': RarityEnum.RARE.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 1.50,
        'rarity': RarityEnum.RARE.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Greater Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 3.00,
        'rarity': RarityEnum.EPIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Greater Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 4.00,
        'rarity': RarityEnum.EPIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Greater Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 5.00,
        'rarity': RarityEnum.EPIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Greater Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 6.00,
        'rarity': RarityEnum.EPIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Major Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 10.00,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Major Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 20.00,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Major Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 35.00,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Major Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 50.00,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Superior Tax {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 100.00,
        'rarity': RarityEnum.MYTHIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Superior Monarch {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 200.00,
        'rarity': RarityEnum.MYTHIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Superior Emperor {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 350.00,
        'rarity': RarityEnum.MYTHIC.name,
        'class': TrocadoPouchConsumable
    },
    {
        'name': f'Superior Overlord {TrocadoEnum.TROCADO_POUCH.value}',
        'weight': 500.00,
        'rarity': RarityEnum.MYTHIC.name,
        'class': TrocadoPouchConsumable
    },

    #  Gemstone Items
    {
        'name': 'Minor Opal',
        'weight': 0.10,
        'rarity': RarityEnum.COMMON.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Opal',
        'weight': 0.20,
        'rarity': RarityEnum.COMMON.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Opal',
        'weight': 0.30,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Minor Jadeite',
        'weight': 0.20,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Jadeite',
        'weight': 0.30,
        'rarity': RarityEnum.UNCOMMON.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Jadeite',
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Minor Sapphire',
        'weight': 0.30,
        'rarity': RarityEnum.RARE.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Sapphire',
        'weight': 0.40,
        'rarity': RarityEnum.RARE.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Sapphire',
        'weight': 0.50,
        'rarity': RarityEnum.EPIC.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Minor Ruby',
        'weight': 0.50,
        'rarity': RarityEnum.RARE.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Ruby',
        'weight': 0.60,
        'rarity': RarityEnum.EPIC.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Ruby',
        'weight': 0.70,
        'rarity': RarityEnum.EPIC.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Minor Emerald',
        'weight': 0.70,
        'rarity': RarityEnum.EPIC.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Emerald',
        'weight': 0.80,
        'rarity': RarityEnum.EPIC.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Emerald',
        'weight': 0.90,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Minor Diamond',
        'weight': 1.00,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Diamond',
        'weight': 1.50,
        'rarity': RarityEnum.LEGENDARY.name,
        'class': GemstoneConsumable
    },
    {
        'name': 'Greater Diamond',
        'weight': 2.50,
        'rarity': RarityEnum.MYTHIC.name,
        'class': GemstoneConsumable
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
