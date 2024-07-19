from enum import Enum
from typing import TYPE_CHECKING
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
    RaijusFootstepsCondition,
    RobustBlockCondition,
    RockArmorCondition
)
from rpgram.conditions.special_damage_skill import (
    SDCrystallineInfusionCondition,
    SDWildAcidCondition,
    SDWildFireCondition,
    SDWildGroundCondition,
    SDWildLightningCondition,
    SDWildPoisonCondition,
    SDWildRockCondition,
    SDWildWindCondition
)
from rpgram.conditions.target_skill_buff import (
    WarBannerCondition
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
    GuardianSkillEnum,
    MageSkillEnum,
    SorcererSkillEnum,
    WarriorSkillEnum
)


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def condition_factory(
    name: str = None,
    condition_name: str = None,
    turn: int = None,
    level: int = None,
    power: int = None,
    damage: int = None,
    character: 'BaseCharacter' = None,
) -> Condition:
    from rpgram.characters.char_base import BaseCharacter
    if isinstance(condition_name, str) and not isinstance(name, str):
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
    elif compare_condition(name, BarbarianSkillEnum.RAIJUS_FOOTSTEPS):
        condition_class = RaijusFootstepsCondition
    elif compare_condition(name, BarbarianSkillEnum.FAFNIRS_SCALES):
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


def compare_condition(name: str, condition_enum: Enum) -> bool:
    return name in [condition_enum, condition_enum.name, condition_enum.value]


if __name__ == '__main__':
    print(condition_factory(name=DebuffEnum.CONFUSION.name))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, turn=10))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, level=10))
    print(condition_factory(name=DebuffEnum.CONFUSION.name, turn=10, level=10))
