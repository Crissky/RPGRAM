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
    CurseCondition,
    ExhaustionCondition,
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
    FrenzyCondition,
    FuriousFuryCondition,
    FuriousInstinctCondition,
    MysticalConfluenceCondition,
    MysticalProtectionCondition,
    MysticalVigorCondition,
    RobustBlockCondition
)
from rpgram.conditions.target_skill import (
    ShatterCondition,
    WarBannerCondition
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
    STUNNED,
)
from rpgram.enums.consumable import HealingConsumableEnum
from rpgram.enums.skill import (
    BarbarianSkillEnum,
    GuardianSkillEnum,
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
    if name == BERSERKER:
        condition_class = BerserkerCondition
    elif name == BLEEDING:
        condition_class = BleedingCondition
    elif name == BLINDNESS:
        condition_class = BlindnessCondition
    elif name == BURN:
        condition_class = BurnCondition
    elif name == CONFUSION:
        condition_class = ConfusionCondition
    elif name == CURSE:
        condition_class = CurseCondition
    elif name == EXHAUSTION:
        condition_class = ExhaustionCondition
    elif name == FROZEN:
        condition_class = FrozenCondition
    elif name == PARALYSIS:
        condition_class = ParalysisCondition
    elif name == PETRIFIED:
        condition_class = PetrifiedCondition
    elif name == POISONING:
        condition_class = PoisoningCondition
    elif name == SILENCE:
        condition_class = SilenceCondition
    elif name == STUNNED:
        condition_class = StunnedCondition
    # HEALING BUFFS
    elif name == HealingConsumableEnum.HEAL1.value:
        condition_class = Heal1Condition
    elif name == HealingConsumableEnum.HEAL2.value:
        condition_class = Heal2Condition
    elif name == HealingConsumableEnum.HEAL3.value:
        condition_class = Heal3Condition
    elif name == HealingConsumableEnum.HEAL4.value:
        condition_class = Heal4Condition
    elif name == HealingConsumableEnum.HEAL5.value:
        condition_class = Heal5Condition
    elif name == HealingConsumableEnum.HEAL6.value:
        condition_class = Heal6Condition
    elif name == HealingConsumableEnum.HEAL7.value:
        condition_class = Heal7Condition
    elif name == HealingConsumableEnum.HEAL8.value:
        condition_class = Heal8Condition
    # BARBARIAN BUFFS
    elif name == BarbarianSkillEnum.FURIOUS_FURY.value:
        condition_class = FuriousFuryCondition
    elif name == BarbarianSkillEnum.FURIOUS_INSTINCT.value:
        condition_class = FuriousInstinctCondition
    elif name == BarbarianSkillEnum.FRENZY.value:
        condition_class = FrenzyCondition
    # GUARDIAN BUFFS
    elif name == GuardianSkillEnum.ROBUST_BLOCK.value:
        condition_class = RobustBlockCondition
    elif name == GuardianSkillEnum.CRYSTAL_ARMOR.value:
        condition_class = CrystalArmorCondition
    elif name == GuardianSkillEnum.GUARDIAN_SHIELD.value:
        condition_class = GuardianShieldCondition
    elif name == GuardianSkillEnum.SHATTER.value:
        condition_class = ShatterCondition
    # SORCERER BUFFS
    elif name == SorcererSkillEnum.MYSTICAL_PROTECTION.value:
        condition_class = MysticalProtectionCondition
    elif name == SorcererSkillEnum.MYSTICAL_CONFLUENCE.value:
        condition_class = MysticalConfluenceCondition
    elif name == SorcererSkillEnum.MYSTICAL_VIGOR.value:
        condition_class = MysticalVigorCondition
    elif name == SorcererSkillEnum.PRISMATIC_SHIELD.value:
        condition_class = PrismaticShieldCondition
    elif name == SorcererSkillEnum.CHAOS_WEAVER.value:
        condition_class = ChaosWeaverCondition
    # WARRIOR BUFFS
    elif name == WarriorSkillEnum.AEGIS_SHADOW.value:
        condition_class = AegisShadowCondition
    elif name == WarriorSkillEnum.WAR_BANNER.value:
        condition_class = WarBannerCondition
    else:
        raise ValueError(f'Condição {name} não encontrada!')

    return condition_class(**kwargs)


if __name__ == '__main__':
    print(condition_factory(name=CONFUSION))
    print(condition_factory(name=CONFUSION, turn=10))
    print(condition_factory(name=CONFUSION, level=10))
    print(condition_factory(name=CONFUSION, turn=10, level=10))
