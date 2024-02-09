# DAMAGE_TYPES para equipamentos de uma ou duas mãos

SLASHING_WEAPONS = [
    'SWORD', 'DAGGER', 'GREAT_SWORD', 'AXE', 'DOUBLE_AXE', 'KATANA',
    'SCIMITAR', 'MACHETE', 'CUTLASS', 'FALCHION', 'HALBERD', 'WHIP'
]
BLUDGEONING_WEAPONS = [
    'SHIELD', 'STAFF', 'WARHAMMER', 'MACE', 'CLUB', 'FLAIL',
    'MORNING_STAR', 'SLEDGEHAMMER', 'BLACKJACK', 'SHARUR'
]
PIERCING_WEAPONS = [
    'SPIKED_SHIELD', 'BOW', 'HALBERD', 'CROSSBOW', 'ARBALEST', 'SPEAR',
    'JAVELIN', 'PIKE', 'LANCE', 'RAPIER', 'ESTOQUE', 'TRIDENT', 'DART_BLOWER',
    'SAI'
]
MAGIC_WEAPONS = [
    'WAND', 'GRIMOIRE', 'ORB', 'SCEPTER', 'QUILL', 'CHALICE',
    'HARP', 'ROD', 'CRYSTAL', 'VAJRA', 'SHARUR', 'RIKUDŌKON',
    'PRISMATIC_SHIELD'
]

ALL_WEAPONS = []
ALL_WEAPONS.extend(SLASHING_WEAPONS)
ALL_WEAPONS.extend(BLUDGEONING_WEAPONS)
ALL_WEAPONS.extend(PIERCING_WEAPONS)
ALL_WEAPONS.extend(MAGIC_WEAPONS)


# Equipamentos com maior chance de ter um tipo de dano extra
ENCHANTED_WEAPONS = [
    'WAND', 'STAFF', 'DART_BLOWER', 'GRIMOIRE', 'ORB', 'SCEPTER', 'QUILL',
    'CHALICE', 'HARP', 'ROD', 'CRYSTAL', 'VAJRA', 'SHARUR', 'RIKUDŌKON'
]


# Equipamentos mais ou menos pesados que o normal
LIGHT_EQUIPMENTS = [
    'RING', 'NECKLACE', 'AMULET', 'QUILL', 'CHARM', 'COIN', 'SCARF',
    'KRATOS\'S_RING', 'HERMES\'S_RING', 'ARTEMIS\'S_RING', 'HECATE\'S_RING',
    'GAIA\'S_RING',
]
HEAVY_EQUIPMENTS = [
    'GREAT_SWORD', 'SHIELD', 'SPIKED_SHIELD', 'DOUBLE_AXE', 'HALBERD', 'FLAIL',
    'SLEDGEHAMMER', 'ARBALEST', 'SPEAR', 'LANCE', 'SCEPTER', 'CRYSTAL',
    'RIKUDŌKON', 'SPAULDER', 'SPIKED_SPAULDER', 'GREAVES', 'SPIKED_GREAVES',
    'PRISMATIC_SHIELD'
]
VERY_HEAVY_EQUIPMENTS = [
    'ARMOR', 'SPIKED_ARMOR', 'WARHAMMER', 'PIKE', 'BRIGANDINE', 'SHARUR'
]


# Especial Materials Equipments
MAGICAL_QUILL_EQUIPMENTS = ['QUILL']
MAGICAL_GRIMOIRE_EQUIPMENTS = ['GRIMOIRE', 'SHOES']
MAGICAL_STONES_EQUIPMENTS = ['ORB', 'CRYSTAL', 'PRISMATIC_SHIELD']
MAGICAL_WEARABLE_EQUIPMENTS = ['ROBE', 'POINTED_HAT']
MAGICAL_MASK_EQUIPMENTS = ['MASK']
TATICAL_WEARABLE_EQUIPMENTS = ['CLOAK', 'GUGEL', 'HOOD', 'SCARF']
COIN_EQUIPMENTS = ['COIN']


# EQUIPMENTS DEFINITIONS
ONE_HAND_EQUIPMENTS = {
    'SWORD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 10,
        }
    ),
    'DAGGER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 7,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'WAND': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 2,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 3, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    ),
    'SHIELD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 7, 'bonus_hit': 1,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
    ),
    'SPIKED_SHIELD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 7, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
    ),
    'PRISMATIC_SHIELD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
    ),
    'AXE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 10,
            'bonus_evasion': 10,
        }
    ),
    'SCIMITAR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 3, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'MACHETE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 3,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 0, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'CUTLASS': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 1, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'FALCHION': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 7, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 3,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 3, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 3, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'WHIP': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 1,
        }
    ),
    'MACE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 7, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 10,
            'bonus_evasion': 10,
        }
    ),
    'CLUB': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'MORNING_STAR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 10,
            'bonus_evasion': 1,
        }
    ),
    'SLEDGEHAMMER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 7, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 10,
            'bonus_evasion': 10,
        }
    ),
    'BLACKJACK': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'CROSSBOW': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 1,
        }
    ),
    'JAVELIN': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'RAPIER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 7,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'ESTOQUE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 7,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'TRIDENT': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'SAI': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 7,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'ORB': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 7, 'bonus_hit': 3,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'QUILL': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'CHALICE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 7, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 10, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'ROD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 7, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'VAJRA': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
TWO_HANDS_EQUIPMENTS = {
    'GREAT_SWORD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    ),
    'BOW': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 3,
        }
    ),
    'STAFF': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    ),
    'DOUBLE_AXE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 10,
            'bonus_evasion': 10,
        }
    ),
    'KATANA': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 3, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'HALBERD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 7,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 10,
        }
    ),
    'WARHAMMER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 7, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 10,
            'bonus_evasion': 10,
        }
    ),
    'FLAIL': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 10,
            'bonus_evasion': 1,
        }
    ),
    'ARBALEST': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 3,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    ),
    'SPEAR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'PIKE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'LANCE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 7, 'bonus_initiative': 5,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 1,
        }
    ),
    'DART_BLOWER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 10,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'GRIMOIRE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SCEPTER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 7, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'HARP': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 3, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'CRYSTAL': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 7, 'bonus_hit': 3,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SHARUR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 0,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 10,
        }
    ),
    'RIKUDŌKON': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
HELMET_EQUIPMENTS = {
    'HELMET': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 5, 'bonus_hit': 1,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    ),
    'KRÁNOS': dict(  # krános é capacete em grego
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 7, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 10,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    ),
    'GUGEL': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 3, 'bonus_hit': 5,
            'bonus_evasion': 10,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'HOOD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 7,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 7,
            'bonus_evasion': 7,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'POINTED_HAT': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 7, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 5,
        }
    ),
    'MASK': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 7, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 7, 'bonus_hit': 3,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
ARMOR_EQUIPMENTS = {
    'ARMOR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    ),
    'SPIKED_ARMOR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 0, 'bonus_hit': 3,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 10,
        }
    ),
    'BRIGANDINE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 3,
            'bonus_evasion': 5,
        }
    ),
    'ROBE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 7, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'CLOAK': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SPAULDER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 3, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 3, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SPIKED_SPAULDER': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 5,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
}
BOOTS_EQUIPMENTS = {
    'BOOTS': dict(
        attr_bonus_prob={
            'bonus_hit_points': 3, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 3, 'bonus_hit': 5,
            'bonus_evasion': 10,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SANDALS': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 5,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 10,
            'bonus_evasion': 10,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'GREAVES': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SPIKED_GREAVES': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 3,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 5,
            'bonus_magical_defense': 0, 'bonus_hit': 3,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'SHOES': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 5,
            'bonus_evasion': 3,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
RING_EQUIPMENTS = {
    'RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'KRATOS\'S_RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'HERMES\'S_RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
    'ARTEMIS\'S_RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 1,
        }
    ),
    'HECATE\'S_RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'GAIA\'S_RING': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
AMULET_EQUIPMENTS = {
    'NECKLACE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'AMULET': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'CHARM': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_penality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
    'COIN': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 0,
            'bonus_evasion': 0,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 0,
            'bonus_evasion': 10,
        }
    ),
    'SCARF': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 5,
            'bonus_physical_attack': 0, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 0, 'bonus_physical_defense': 0,
            'bonus_magical_defense': 0, 'bonus_hit': 5,
            'bonus_evasion': 10,
        },
        attr_penality_prob={
            'bonus_hit_points': 0, 'bonus_initiative': 0,
            'bonus_physical_attack': 5, 'bonus_precision_attack': 0,
            'bonus_magical_attack': 5, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 0,
            'bonus_evasion': 0,
        }
    ),
}

ALL_EQUIPMENTS_DEFINITIONS = {}
ALL_EQUIPMENTS_DEFINITIONS.update(ONE_HAND_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(TWO_HANDS_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(HELMET_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(ARMOR_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(BOOTS_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(RING_EQUIPMENTS)
ALL_EQUIPMENTS_DEFINITIONS.update(AMULET_EQUIPMENTS)


for weapon in ALL_WEAPONS:
    if not weapon in ALL_EQUIPMENTS_DEFINITIONS.keys():
        raise ValueError(f'Weapon {weapon} not defined.')

for weapon in ONE_HAND_EQUIPMENTS.keys():
    if not weapon in ALL_WEAPONS:
        raise ValueError(f'One hand weapon {weapon} not defined.')

for weapon in TWO_HANDS_EQUIPMENTS.keys():
    if not weapon in ALL_WEAPONS:
        raise ValueError(f'Two hands weapon {weapon} not defined.')
