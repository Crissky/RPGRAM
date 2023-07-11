from rpgram.boosters.classe import Classe
from rpgram.boosters.equipment import Equipment
from rpgram.boosters.race import Race
from rpgram.characters.char_base import BaseCharacter
from rpgram.enums.damage import DamageEnum
from rpgram.enums.equipment import EquipmentEnum
from rpgram.equips import Equips


STEEL_HELMET = Equipment(
    name='Capacete de Aço',
    equip_type=EquipmentEnum.HELMET,
    damage_types=None,
    weight=10,
    bonus_physical_defense=30,
    bonus_evasion=-5,
)
STEEL_GIANT_SWORD = Equipment(
    name='Espada Gigante de Aço',
    equip_type=EquipmentEnum.TWO_HANDS,
    damage_types=DamageEnum.SLASHING,
    weight=40,
    bonus_physical_attack=30,
    bonus_hit=15,
    bonus_evasion=-10,
)
STEEL_ARMOR = Equipment(
    name='Armadura de Aço',
    equip_type=EquipmentEnum.ARMOR,
    damage_types=None,
    weight=60,
    bonus_physical_defense=80,
    bonus_evasion=-25,
)
LEATHER_BOOTS = Equipment(
    name='Botas de Couro',
    equip_type=EquipmentEnum.BOOTS,
    damage_types=None,
    weight=10,
    bonus_physical_defense=10,
    bonus_magical_defense=10,
    bonus_evasion=30,
)
ANY_RING = Equipment(
    name='Algum Anel',
    equip_type=EquipmentEnum.RING,
    damage_types=None,
    weight=0.1,
    bonus_evasion=100,
)
BRIGHT_NECKLACE = Equipment(
    name='Colar Brilhante',
    equip_type=EquipmentEnum.NECKLACE,
    damage_types=None,
    weight=0.2,
    bonus_charisma=150,
)
EQUIPS = Equips(
    helmet=STEEL_HELMET,
    left_hand=STEEL_GIANT_SWORD,
    armor=STEEL_ARMOR,
    boots=LEATHER_BOOTS,
    ring=ANY_RING,
    necklace=BRIGHT_NECKLACE,
)
WARRIOR_CLASSE = Classe(
    name='GUERREIRO',
    description='GUERREIRO TESTE',
    bonus_strength=15,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=10,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.5,
    multiplier_dexterity=1,
    multiplier_constitution=1.0,
    multiplier_intelligence=1,
    multiplier_wisdom=1,
    multiplier_charisma=1,
)
HUMAN_RACE = Race(
    name='HUMANO',
    description='HUMANO TESTE',
    bonus_strength=15,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=10,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.5,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.0,
    multiplier_wisdom=1.0,
    multiplier_charisma=1.0,
)
BASE_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=WARRIOR_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=21,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)

if __name__ == '__main__':
    print(f'BASE_CHARACTER: {BASE_CHARACTER}')