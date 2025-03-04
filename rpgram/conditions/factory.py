from enum import Enum
from typing import TYPE_CHECKING, Union
from rpgram.conditions.barrier import (
    AegisShadowCondition,
    AjaxShieldCondition,
    BarrierCondition,
    BeatifyingAegisCondition,
    FlameMantillaCondition,
    GuardianShieldCondition,
    HealingRefugeCondition,
    MagicShieldCondition,
    PiskieWindbagCondition,
    PrismaticShieldCondition,
    ChaosWeaverCondition,
    ProtectiveAuraCondition,
    ProtectiveInfusionCondition,
    RobysticShieldCondition,
    RoyalShieldCondition
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
    DeathSentenceCondition,
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
    HealingCondition,
)
from rpgram.conditions.self_skill import (
    AlertCondition,
    ArenaDomainCondition,
    ChampionInspirationCondition,
    ChaoticStepsCondition,
    CrystalArmorCondition,
    FafnirsScalesCondition,
    FenrirsInstinctCondition,
    FlamingFuryCondition,
    FrenzyCondition,
    FuriousFuryCondition,
    FuriousInstinctCondition,
    HrungnirsSovereigntyCondition,
    ImproviseCondition,
    InvestigationCondition,
    LavaSkinCondition,
    MistFormCondition,
    MysticBlockCondition,
    MysticalConfluenceCondition,
    MysticalProtectionCondition,
    MysticalVigorCondition,
    PenitenceCondition,
    RaijusFootstepsCondition,
    RobustBlockCondition,
    RobysticBlockCondition,
    RockArmorCondition,
    ShadowStepsCondition,
    SharpFaroCondition,
    SniffCondition,
    TurtleStanceCondition,
    UnicornStanceCondition,
    VigilFlameCondition,
    YmirsResilienceCondition
)
from rpgram.conditions.special_damage_skill import (
    SDAresBladeCondition,
    SDBlueDjinnBalmCondition,
    SDFellowPandinusCondition,
    SDFellowTurtleCondition,
    SDFellowWolfCondition,
    SDFellowYetiCondition,
    SDFlamingFuryCondition,
    SDGreenDragonBalmCondition,
    SDCrystallineInfusionCondition,
    SDEscarchaSapCondition,
    SDFellowBearCondition,
    SDFellowFalconCondition,
    SDFellowOwlCondition,
    SDFellowTigerCondition,
    SDIgneousHeartCondition,
    SDIgneousSapCondition,
    SDMantilledArmsCondition,
    SDPoisonousSapCondition,
    SDRedPhoenixBalmCondition,
    SDThornySpaulderCondition,
    SDSacredBalmCondition,
    SDVigilArmsCondition,
    SDWildAcidCondition,
    SDWildFireCondition,
    SDWildGroundCondition,
    SDWildLightningCondition,
    SDWildPoisonCondition,
    SDWildRockCondition,
    SDWildWindCondition,
    SpecialDamageSkillCondition
)
from rpgram.conditions.target_skill_buff import (
    AgileFeetCondition,
    AnansisTrickeryCondition,
    ArtemissArrowCondition,
    BlueEquilibriumCondition,
    BodyguardBearCondition,
    BoneArmorCondition,
    BoneBucklerCondition,
    BoneSpaulderCondition,
    CeridwensMagicPotionCondition,
    ClairvoyantWolfCondition,
    CourtesanAnointingCondition,
    CrescentMoonBalladCondition,
    CrystalSapRingCondition,
    EagleEyeCondition,
    FighterPandinusCondition,
    GraceOfThePantheonCondition,
    HecatesFlamesCondition,
    HunterTigerCondition,
    IdunnsAppleCondition,
    IsissVeilCondition,
    KnightAnointingCondition,
    KratossWrathCondition,
    LeadershipCondition,
    LookouterYetiCondition,
    LordAnointingCondition,
    MaidenAnointingCondition,
    MartialBannerCondition,
    OgunsCloakCondition,
    ProtectorTurtleCondition,
    RangerFalconCondition,
    SquireAnointingCondition,
    TargetSkillBuffCondition,
    TricksterTrovaCondition,
    UllrsFocusCondition,
    VidarsBraveryCondition,
    OakArmorCondition,
    VineBucklerCondition,
    SilkFlossSpaulderCondition,
    VineCrosierCondition,
    VitalityAuraCondition,
    WarBannerCondition,
    WarCornuCondition,
    WarSongCondition,
    WarriorAnointingCondition,
    WatcherOwlCondition,
    WildCarnationCloakCondition
)
from rpgram.conditions.target_skill_debuff import (
    AchillesHeelCondition,
    DisarmorCondition,
    DoUchiCondition,
    KoteUchiCondition,
    MuddyCondition,
    RedEquilibriumCondition,
    ShatterCondition,
    TargetSkillDebuffCondition
)
from rpgram.enums.debuff import (
    DebuffEnum,
)
from rpgram.enums.consumable import HealingConsumableEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    BardSkillEnum,
    BerserkirSkillEnum,
    BountyHunterSkillEnum,
    ClericSkillEnum,
    DruidSkillEnum,
    DuelistSkillEnum,
    GladiatorSkillEnum,
    GuardianSkillEnum,
    HealerSkillEnum,
    HeraldSkillEnum,
    KnightSkillEnum,
    MageSkillEnum,
    MercenarySkillEnum,
    MultiClasseSkillEnum,
    NecromancerSkillEnum,
    PaladinSkillEnum,
    RangerSkillEnum,
    RogueSkillEnum,
    SamuraiSkillEnum,
    ShamanSkillEnum,
    SorcererSkillEnum,
    SorcererSupremeSkillEnum,
    SummonerSkillEnum,
    WarriorSkillEnum
)


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


CONDITION_TYPES = Union[Condition, Enum, str]
HAVE_POWER_CONDITIONS = (
    BarrierCondition,
    HealingCondition,
    SpecialDamageSkillCondition,
    TargetSkillBuffCondition,
    TargetSkillDebuffCondition
)


def condition_factory(
    name: CONDITION_TYPES = None,
    condition_name: str = None,
    turn: int = None,
    level: int = None,
    power: int = None,
    damage: int = None,
    character: 'BaseCharacter' = None,
    set_default_power: bool = False
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
    elif compare_condition(name, DebuffEnum.DEATH_SENTENCE):
        condition_class = DeathSentenceCondition
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
    # DUELIST BUFFS
    elif compare_condition(name, DuelistSkillEnum.AGILE_FEET):
        condition_class = AgileFeetCondition
    elif compare_condition(name, DuelistSkillEnum.EAGLE_EYE):
        condition_class = EagleEyeCondition
    elif compare_condition(name, DuelistSkillEnum.ACHILLEÇÇÇS_HEEL):
        condition_class = AchillesHeelCondition
    elif compare_condition(name, DuelistSkillEnum.DISARMOR):
        condition_class = DisarmorCondition
    # GUARDIAN BUFFS
    elif compare_condition(name, GuardianSkillEnum.CRYSTAL_ARMOR):
        condition_class = CrystalArmorCondition
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
    # HERALD BUFFS
    elif compare_condition(name, HeraldSkillEnum.MYSTIC_BLOCK):
        condition_class = MysticBlockCondition
    elif compare_condition(name, HeraldSkillEnum.ROBYSTIC_SHIELD):
        condition_class = RobysticShieldCondition
    elif compare_condition(name, HeraldSkillEnum.ROBYSTIC_BLOCK):
        condition_class = RobysticBlockCondition
    elif compare_condition(name, HeraldSkillEnum.VIGIL_FLAME):
        condition_class = VigilFlameCondition
    elif compare_condition(name, HeraldSkillEnum.VIGIL_ARMS):
        condition_class = SDVigilArmsCondition
    elif compare_condition(name, HeraldSkillEnum.FLAME_MANTILLA):
        condition_class = FlameMantillaCondition
    elif compare_condition(name, HeraldSkillEnum.MANTILLED_ARMS):
        condition_class = SDMantilledArmsCondition
    elif compare_condition(name, HeraldSkillEnum.BLUE_EQUILIBRIUM):
        condition_class = BlueEquilibriumCondition
    elif compare_condition(name, HeraldSkillEnum.RED_EQUILIBRIUM):
        condition_class = RedEquilibriumCondition
    elif compare_condition(name, HeraldSkillEnum.IGNEOUS_HEART):
        condition_class = SDIgneousHeartCondition
    # BARD BUFFS
    elif compare_condition(name, BardSkillEnum.WAR_SONG):
        condition_class = WarSongCondition
    elif compare_condition(name, BardSkillEnum.CRESCENT_MOON_BALLAD):
        condition_class = CrescentMoonBalladCondition
    elif compare_condition(name, BardSkillEnum.TRICKSTER_TROVA):
        condition_class = TricksterTrovaCondition
    # BOUNTY HUNTER BUFFS
    elif compare_condition(name, BountyHunterSkillEnum.SHARP_FARO):
        condition_class = SharpFaroCondition
    elif compare_condition(name, BountyHunterSkillEnum.INVESTIGATION):
        condition_class = InvestigationCondition
    # KNIGHT BUFFS
    elif compare_condition(name, KnightSkillEnum.CHAMPION_INSPIRATION):
        condition_class = ChampionInspirationCondition
    elif compare_condition(name, KnightSkillEnum.LEADERSHIP):
        condition_class = LeadershipCondition
    elif compare_condition(name, KnightSkillEnum.ROYAL_SHIELD):
        condition_class = RoyalShieldCondition
    # HEALER BUFFS
    elif compare_condition(name, HealerSkillEnum.VITALITY_AURA):
        condition_class = VitalityAuraCondition
    elif compare_condition(name, HealerSkillEnum.PROTECTIVE_AURA):
        condition_class = ProtectiveAuraCondition
    elif compare_condition(name, HealerSkillEnum.HEALING_REFUGE):
        condition_class = HealingRefugeCondition
    elif compare_condition(name, HealerSkillEnum.PROTECTIVE_INFUSION):
        condition_class = ProtectiveInfusionCondition
    elif compare_condition(name, HealerSkillEnum.BEATIFYING_AEGIS):
        condition_class = BeatifyingAegisCondition
    # GLADIATOR BUFFS
    elif compare_condition(name, GladiatorSkillEnum.TURTLE_STANCE):
        condition_class = TurtleStanceCondition
    elif compare_condition(name, GladiatorSkillEnum.UNICORN_STANCE):
        condition_class = UnicornStanceCondition
    elif compare_condition(name, GladiatorSkillEnum.ARENA_DOMAIN):
        condition_class = ArenaDomainCondition
    elif compare_condition(name, GladiatorSkillEnum.ARES_BLADE):
        condition_class = SDAresBladeCondition
    elif compare_condition(name, GladiatorSkillEnum.AJAX_SHIELD):
        condition_class = AjaxShieldCondition
    elif compare_condition(name, GladiatorSkillEnum.MARTIAL_BANNER):
        condition_class = MartialBannerCondition
    elif compare_condition(name, GladiatorSkillEnum.FLAMING_FURY):
        condition_class = FlamingFuryCondition
    elif compare_condition(name, GladiatorSkillEnum.FLAMING_FURY_BLADE):
        condition_class = SDFlamingFuryCondition
    elif compare_condition(name, GladiatorSkillEnum.WAR_CORNU):
        condition_class = WarCornuCondition
    # SUMMONER BUFFS
    elif compare_condition(name, SummonerSkillEnum.PISKIE_WINDBAG):
        condition_class = PiskieWindbagCondition
    elif compare_condition(name, MercenarySkillEnum.IMPROVISE):
        condition_class = ImproviseCondition
    # NECROMANCER BUFFS
    elif compare_condition(name, NecromancerSkillEnum.BONE_BUCKLER):
        condition_class = BoneBucklerCondition
    elif compare_condition(name, NecromancerSkillEnum.BONE_SPAULDER):
        condition_class = BoneSpaulderCondition
    elif compare_condition(name, NecromancerSkillEnum.BONE_ARMOR):
        condition_class = BoneArmorCondition
    # RANGER BUFFS
    elif compare_condition(name, RangerSkillEnum.SNIFF):
        condition_class = SniffCondition
    elif compare_condition(name, RangerSkillEnum.ALERT):
        condition_class = AlertCondition
    # SHAMAN BUFFS
    elif compare_condition(name, ShamanSkillEnum.VINE_CROSIER):
        condition_class = VineCrosierCondition
    elif compare_condition(name, ShamanSkillEnum.WILD_CARNATION_CLOAK):
        condition_class = WildCarnationCloakCondition
    elif compare_condition(name, ShamanSkillEnum.CRYSTAL_SAP_RING):
        condition_class = CrystalSapRingCondition
    elif compare_condition(name, ShamanSkillEnum.FIGHTER_PANDINUS):
        condition_class = FighterPandinusCondition
    elif compare_condition(name, ShamanSkillEnum.PROTECTOR_TURTLE):
        condition_class = ProtectorTurtleCondition
    elif compare_condition(name, ShamanSkillEnum.CLAIRVOYANT_WOLF):
        condition_class = ClairvoyantWolfCondition
    elif compare_condition(name, ShamanSkillEnum.LOOKOUTER_YETI):
        condition_class = LookouterYetiCondition
    elif compare_condition(name, ShamanSkillEnum.FELLOW_PANDINUS):
        condition_class = SDFellowPandinusCondition
    elif compare_condition(name, ShamanSkillEnum.FELLOW_TURTLE):
        condition_class = SDFellowTurtleCondition
    elif compare_condition(name, ShamanSkillEnum.FELLOW_WOLF):
        condition_class = SDFellowWolfCondition
    elif compare_condition(name, ShamanSkillEnum.FELLOW_YETI):
        condition_class = SDFellowYetiCondition
    # BERSERKIR BUFFS
    elif compare_condition(name, BerserkirSkillEnum.HRUNGNIRÇÇÇS_SOVEREIGNTY):
        condition_class = HrungnirsSovereigntyCondition
    elif compare_condition(name, BerserkirSkillEnum.FENRIRÇÇÇS_INSTINCT):
        condition_class = FenrirsInstinctCondition
    elif compare_condition(name, BerserkirSkillEnum.YMIRÇÇÇS_RESILIENCE):
        condition_class = YmirsResilienceCondition
    # SORCERER SUPREME BUFFS
    elif compare_condition(name, SorcererSupremeSkillEnum.MAGIC_SHIELD):
        condition_class = MagicShieldCondition
    # SAMURAI BUFFS
    elif compare_condition(name, SamuraiSkillEnum.KOTE_UCHI):
        condition_class = KoteUchiCondition
    elif compare_condition(name, SamuraiSkillEnum.DO_UCHI):
        condition_class = DoUchiCondition
    # MULTICLASSE BUFFS
    elif compare_condition(name, MultiClasseSkillEnum.ROBUST_BLOCK):
        condition_class = RobustBlockCondition
    elif compare_condition(name, MultiClasseSkillEnum.GUARDIAN_SHIELD):
        condition_class = GuardianShieldCondition
    else:
        raise ValueError(f'Condição {name} não encontrada!')

    # SET_DEFAULT_POWER
    if (
        set_default_power is True and
        power is None and
        issubclass(condition_class, HAVE_POWER_CONDITIONS)
    ):
        kwargs['power'] = 1
    elif (
        set_default_power is True and
        not issubclass(condition_class, HAVE_POWER_CONDITIONS)
    ):
        print(
            f'{condition_name} ({condition_class.__name__}) '
            f'não está na lista de condições que têm o atributo power.'
        )

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
