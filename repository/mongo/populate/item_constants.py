# DAMAGE_TYPES para equipamentos de uma ou duas mãos
SLASHING_WEAPONS = ['SWORD', 'DAGGER', 'GREAT_SWORD']
BLUDGEONING_WEAPONS = ['SHIELD', 'STAFF']
PIERCING_WEAPONS = ['BOW']
MAGIC_WEAPONS = ['WAND']

ALL_WEAPONS = []
ALL_WEAPONS.extend(SLASHING_WEAPONS)
ALL_WEAPONS.extend(BLUDGEONING_WEAPONS)
ALL_WEAPONS.extend(PIERCING_WEAPONS)
ALL_WEAPONS.extend(MAGIC_WEAPONS)


# Equipamentos com maior chance de ter um tipo de dano extra
ENCHANTED_WEAPONS = ['WAND', 'STAFF']


# Equipamentos mais ou menos pesados que o normal
LIGHT_EQUIPMENTS = ['RING', 'NECKLACE']
HEAVY_EQUIPMENTS = ['GREAT_SWORD', 'SHIELD']
VERY_HEAVY_EQUIPMENTS = ['ARMOR']


# EQUIPMENTS DEFINITIONS
ONE_HAND_EQUIPMENTS = {
    'SWORD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 3,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 3,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 3,
        },
        attr_panality_prob={
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
            'bonus_physical_attack': 5, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 7,
            'bonus_evasion': 1,
        },
        attr_panality_prob={
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
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 2,
        },
        attr_panality_prob={
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
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 7, 'bonus_hit': 1,
            'bonus_evasion': 5,
        },
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        }
    ),
}
TWO_HANDS_EQUIPMENTS = {
    'GREAT_SWORD': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 10, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_panality_prob={
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
            'bonus_physical_attack': 1, 'bonus_precision_attack': 10,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 1,
        },
        attr_panality_prob={
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
            'bonus_physical_attack': 3, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 10, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 5, 'bonus_hit': 5,
            'bonus_evasion': 5,
        },
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 3,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 5,
        }
    ),
}
HELMET_EQUIPMENTS = {
    'HELMET': dict(
        attr_bonus_prob={
            'bonus_hit_points': 5, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 7, 'bonus_hit': 1,
            'bonus_evasion': 3,
        },
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
        }
    ),
}
ARMOR_EQUIPMENTS = {
    'ARMOR': dict(
        attr_bonus_prob={
            'bonus_hit_points': 10, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 10,
            'bonus_magical_defense': 10, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 10,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 5,
            'bonus_evasion': 10,
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
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
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
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        }
    ),
}
NECKLACE_EQUIPMENTS = {
    'NECKLACE': dict(
        attr_bonus_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
        },
        attr_panality_prob={
            'bonus_hit_points': 1, 'bonus_initiative': 1,
            'bonus_physical_attack': 1, 'bonus_precision_attack': 1,
            'bonus_magical_attack': 1, 'bonus_physical_defense': 1,
            'bonus_magical_defense': 1, 'bonus_hit': 1,
            'bonus_evasion': 1,
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
ALL_EQUIPMENTS_DEFINITIONS.update(NECKLACE_EQUIPMENTS)


for weapon in ALL_WEAPONS:
    if not weapon in ALL_EQUIPMENTS_DEFINITIONS.keys():
        raise ValueError(f'Weapon {weapon} not defined.')

for weapon in ONE_HAND_EQUIPMENTS.keys():
    if not weapon in ALL_WEAPONS:
        raise ValueError(f'One hand weapon {weapon} not defined.')

for weapon in TWO_HANDS_EQUIPMENTS.keys():
    if not weapon in ALL_WEAPONS:
        raise ValueError(f'Two hands weapon {weapon} not defined.')
