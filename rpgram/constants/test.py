from rpgram.boosters.classe import Classe
from rpgram.boosters.equipment import Equipment
from rpgram.boosters.race import Race
from rpgram.characters.char_base import BaseCharacter
from rpgram.conditions.heal import HealingCondition
from rpgram.consumables.heal import HealingConsumable
from rpgram.dice import Dice
from rpgram.enums.classe import ClasseEnum
from rpgram.enums.damage import DamageEnum
from rpgram.enums.equipment import EquipmentEnum
from rpgram.enums.turn import TurnEnum
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
BRIGHT_AMULET = Equipment(
    name='Colar Brilhante',
    equip_type=EquipmentEnum.AMULET,
    damage_types=None,
    weight=0.2,
    bonus_charisma=150,
)
EQUIPS = Equips(
    player_id=123,
    helmet=STEEL_HELMET,
    left_hand=STEEL_GIANT_SWORD,
    armor=STEEL_ARMOR,
    boots=LEATHER_BOOTS,
    ring=ANY_RING,
    amulet=BRIGHT_AMULET,
)
BARBARIAN_CLASSE = Classe(
    name=ClasseEnum.BARBARIAN.value,
    description='BÁRBARO TESTE',
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
CLERIC_CLASSE = Classe(
    name=ClasseEnum.CLERIC.value,
    description='BÁRBARO TESTE',
    bonus_strength=10,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=10,
    bonus_wisdom=15,
    bonus_charisma=10,
    multiplier_strength=1.0,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.0,
    multiplier_wisdom=1.5,
    multiplier_charisma=1.0,
)
DRUID_CLASSE = Classe(
    name=ClasseEnum.DRUID.value,
    description='BÁRBARO TESTE',
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
GUARDIAN_CLASSE = Classe(
    name=ClasseEnum.GUARDIAN.value,
    description='GUARDIÃO TESTE',
    bonus_strength=10,
    bonus_dexterity=10,
    bonus_constitution=15,
    bonus_intelligence=10,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.0,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.5,
    multiplier_intelligence=1.0,
    multiplier_wisdom=1.0,
    multiplier_charisma=1.0,
)
MAGE_CLASSE = Classe(
    name=ClasseEnum.MAGE.value,
    description='MAGO TESTE',
    bonus_strength=10,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=15,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.0,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.5,
    multiplier_wisdom=1.0,
    multiplier_charisma=1.0,
)
PALADIN_CLASSE = Classe(
    name=ClasseEnum.PALADIN.value,
    description='PALADINO TESTE',
    bonus_strength=15,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=10,
    bonus_wisdom=15,
    bonus_charisma=10,
    multiplier_strength=1.5,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.0,
    multiplier_wisdom=1.5,
    multiplier_charisma=1.0,
)
ROGUE_CLASSE = Classe(
    name=ClasseEnum.ROGUE.value,
    description='LADINO TESTE',
    bonus_strength=10,
    bonus_dexterity=15,
    bonus_constitution=10,
    bonus_intelligence=10,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.0,
    multiplier_dexterity=1.5,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.0,
    multiplier_wisdom=1.0,
    multiplier_charisma=1.0,
)
SORCERER_CLASSE = Classe(
    name=ClasseEnum.SORCERER.value,
    description='FEITICEIRO TESTE',
    bonus_strength=10,
    bonus_dexterity=10,
    bonus_constitution=10,
    bonus_intelligence=15,
    bonus_wisdom=10,
    bonus_charisma=10,
    multiplier_strength=1.0,
    multiplier_dexterity=1.0,
    multiplier_constitution=1.0,
    multiplier_intelligence=1.5,
    multiplier_wisdom=1.0,
    multiplier_charisma=1.0,
)
WARRIOR_CLASSE = Classe(
    name=ClasseEnum.WARRIOR.value,
    description='GUERREIRO TESTE',
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
BARBARIAN_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=BARBARIAN_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=101,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
CLERIC_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=CLERIC_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=101,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
DRUID_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=DRUID_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=101,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
GUARDIAN_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=GUARDIAN_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=101,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
MAGE_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=MAGE_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=151,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
PALADIN_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=PALADIN_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=151,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
ROGUE_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=ROGUE_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=151,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
SORCERER_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=SORCERER_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=51,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
WARRIOR_CHARACTER = BaseCharacter(
    char_name='PERSONAGEM TESTE',
    classe=WARRIOR_CLASSE,
    race=HUMAN_RACE,
    equips=EQUIPS,
    _id='ffffffffffffffffffffffff',
    level=101,
    xp=0,
    base_strength=10,
    base_dexterity=10,
    base_constitution=10,
    base_intelligence=10,
    base_wisdom=10,
    base_charisma=10,
    combat_damage=0,
)
POTION = HealingConsumable(
    name='Potion',
    description='Cura 100 de HP.',
    power=100,
    weight=0.1,
    condition=HealingCondition(
        name='Potion',
        power=20,
        frequency=TurnEnum.START,
        turn=5,
        level=1,
    )
)

if __name__ == '__main__':
    print(f'BASE_CHARACTER: {BASE_CHARACTER}')
    print('HP:', BASE_CHARACTER.cs.show_hit_points)
    BASE_CHARACTER.cs.hp = -300
    POTION(BASE_CHARACTER)
    BASE_CHARACTER.cs.hp = -600
    POTION(BASE_CHARACTER)

    dice = Dice(character=BASE_CHARACTER, faces=20)
    dice.throw()
    print(dice.value)
    print(dice.text)
    print(dice.throw())
    print(dice.throw())
    print(dice.throw(rethrow=True))
