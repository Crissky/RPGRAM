from enum import Enum
from typing import TYPE_CHECKING, Union
from rpgram.conditions.barrier import (
    AegisShadowCondition,
    GuardianShieldCondition,
    PrismaticShieldCondition,
    ChaosWeaverCondition
)
from rpgram.conditions.condition import Condition
from rpgram.conditions.debuff import (
    BerserkerCondition,
    BleedingCondition,
    BlindnessCondition,
    BurnCondition,
    ConfusionCondition,
    CrystallizedCondition,
    CurseCondition,
    ExhaustionCondition,
    FearingCondition,
    FrozenCondition,
    ImprisonedCondition,
    ParalysisCondition,
    PetrifiedCondition,
    PoisoningCondition,
    SilenceCondition,
    StunnedCondition,
)
from rpgram.conditions.heal import (
    Heal1Condition,
    Heal2Condition,
    Heal3Condition,
    Heal4Condition,
    Heal5Condition,
    Heal6Condition,
    Heal7Condition,
    Heal8Condition,
)
from rpgram.conditions.self_skill import (
    ChaoticStepsCondition,
    CrystalArmorCondition,
    FafnirsScalesCondition,
    FrenzyCondition,
    FuriousFuryCondition,
    FuriousInstinctCondition,
    LavaSkinCondition,
    MistFormCondition,
    MysticalConfluenceCondition,
    MysticalProtectionCondition,
    MysticalVigorCondition,
    PenitenceCondition,
    RaijusFootstepsCondition,
    RobustBlockCondition,
    RockArmorCondition,
    ShadowStepsCondition
)
from rpgram.conditions.special_damage_skill import (
    SDBlueDjinnBalmCondition,
    SDGreenDragonBalmCondition,
    SDCrystallineInfusionCondition,
    SDEscarchaSapCondition,
    SDFellowBearCondition,
    SDFellowFalconCondition,
    SDFellowOwlCondition,
    SDFellowTigerCondition,
    SDIgneousSapCondition,
    SDPoisonousSapCondition,
    SDRedPhoenixBalmCondition,
    SDThornySpaulderCondition,
    SDSacredBalmCondition,
    SDWildAcidCondition,
    SDWildFireCondition,
    SDWildGroundCondition,
    SDWildLightningCondition,
    SDWildPoisonCondition,
    SDWildRockCondition,
    SDWildWindCondition
)
from rpgram.conditions.target_skill_buff import (
    AnansisTrickeryCondition,
    ArtemissArrowCondition,
    BodyguardBearCondition,
    CeridwensMagicPotionCondition,
    CourtesanAnointingCondition,
    GraceOfThePantheonCondition,
    HecatesFlamesCondition,
    HunterTigerCondition,
    IdunnsAppleCondition,
    IsissVeilCondition,
    KnightAnointingCondition,
    KratossWrathCondition,
    LordAnointingCondition,
    MaidenAnointingCondition,
    OgunsCloakCondition,
    RangerFalconCondition,
    SquireAnointingCondition,
    UllrsFocusCondition,
    VidarsBraveryCondition,
    OakArmorCondition,
    VineBucklerCondition,
    SilkFlossSpaulderCondition,
    WarBannerCondition,
    WarriorAnointingCondition,
    WatcherOwlCondition
)
from rpgram.conditions.target_skill_debuff import (
    MuddyCondition,
    ShatterCondition
)
from rpgram.enums.debuff import (
    DebuffEnum,
)
from rpgram.enums.consumable import HealingConsumableEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    ClericSkillEnum,
    DruidSkillEnum,
    GuardianSkillEnum,
    MageSkillEnum,
    PaladinSkillEnum,
    RogueSkillEnum,
    SorcererSkillEnum,
    WarriorSkillEnum
)


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


CONDITION_TYPES = Union[Condition, Enum, str]


def condition_factory(
    name: CONDITION_TYPES = None,
    condition_name: str = None,
    turn: int = None,
    level: int = None,
    power: int = None,
    damage: int = None,
    character: 'BaseCharacter' = None,
) -> Condition:
    from rpgram.characters.char_base import BaseCharacter
    if isinstance(condition_name, str) and name is None:
        name = condition_name

    kwargs = {}
    if isinstance(turn, int):
        kwargs['turn'] = turn
    elif turn is not None:
        raise TypeError(f'Turn deve ser do tipo inteiro: {type(turn)}')

    if isinstance(level, int):
        kwargs['level'] = level
    elif level is not None:
        raise TypeError(f'Level deve ser do tipo inteiro: {type(level)}')

    if isinstance(power, int):
        kwargs['power'] = power
    elif power is not None:
        raise TypeError(f'Power deve ser do tipo inteiro: {type(power)}')

    if isinstance(damage, int):
        kwargs['damage'] = damage
    elif damage is not None:
        raise TypeError(f'Damage deve ser do tipo inteiro: {type(damage)}')

    if isinstance(character, BaseCharacter):
        kwargs['character'] = character
    elif character is not None:
        raise TypeError(f'Personagem deve ser do tipo {BaseCharacter}')

    # DEBUFFS
    if compare_condition(name, DebuffEnum.BERSERKER):
        condition_class = BerserkerCondition
    elif compare_condition(name, DebuffEnum.BLEEDING):
        condition_class = BleedingCondition
    elif compare_condition(name, DebuffEnum.BLINDNESS):
        condition_class = BlindnessCondition
    elif compare_condition(name, DebuffEnum.BURN):
        condition_class = BurnCondition
    elif compare_condition(name, DebuffEnum.CONFUSION):
        condition_class = ConfusionCondition
    elif compare_condition(name, DebuffEnum.CRYSTALLIZED):
        condition_class = CrystallizedCondition
    elif compare_condition(name, DebuffEnum.CURSE):
        condition_class = CurseCondition
    elif compare_condition(name, DebuffEnum.EXHAUSTION):
        condition_class = ExhaustionCondition
    elif compare_condition(name, DebuffEnum.FEARING):
        condition_class = FearingCondition
    elif compare_condition(name, DebuffEnum.FROZEN):
        condition_class = FrozenCondition
    elif compare_condition(name, DebuffEnum.IMPRISONED):
        condition_class = ImprisonedCondition
    elif compare_condition(name, DebuffEnum.PARALYSIS):
        condition_class = ParalysisCondition
    elif compare_condition(name, DebuffEnum.PETRIFIED):
        condition_class = PetrifiedCondition
    elif compare_condition(name, DebuffEnum.POISONING):
        condition_class = PoisoningCondition
    elif compare_condition(name, DebuffEnum.SILENCE):
        condition_class = SilenceCondition
    elif compare_condition(name, DebuffEnum.STUNNED):
        condition_class = StunnedCondition
    # HEALING BUFFS
    elif compare_condition(name, HealingConsumableEnum.HEAL1):
        condition_class = Heal1Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL2):
        condition_class = Heal2Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL3):
        condition_class = Heal3Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL4):
        condition_class = Heal4Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL5):
        condition_class = Heal5Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL6):
        condition_class = Heal6Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL7):
        condition_class = Heal7Condition
    elif compare_condition(name, HealingConsumableEnum.HEAL8):
        condition_class = Heal8Condition
    # BARBARIAN BUFFS
    elif compare_condition(name, BarbarianSkillEnum.FURIOUS_FURY):
        condition_class = FuriousFuryCondition
    elif compare_condition(name, BarbarianSkillEnum.FURIOUS_INSTINCT):
        condition_class = FuriousInstinctCondition
    elif compare_condition(name, BarbarianSkillEnum.FRENZY):
        condition_class = FrenzyCondition
    elif compare_condition(name, BarbarianSkillEnum.RAIJŪÇÇÇS_FOOTSTEPS):
        condition_class = RaijusFootstepsCondition
    elif compare_condition(name, BarbarianSkillEnum.FAFNIRÇÇÇS_SCALES):
        condition_class = FafnirsScalesCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_FIRE):
        condition_class = SDWildFireCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_LIGHTNING):
        condition_class = SDWildLightningCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_WIND):
        condition_class = SDWildWindCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_ROCK):
        condition_class = SDWildRockCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_GROUND):
        condition_class = SDWildGroundCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_ACID):
        condition_class = SDWildAcidCondition
    elif compare_condition(name, BarbarianSkillEnum.WILD_POISON):
        condition_class = SDWildPoisonCondition
    # CLERIC BUFFS
    elif compare_condition(name, ClericSkillEnum.IDUNNÇÇÇS_APPLE):
        condition_class = IdunnsAppleCondition
    elif compare_condition(name, ClericSkillEnum.KRATOSÇÇÇS_WRATH):
        condition_class = KratossWrathCondition
    elif compare_condition(name, ClericSkillEnum.ULLRÇÇÇS_FOCUS):
        condition_class = UllrsFocusCondition
    elif compare_condition(name, ClericSkillEnum.HECATEÇÇÇS_FLAMES):
        condition_class = HecatesFlamesCondition
    elif compare_condition(name, ClericSkillEnum.OGUNÇÇÇS_CLOAK):
        condition_class = OgunsCloakCondition
    elif compare_condition(name, ClericSkillEnum.ISISÇÇÇS_VEIL):
        condition_class = IsissVeilCondition
    elif compare_condition(name, ClericSkillEnum.ANANSIÇÇÇS_TRICKERY):
        condition_class = AnansisTrickeryCondition
    elif compare_condition(name, ClericSkillEnum.VIDARÇÇÇS_BRAVERY):
        condition_class = VidarsBraveryCondition
    elif compare_condition(name, ClericSkillEnum.ARTEMISÇÇÇS_ARROW):
        condition_class = ArtemissArrowCondition
    elif compare_condition(name, ClericSkillEnum.CERIDWENÇÇÇS_MAGIC_POTION):
        condition_class = CeridwensMagicPotionCondition
    elif compare_condition(name, ClericSkillEnum.GRACE_OF_THE_PANTHEON):
        condition_class = GraceOfThePantheonCondition
    # DRUID BUFFS
    elif compare_condition(name, DruidSkillEnum.RANGER_FALCON):
        condition_class = RangerFalconCondition
    elif compare_condition(name, DruidSkillEnum.FELLOW_FALCON):
        condition_class = SDFellowFalconCondition
    elif compare_condition(name, DruidSkillEnum.GUARDIAN_BEAR):
        condition_class = BodyguardBearCondition
    elif compare_condition(name, DruidSkillEnum.FELLOW_BEAR):
        condition_class = SDFellowBearCondition
    elif compare_condition(name, DruidSkillEnum.HUNTER_TIGER):
        condition_class = HunterTigerCondition
    elif compare_condition(name, DruidSkillEnum.FELLOW_TIGER):
        condition_class = SDFellowTigerCondition
    elif compare_condition(name, DruidSkillEnum.WATCHER_OWL):
        condition_class = WatcherOwlCondition
    elif compare_condition(name, DruidSkillEnum.FELLOW_OWL):
        condition_class = SDFellowOwlCondition
    elif compare_condition(name, DruidSkillEnum.VINE_BUCKLER):
        condition_class = VineBucklerCondition
    elif compare_condition(name, DruidSkillEnum.SILK_FLOSS_SPAULDER):
        condition_class = SilkFlossSpaulderCondition
    elif compare_condition(name, DruidSkillEnum.THORNY_SPAULDER):
        condition_class = SDThornySpaulderCondition
    elif compare_condition(name, DruidSkillEnum.OAK_ARMOR):
        condition_class = OakArmorCondition
    elif compare_condition(name, DruidSkillEnum.POISONOUS_SAP):
        condition_class = SDPoisonousSapCondition
    elif compare_condition(name, DruidSkillEnum.IGNEOUS_SAP):
        condition_class = SDIgneousSapCondition
    elif compare_condition(name, DruidSkillEnum.ESCARCHA_SAP):
        condition_class = SDEscarchaSapCondition
    # GUARDIAN BUFFS
    elif compare_condition(name, GuardianSkillEnum.ROBUST_BLOCK):
        condition_class = RobustBlockCondition
    elif compare_condition(name, GuardianSkillEnum.CRYSTAL_ARMOR):
        condition_class = CrystalArmorCondition
    elif compare_condition(name, GuardianSkillEnum.GUARDIAN_SHIELD):
        condition_class = GuardianShieldCondition
    elif compare_condition(name, GuardianSkillEnum.CRYSTALLINE_INFUSION):
        condition_class = SDCrystallineInfusionCondition
    elif compare_condition(name, GuardianSkillEnum.SHATTER):
        condition_class = ShatterCondition
    # MAGE BUFFS
    elif compare_condition(name, MageSkillEnum.ROCK_ARMOR):
        condition_class = RockArmorCondition
    elif compare_condition(name, MageSkillEnum.LAVA_SKIN):
        condition_class = LavaSkinCondition
    elif compare_condition(name, MageSkillEnum.MIST_FORM):
        condition_class = MistFormCondition
    elif compare_condition(name, MageSkillEnum.MUDDY):
        condition_class = MuddyCondition
    # PALADIN BUFFS
    elif compare_condition(name, PaladinSkillEnum.SACRED_BALM):
        condition_class = SDSacredBalmCondition
    elif compare_condition(name, PaladinSkillEnum.GREENDRAGON_BALM):
        condition_class = SDGreenDragonBalmCondition
    elif compare_condition(name, PaladinSkillEnum.REDPHOENIX_BALM):
        condition_class = SDRedPhoenixBalmCondition
    elif compare_condition(name, PaladinSkillEnum.BLUEDJINN_BALM):
        condition_class = SDBlueDjinnBalmCondition
    elif compare_condition(name, PaladinSkillEnum.SQUIRE_ANOINTING):
        condition_class = SquireAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.WARRIOR_ANOINTING):
        condition_class = WarriorAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.MAIDEN_ANOINTING):
        condition_class = MaidenAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.KNIGHT_ANOINTING):
        condition_class = KnightAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.COURTESAN_ANOINTING):
        condition_class = CourtesanAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.LORD_ANOINTING):
        condition_class = LordAnointingCondition
    elif compare_condition(name, PaladinSkillEnum.PENITENCE):
        condition_class = PenitenceCondition
    # ROGUE BUFFS
    elif compare_condition(name, RogueSkillEnum.SHADOW_STEPS):
        condition_class = ShadowStepsCondition
    elif compare_condition(name, RogueSkillEnum.CHAOTIC_STEPS):
        condition_class = ChaoticStepsCondition
    # SORCERER BUFFS
    elif compare_condition(name, SorcererSkillEnum.MYSTICAL_PROTECTION):
        condition_class = MysticalProtectionCondition
    elif compare_condition(name, SorcererSkillEnum.MYSTICAL_CONFLUENCE):
        condition_class = MysticalConfluenceCondition
    elif compare_condition(name, SorcererSkillEnum.MYSTICAL_VIGOR):
        condition_class = MysticalVigorCondition
    elif compare_condition(name, SorcererSkillEnum.PRISMATIC_SHIELD):
        condition_class = PrismaticShieldCondition
    elif compare_condition(name, SorcererSkillEnum.CHAOS_WEAVER):
        condition_class = ChaosWeaverCondition
    # WARRIOR BUFFS
    elif compare_condition(name, WarriorSkillEnum.AEGIS_SHADOW):
        condition_class = AegisShadowCondition
    elif compare_condition(name, WarriorSkillEnum.WAR_BANNER):
        condition_class = WarBannerCondition
    else:
        raise ValueError(f'Condição {name} não encontrada!')

    return condition_class(**kwargs)


def compare_condition(name: CONDITION_TYPES, condition_enum: Enum) -> bool:
    if isinstance(name, str):
        name = name.upper()

    return (
        name in [
            condition_enum,
            condition_enum.name.upper(),
            condition_enum.value.upper(),
        ]
    )


def create_condition_to_dict(
    condition: Condition,
    character: 'BaseCharacter' = None
) -> dict:
    dict_condition = condition.to_dict()
    if 'need_character' in dict_condition:
        dict_condition['character'] = character
        dict_condition.pop('need_character')

    return dict_condition


def copy_condition(
    condition: Condition,
    character: 'BaseCharacter' = None
) -> Condition:
    dict_condition = create_condition_to_dict(condition, character)
    return condition_factory(**dict_condition)


if __name__ == '__main__':
    print(condition_factory(name=DebuffEnum.CONFUSION.name))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, turn=10))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, level=10))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, turn=10, level=10))
